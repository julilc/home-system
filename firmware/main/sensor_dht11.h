#ifndef SENSOR_DHT11_H
#define SENSOR_DHT11_H

#include <Arduino.h>
#include <DHT.h>

class SensorDHT11 {
public:
    SensorDHT11(uint8_t pin, uint8_t type);
    void begin();
    float readTemperature();
    float readHumidity();
private:
    DHT dht;
};

#endif