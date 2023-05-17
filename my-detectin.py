import jetson.inference
import jetson.utils

# Camera parameters
focal_length = 500  # in pixels (example value)
image_width = 640  # in pixels (example value)
real_width = 30  # in centimeters (example value)

net = jetson.inference.detectNet("ssd-mobilenet-v2", threshold=0.5)
camera = jetson.utils.videoSource("/dev/video0")      # '/dev/video0' for V4L2
display = jetson.utils.videoOutput("display://0") # 'my_video.mp4' for file

while display.IsStreaming():
    img = camera.Capture()
    detections = net.Detect(img)
    #overlay = jetson.utils.Overlay("box labels", img.width, img.height, "arial.ttf", 12)
    for detection in detections:
        class_id = detection.ClassID
        left, top, right, bottom = int(detection.Left), int(detection.Top), int(detection.Right), int(detection.Bottom)
        box_width = right - left
        box_height = bottom - top
        box_area = box_width * box_height
        object_width = (real_width * box_width) / image_width * (box_area / image_width**2)**0.5
        distance = (focal_length * real_width) / box_width
        label_text = "Class ID: {}, Object Width: {:.2f} cm, Distance: {:.2f} cm".format(class_id, object_width, distance)
        #overlay.AddText(left, top, label_text)
        # Do further processing with the object width and distance here
    #overlay.Render(img)
    display.Render(img)
    display.SetStatus("Object Detection | Network {:.0f} FPS".format(net.GetNetworkFPS()))
