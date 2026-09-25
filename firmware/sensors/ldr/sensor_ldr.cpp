#include "sensor_ldr.h"

SensorLDR::SensorLDR(uint8_t analogPin) {
    _pin = analogPin;
}

void SensorLDR::begin() {
    pinMode(_pin, INPUT);
}

int SensorLDR::readValue() {
    return analogRead(_pin); // Returns raw ADC value (0 - 4095 on ESP32)
}