#include <Servo.h>

int servo_pin = 13;
int i = 0;
Servo servo;
int data = 0;

void setup() { 
  Serial.begin(9600);
  servo.attach(servo_pin);
  servo.write(180);
}

void loop() {
  if (Serial.available()) { 
    data = Serial.read();
  }
  if (data != 0) {
    servo.write(0);
    delay(15000);
    servo.write(180);
  }
}
