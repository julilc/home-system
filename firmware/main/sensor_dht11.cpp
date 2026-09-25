#include "sensor_dht11.h"

SensorDHT11::SensorDHT11(uint8_t pin, uint8_t type) : dht(pin, type) {}

void SensorDHT11::begin() {
    dht.begin();
}

float SensorDHT11::readTemperature() {
    return dht.readTemperature();
}

float SensorDHT11::readHumidity() {
    return dht.readHumidity();
}