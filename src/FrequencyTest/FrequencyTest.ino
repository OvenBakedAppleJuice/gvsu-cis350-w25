#include <FastLED.h>

#define LED_PIN     6
#define NUM_LEDS    256
#define BRIGHTNESS  100
#define LED_TYPE    WS2812B
#define COLOR_ORDER GRB

#define MATRIX_WIDTH 16
#define MATRIX_HEIGHT 16

CRGB leds[NUM_LEDS];
int columnHeights[MATRIX_WIDTH];  // To store parsed values

void setup() {
  Serial.begin(9600);
  FastLED.addLeds<LED_TYPE, LED_PIN, COLOR_ORDER>(leds, NUM_LEDS);
  FastLED.setBrightness(BRIGHTNESS);
  clearLEDs();
}

void loop() {
  if (Serial.available()) {
    String line = Serial.readStringUntil('\n');
    line.trim();
    
    // Split the line into 16 comma-separated integers
    int commaIndex = 0;
    int valueIndex = 0;
    while (line.length() > 0 && valueIndex < MATRIX_WIDTH) {
      int nextComma = line.indexOf(',');
      String valueStr;
      
      if (nextComma != -1) {
        valueStr = line.substring(0, nextComma);
        line = line.substring(nextComma + 1);
      } else {
        valueStr = line;
        line = "";
      }

      columnHeights[valueIndex] = constrain(valueStr.toInt(), 0, MATRIX_HEIGHT);
      valueIndex++;
    }

    // Clear all LEDs
    clearLEDs();

    // Light up columns
    for (int col = 0; col < MATRIX_WIDTH; col++) {
      int height = columnHeights[col];
      for (int row = 0; row < height; row++) {
        int ledIndex = getLEDIndex(row, col);
        leds[ledIndex] = CHSV(160, 255, BRIGHTNESS); // Blue hue
      }
    }

    FastLED.show();
  }
}

// Convert (row, col) to LED index (serpentine layout, bottom row = row 0)
int getLEDIndex(int row, int col) {
  int trueRow = MATRIX_HEIGHT - 1 - row; // flip to start lighting from bottom
  if (trueRow % 2 == 0) {
    // Left to right
    return trueRow * MATRIX_WIDTH + col;
  } else {
    // Right to left
    return trueRow * MATRIX_WIDTH + (MATRIX_WIDTH - 1 - col);
  }
}

void clearLEDs() {
  for (int i = 0; i < NUM_LEDS; i++) {
    leds[i] = CRGB::Black;
  }
  FastLED.show();
}
