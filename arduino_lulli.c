#include <Arduino.h>
#include <Servo.h>

#define SLOW_FWD 20
#define FAST_FWD 80
#define FAST_BCK 74
#define SLOW_BCK 16
#define UPDOWN 30
#define STRING_FULL_TIME_UP 8800 //milisceonds
#define STRING_FULL_TIME_DOWN 7500 //milisceonds

const int motorPin = 9;  // Motor control pin
const int kanenetPin = 10; //Kannent motor
Servo esc_1;
Servo esc_2;

void set_esc_power (Servo esc, int power) {
  power = constrain(power, -100, 100);
  int signal_min = 1050;
  int signal_max = 1950;
  int signal_output = map(power, -100, 100, signal_min, signal_max); //map(value, fromLow, fromHigh, toLow, toHigh)
  esc.writeMicroseconds(signal_output);
}

void setup() {
  esc_1.attach(motorPin);
  esc_2.attach(kanenetPin);
  Serial.begin(9600);
  // Set the motor pin as an output pin
  pinMode(motorPin, OUTPUT);
  pinMode(kanenetPin, OUTPUT);
  while (!Serial) {
    ; // wait for serial port to connect.
  }
}

void loop() {
  set_esc_power(esc_1, 0);
  set_esc_power(esc_2, 0);
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
      set_esc_power(esc_1, FAST_FWD);
      delay(500);
    }
    //Slow forward
    if (buffer[0] == 'O') {
      set_esc_power(esc_1, SLOW_FWD);
      delay(500);
    }
    //Slow backward
    if (buffer[0] == 'A') {
      set_esc_power(esc_1, -SLOW_BCK);
      delay(500);
    }
    //Fast Backward
    if (buffer[0] == 'B') {
      set_esc_power(esc_1, -FAST_BCK);
      delay(500);
    }
    //Take Kanenet down
    if (buffer[0] == 'D') {
      set_esc_power(esc_2, -UPDOWN);
      delay(STRING_FULL_TIME_DOWN);
      set_esc_power(esc_2, 0);
    }
    //Take Kanenet UP
    if (buffer[0] == 'U') {
      set_esc_power(esc_2, UPDOWN);
      delay(STRING_FULL_TIME_UP);
      set_esc_power(esc_2, 0);
    }
    //Take Kanenet UP
    if (buffer[0] == 'P') {
      set_esc_power(esc_2, UPDOWN);
      delay(300);
      set_esc_power(esc_2, 0);
    }
    //Take Kanenet UP
    if (buffer[0] == 'L') {
      set_esc_power(esc_2, -UPDOWN);
      delay(300);
      set_esc_power(esc_2, 0);
    }
  }
}
