/**
 * @brief Demo Two Month Pico code. Blinks an LED and responds to a few basic serial commands.
 *
 */

uint32_t lastBlink = 0;
bool ledState = false;

void setup() {
  pinMode(LED_BUILTIN, OUTPUT);
  // LED on during setup
  digitalWrite(LED_BUILTIN, HIGH);

  // Configure serial for UART over USB
  Serial.begin(115200);
  delay(1000);

  // LED off before loop
  digitalWrite(LED_BUILTIN, LOW);
}

void loop() {
  // Blink on a timer
  if (millis() - lastBlink > 1000) {
    lastBlink = millis();
    ledState = !ledState;
    digitalWrite(LED_BUILTIN, ledState);
  }

  // Respond to serial commands
  if (Serial.available()) {
    String command = Serial.readStringUntil('\n');
    command.trim();

    if (command == "led_on") {
      digitalWrite(LED_BUILTIN, HIGH);
    } else if (command == "led_off") {
      digitalWrite(LED_BUILTIN, LOW);
    } else if (command == "ping") {
      Serial.println("pong");
    } else if (command == "time") {
      Serial.println(millis());
    }
  }
}
