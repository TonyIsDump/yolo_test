const int ledPin = 7;  // LED connected to pin 13 (built-in LED on most Arduino boards)
unsigned long lastDataTime = 0;  // Timestamp of last received data
const unsigned long timeout = 500;  // Timeout in milliseconds (1 second)

void setup() {
  pinMode(ledPin, OUTPUT);  // Set LED pin as output
  digitalWrite(ledPin, LOW);  // Ensure LED is off initially
  Serial.begin(115200);  // Start serial communication at 115200 baud
}

void loop() {
  // Check if serial data is available
  if (Serial.available() > 0) {
    String data = Serial.readStringUntil('\r');  // Read until carriage return
    if (data.length() > 0) {
      digitalWrite(ledPin, HIGH);  // Turn on LED when data is received
      lastDataTime = millis();  // Update timestamp
    }
  }

  // Turn off LED if no data received for longer than timeout
  if (millis() - lastDataTime > timeout) {
    digitalWrite(ledPin, LOW);  // Turn off LED
  }
}