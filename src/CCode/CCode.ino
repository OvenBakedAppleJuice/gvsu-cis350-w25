#include <FastLED.h>

#define LED_PIN     6
#define NUM_LEDS    256
#define BRIGHTNESS  75
#define LED_TYPE    WS2812B
#define COLOR_ORDER GRB

#define MATRIX_WIDTH 16
#define MATRIX_HEIGHT 16

CRGB leds[NUM_LEDS];
int columnHeights[MATRIX_WIDTH];
int inputHue = 0;

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

    // Count number of commas
    int commaCount = 0;
    for (int i = 0; i < line.length(); i++) {
      if (line.charAt(i) == ',') {
        commaCount++;
      }
    }

    if (commaCount >= 2) {
      // === MODE 1: Hue + Column Heights ===
      int valueIndex = -1;
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

      if (valueIndex == -1) 
      {
        inputHue = constrain(abs(valueStr.toInt()), 0, 255);  // Hue input
      } 
      else 
      {
        columnHeights[valueIndex] = constrain(abs(valueStr.toInt()), 0, MATRIX_HEIGHT);  // Apply abs()
      }


        valueIndex++;
      }

      clearLEDs();

      for (int col = 0; col < MATRIX_WIDTH; col++) {
        int height = columnHeights[col];
        for (int row = 0; row < height; row++) {
          int ledIndex = getLEDIndex(row, col);
          leds[ledIndex] = CHSV(inputHue, 255, BRIGHTNESS);
        }
      }

      FastLED.show();

    } 
    else 
    {
  // === MODE 2: Hue + Volume-based Rows ===
  int commaPos = line.indexOf(',');
  if (commaPos != -1) {
    String hueStr = line.substring(0, commaPos);
    String volStr = line.substring(commaPos + 1);

    int hue = constrain(abs(hueStr.toInt()), 0, 255);
    int volume = abs(volStr.toInt());
    volume = constrain(volume, 0, 100);
    int numRows = map(volume, 0, 100, 0, MATRIX_HEIGHT);

    clearLEDs();

    for (int i = 0; i < numRows; i++) {
      int row = MATRIX_HEIGHT - 1 - i;  // Invert: light from bottom up
      for (int col = 0; col < MATRIX_WIDTH; col++) {
        int index;
        if (row % 2 == 0) {
          index = row * MATRIX_WIDTH + col;
        } else {
          index = row * MATRIX_WIDTH + (MATRIX_WIDTH - 1 - col);
        }
        leds[index] = CHSV(hue, 255, BRIGHTNESS);
      }
    }

    FastLED.show();
  }
}

  }
}

int getLEDIndex(int row, int col) {
  int trueRow = MATRIX_HEIGHT - 1 - row;
  if (trueRow % 2 == 0) {
    return trueRow * MATRIX_WIDTH + col;
  } else {
    return trueRow * MATRIX_WIDTH + (MATRIX_WIDTH - 1 - col);
  }
}

void clearLEDs() {
  for (int i = 0; i < NUM_LEDS; i++) {
    leds[i] = CRGB::Black;
  }
  FastLED.show();
}
