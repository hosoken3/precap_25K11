#include <Servo.h>

Servo ds3218;
const int servoPin = 9; // PWM-capable pin
const int baudRate = 115200;

String inputBuffer = "";

void setup() {
  Serial.begin(baudRate);       // UART from Raspberry Pi
  ds3218.attach(servoPin);      // Attach servo to PWM pin
  ds3218.write(90);             // Default to center position
}

void loop() {
  while (Serial.available()) {  // Read UART input
    char c = Serial.read();
    if (c == '\n') {
      processCommand(inputBuffer);
      inputBuffer = "";
    } else {
      inputBuffer += c;
    }
  }
}

void processCommand(String cmd) {
  cmd.trim();
  if (cmd.startsWith("ROTATE ")) {        //Rotation
    int angle = cmd.substring(7).toInt();
    angle = constrain(angle, 0, 270); 
    ds3218.write(angle);
    Serial.println("OK ROTATE " + String(angle));
  } else if (cmd == "RESET") {           //Back position
    ds3218.write(90);
    Serial.println("OK RESET");
  } else {
    Serial.println("ERR UNKNOWN CMD");  //Error
  }
}
