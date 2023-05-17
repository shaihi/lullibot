#include <Arduino.h>
#include <Servo.h>

#define SLOW 20
#define FAST 80

const int motorPin = 9;  // Motor control pin
Servo esc_1;

void set_esc_power (Servo esc, int power) {
  power = constrain(power, -100, 100);
  int signal_min = 1050;
  int signal_max = 1950;
  int signal_output = map(power, -100, 100, signal_min, signal_max); //map(value, fromLow, fromHigh, toLow, toHigh)
  esc.writeMicroseconds(signal_output);
}

void setup() {
  esc_1.attach(motorPin);
  Serial.begin(9600);
  // Set the motor pin as an output pin
  pinMode(motorPin, OUTPUT);
  while (!Serial) {
    ; // wait for serial port to connect.
  }
}

void loop() {
  set_esc_power(esc_1, 0);
  //minus goes to blue carton
  //set_esc_power(esc_1, 30);
  //delay(500);
  //exit(1);
  char buffer[16];
  if (Serial.available() > 0) {
    int size = Serial.readBytesUntil('\n', buffer, 12);
    //Stop motor
    if (buffer[0] == 'S') {
      set_esc_power(esc_1, 0);
    }
    //Fast forward
    if (buffer[0] == 'F') {
      set_esc_power(esc_1, FAST);
      delay(500);
    }
    //Slow forward
    if (buffer[0] == 'O') {
      set_esc_power(esc_1, SLOW);
      delay(500);
    }
    //Slow backward
    if (buffer[0] == 'A') {
      set_esc_power(esc_1, -SLOW);
      delay(500);
    }
    //Fast Backward
    if (buffer[0] == 'B') {
      set_esc_power(esc_1, -FAST);
      delay(500);
    }
  }
}