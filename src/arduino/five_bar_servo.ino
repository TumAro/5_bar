#include <Servo.h>

Servo servoL;
Servo servoR;

void setup() {
  Serial.begin(115200);
  servoL.attach(9);
  servoR.attach(10);
}

void loop() {
  if (Serial.available()) {
    float deg1 = Serial.parseFloat();
    float deg2 = Serial.parseFloat();
    servoL.write(deg1);
    servoR.write(deg2);
  }
}
