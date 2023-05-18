#!/usr/bin/python3

# -*- coding: utf-8 -*-
import jetson.inference
import jetson.utils
import serial
from enum import Enum


class movementDirection(Enum):
    FORWARD = 1
    BACKWARD = -1


class engineCMD(Enum):
    STOP = 1
    FWD_FAST = 2
    FWD_SLOW = 3
    BCK_FAST = 4
    BCK_SLOW = 5


# Camera parameters

focal_length = 500  # in pixels (example value)
image_width = 640  # in pixels (example value)
real_width = 30  # in centimeters (example value)

traveled_distance = 0.0  # where we are on the rail ranges from 0 to 50 with 0.01 increments
fast_increment = 6.69  # in cm. distance traveled with a FAST cmd
fast_decrement = 6.57# backward step is 6.57 cm
slow_increment = 0.85  # in cm. distance traveled with a SLOW cmd
movement_direction = movementDirection.FORWARD  # initial state
MAX_LENGTH = 60.0  # in cm - length of rails


def check_direction():
    global movement_direction
    distance_now = 0
    print("entered check_direction(), movement_direction="+str(movement_direction))
    if movement_direction == movementDirection.FORWARD:
        distance_now = traveled_distance + fast_increment
        if distance_now > MAX_LENGTH:
            movement_direction = movementDirection.BACKWARD
            print("changed direction to BACKWARD")
    if movement_direction == movementDirection.BACKWARD:
        print("checking if going beyond zero")
        distance_now = traveled_distance - fast_decrement
        print("distance now is: " + str(distance_now))
        if distance_now < 1.0:
            print("entered condition to change direction")
            movement_direction = movementDirection.FORWARD
            print("changed to FORWARD")
  
  #  print("Calculated distance is:" + str(distance_now))


# cmd is an Enum of engineCMD and ser is the Serial object for communication

def sendEngineCMD(cmd, ser):
    global traveled_distance
    # input for Arduino:
    # 'S' - Stop
    # 'F' - fast forward
    # 'B' - fast backward
    # 'O' - Slow forward
    # 'A' - Slow Backward
    if cmd == engineCMD.STOP:
        ser.write(bytes('S\n', 'utf-8'))
    elif cmd == engineCMD.FWD_FAST:
        ser.write(bytes('F\n', 'utf-8'))
        traveled_distance += fast_increment
    elif cmd == engineCMD.FWD_SLOW:
        ser.write(bytes('O\n', 'utf-8'))
        traveled_distance += slow_increment
    elif cmd == engineCMD.BCK_FAST:
        ser.write(bytes('B\n', 'utf-8'))
        traveled_distance -= fast_decrement
    elif cmd == engineCMD.BCK_SLOW:
        ser.write(bytes('A\n', 'utf-8'))
        traveled_distance -= slow_increment

def main():
    global movement_direction
    net = jetson.inference.detectNet('ssd-mobilenet-v2', threshold=0.5)
    camera = jetson.utils.videoSource('/dev/video0')  # '/dev/video0' for V4L2
    display = jetson.utils.videoOutput('display://0')  # 'my_video.mp4' for file
    
   # movement_direction = movementDirection.BACKWARD  # initial state

    with serial.Serial('/dev/ttyACM0', 9600, timeout=10) as ser:
        while display.IsStreaming():
            img = camera.Capture()
            detections = net.Detect(img)

            # print("ran detection on image")

            for detection in detections:
                class_id = detection.ClassID
                (left, top, right, bottom) = (int(detection.Left),
                        int(detection.Top), int(detection.Right),
                        int(detection.Bottom))
                box_width = right - left
                box_height = bottom - top
                box_area = box_width * box_height
                object_width = real_width * box_width / image_width \
                    * (box_area / image_width ** 2) ** 0.5

            # distance = (focal_length * real_width) / box_width

                label_text = \
                    'Class ID: {}, Object Width: {:.2f} cm, Distance: ??? cm'.format(class_id,
                        object_width)
                class_name = net.GetClassDesc(detection.ClassID)
                if class_name == 'kite' || class_name == 'chicken' || class_name == 'mouse':
                    print ('Found one! ' + class_name)
                    print ('Object width is: ' + str(object_width))
                    sendEngineCMD(engineCMD.STOP, ser)
                    sleep(1000)
                    continue
                else:

                # tell the motor to continue
                    print("movement_direction: "+str(movement_direction))
                    check_direction()
                    print("movement_direction: "+str(movement_direction))
                    if movement_direction == movementDirection.FORWARD:
                        sendEngineCMD(engineCMD.FWD_FAST, ser)
                        print("Sending FST_FWD cmd. Current position: "+ str(traveled_distance))
                    if movement_direction == movementDirection.BACKWARD:
                        sendEngineCMD(engineCMD.BCK_FAST, ser)
                        print("Sending FST_BCK cmd. Current position: "+ str(traveled_distance))

            # net.SetOverlayString(label_text, left, top)
            # Do further processing with the object width and distance here

            display.Render(img)
            display.SetStatus('Object Detection | Network {:.0f} FPS'.format(net.GetNetworkFPS()))


if __name__ == '__main__':
    main()

