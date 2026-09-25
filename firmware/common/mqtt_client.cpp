#include "mqtt_client.h"

MQTTHandler::MQTTHandler(const char* server, uint16_t port) : _mqttClient(_wifiClient) {
    _server = server;
    _mqttClient.setServer(_server, port);
}

void MQTTHandler::connect(const char* clientId) {
    while (!_mqttClient.connected()) {
        if (_mqttClient.connect(clientId)) {
            // Connected successfully
        } else {
            delay(5000);
        }
    }
}

void MQTTHandler::loop() {
    _mqttClient.loop();
}

bool MQTTHandler::isConnected() {
    return _mqttClient.connected();
}

bool MQTTHandler::publishSensorData(const char* topic, const char* deviceId, float temp, float hum, int ldr) {
    JsonDocument doc;
    doc["device_id"] = deviceId;
    doc["timestamp"] = millis(); // Replace with NTP timestamp if available
    doc["temperature"] = temp;
    doc["humidity"] = hum;
    doc["ldr_value"] = ldr;

    char buffer[256];
    serializeJson(doc, buffer);

    return _mqttClient.publish(topic, buffer);
}