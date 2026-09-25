#ifndef SENSOR_LDR_H
#define SENSOR_LDR_H

#include <Arduino.h>

class SensorLDR {
public:
    SensorLDR(uint8_t analogPin);
    void begin();
    int readValue();
private:
    uint8_t _pin;
};

#endif