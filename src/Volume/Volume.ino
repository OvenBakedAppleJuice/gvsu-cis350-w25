#include <FastLED.h>

#define LED_PIN     6       // Pin connected to the data input on the LED strip
#define NUM_LEDS    256      // Number of LEDs in your strip
#define BRIGHTNESS  100     // Maximum brightness (0–255)
#define LED_TYPE    WS2812B
#define COLOR_ORDER GRB

CRGB leds[NUM_LEDS];

void setup() {
  Serial.begin(9600);  // Match this baud rate with your Python script
  FastLED.addLeds<LED_TYPE, LED_PIN, COLOR_ORDER>(leds, NUM_LEDS);
  FastLED.setBrightness(BRIGHTNESS);
  clearLEDs();
}

void loop() {
  if (Serial.available()) {
    String input = Serial.readStringUntil('\n');
    input.trim(); // remove whitespace
    int volume = input.toInt(); // Convert to integer

    // Constrain to 0–100
    volume = constrain(volume, 0, 100);

    // Determine how many rows to light (max 10 rows)
    int numRows = map(volume, 0, 100, 0, 16);  // Change 10 to 16 if you want to use full grid

    clearLEDs();

    for (int row = 0; row < numRows; row++) {
      for (int col = 0; col < 16; col++) {
        int index;
        if (row % 2 == 0) {
          // Even rows: left to right
          index = row * 16 + col;
        } else {
          // Odd rows: right to left
          index = row * 16 + (15 - col);
        }
        leds[index] = CHSV(160, 255, BRIGHTNESS); // Blue color
      }
    }

    FastLED.show();
  }
}



void clearLEDs() {
  for (int i = 0; i < NUM_LEDS; i++) {
    leds[i] = CRGB::Black;
  }
  FastLED.show();
}
