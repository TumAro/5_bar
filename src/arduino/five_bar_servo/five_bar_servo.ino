#include <Servo.h>

// Pulse width (us) at write(0) and write(180). Datasheet only gives 1500 = center.
// Calibrate: widen until the horn reaches the true end angles without buzzing, then back off.
const int US_MIN = 500;
const int US_MAX = 2500;

// Command limits (deg) where the crank still clears the frame. Placeholders:
// jog each servo in the monitor until it just touches, back off ~5 deg, put the number here.
const float L_MIN = 30, L_MAX = 180;
const float R_MIN = 8, R_MAX = 170;

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
    // constrain() is a macro that evaluates its first arg up to 3 times: never pass parseFloat() into it
    deg1 = constrain(deg1, L_MIN, L_MAX);
    deg2 = constrain(deg2, R_MIN, R_MAX);
    Serial.readStringUntil('\n');  // drop the trailing '\n' so it doesn't trigger a 0,0 write
    servoL.writeMicroseconds(US_MIN + deg1 * (US_MAX - US_MIN) / 180);  // float deg, write() truncates to 1 deg steps
    servoR.writeMicroseconds(US_MIN + deg2 * (US_MAX - US_MIN) / 180);

    // pot wiper feedback (white wires), raw 0-1023
    Serial.print(analogRead(A0));
    Serial.print(',');
    Serial.println(analogRead(A1));
  }
}
