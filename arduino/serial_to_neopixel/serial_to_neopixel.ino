/// @file    Blink.ino
/// @brief   Blink the first LED of an LED strip
/// @example Blink.ino

#include <FastLED.h>

// How many leds in your strip?
#define NUM_LEDS 256

// For led chips like WS2812, which have a data line, ground, and power, you just
// need to define DATA_PIN.  For led chipsets that are SPI based (four wires - data, clock,
// ground, and power), like the LPD8806 define both DATA_PIN and CLOCK_PIN
// Clock pin only needed for SPI based chipsets when not using hardware SPI
#define DATA_PIN 6
#define CLOCK_PIN 13

// Define the array of leds
CRGB leds[NUM_LEDS];
CRGB currLedVals;
void setup() { 
    // Uncomment/edit one of the following lines for your leds arrangement.
    // ## Clockless types ##
    FastLED.addLeds<NEOPIXEL, DATA_PIN>(leds, NUM_LEDS);  // GRB ordering is assumed
    for (int i =0; i< NUM_LEDS; i++){
      leds[i] = CRGB(64, 0, 0);
    }
    FastLED.show();
    Serial.begin(115200);
    for (int i =0; i< NUM_LEDS; i++){
      leds[i] = CRGB(64, 64, 64);
    }

    FastLED.show();

}
int currLed = 0; 
int currColor = 0;
void loop() {
  if(Serial.available()){
    currLedVals[currColor] = Serial.read();
    currColor = (currColor + 1) % 3;
    if(currColor == 0) {
      leds[currLed] = currLedVals;
      currLed = (currLed + 1) % NUM_LEDS;
      if(currLed == 0){
        FastLED.show();
      }
    }
  }

}
