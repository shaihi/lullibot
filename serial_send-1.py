import serial

with serial.Serial('/dev/ttyACM0', 9600, timeout=10) as ser:
    while True:
        led_on = input('Send a command to the motor (F/B/O/A/S)\n')[0]
        print(led_on)
        ser.write(bytes(led_on,'utf-8'))
        

