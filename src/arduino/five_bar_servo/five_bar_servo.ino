#include <Servo.h>

// Pulse width (us) at write(0) and write(180). Datasheet only gives 1500 = center.
// Calibrate: widen until the horn reaches the true end angles without buzzing, then back off.
const int US_MIN = 500;
const int US_MAX = 2500;

Servo servoL;
Servo servoR;

void setup() {
  Serial.begin(115200);
  Serial.println("boot");  // shows up again mid-run = Arduino reset (power/ground problem)
  servoL.attach(9, US_MIN, US_MAX);
  servoR.attach(10, US_MIN, US_MAX);
}

void loop() {
  if (Serial.available()) {
    float deg1 = Serial.parseFloat();
    float deg2 = Serial.parseFloat();
    Serial.readStringUntil('\n');  // drop the trailing '\n' so it doesn't trigger a 0,0 write
    servoL.write(deg1);
    servoR.write(deg2);

    // pot wiper feedback (white wires), raw 0-1023
    Serial.print(analogRead(A0));
    Serial.print(',');
    Serial.println(analogRead(A1));
  }
}
