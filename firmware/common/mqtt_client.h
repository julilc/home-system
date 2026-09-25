#ifndef MQTT_CLIENT_H
#define MQTT_CLIENT_H

#include <WiFi.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>

class MQTTHandler {
public:
    MQTTHandler(const char* server, uint16_t port);
    void begin(MQTT_CALLBACK_SIGNATURE);
    void connect(const char* clientId, const char* subscribeTopic);
    void loop();
    bool publishTemperature(const char* topic, float temperature);
    bool isConnected();

private:
    WiFiClient _wifiClient;
    PubSubClient _mqttClient;
    const char* _server;
};

#endif