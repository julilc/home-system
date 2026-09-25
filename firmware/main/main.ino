#include "sensor_dht11.h"
#include <WiFi.h>
#include <PubSubClient.h>

// Credenciales de red
#define WIFI_SSID "Personal-405"
#define WIFI_PASS "20040306"
#define MQTT_BROKER "broker.hivemq.com" // O la IP de tu broker local

// Pines y configuración del sensor
#define DHT_PIN 23
#define DHT_TYPE DHT11

// --- AQUÍ DEFINES EL TÓPICO ---
#define TOPIC_TEMP "homesysxxssa/sensors/dht11/temperature" 
#define TOPIC_HUM "homesysxxssa/sensors/dht11/humidity"

SensorDHT11 dhtSensor(DHT_PIN, DHT_TYPE);
WiFiClient wifiClient;
PubSubClient mqtt(wifiClient);

unsigned long tiempoAnterior = 0;

void conectarWiFi() {
    WiFi.begin(WIFI_SSID, WIFI_PASS);
    while (WiFi.status() != WL_CONNECTED) {
        Serial.println("Conectando a wifi...");
        delay(500);
    }
    Serial.println("WiFi conectado");
}

void conectarMQTT() {
    while (!mqtt.connected()) {
        if (mqtt.connect("ESP32_DHT11_Node")) {
            Serial.println("MQTT conectado");
        } else {
            delay(2000);
        }
    }
}

void setup() {
    Serial.begin(115200);
    dhtSensor.begin();
    
    conectarWiFi();
    mqtt.setServer(MQTT_BROKER, 1883);
}

void loop() {
    if (!mqtt.connected()) {
        conectarMQTT();
    }
    mqtt.loop();

    // Publica cada 2 segundos
    if (millis() - tiempoAnterior >= 10000) {
        tiempoAnterior = millis();

        float t = dhtSensor.readTemperature();

        if (!isnan(t)) {
            char mensaje[16];
            dtostrf(t, 4, 1, mensaje);

            // Se usa el tópico definido arriba para enviar la info
            mqtt.publish(TOPIC_TEMP, mensaje);

            Serial.print("Temperatura publicada en [");
            Serial.print(TOPIC_TEMP);
            Serial.print("]: ");
            Serial.println(mensaje);
        } else {
            Serial.println("Error leyendo la temperatura desde DHT11");
        }
        float h = dhtSensor.readHumidity();
        if (!isnan(h)) {
            char msj[16];

            dtostrf(h,4,1,msj);
            mqtt.publish(TOPIC_HUM, msj );

            Serial.print("Humedad publicada en [");
            Serial.print(TOPIC_HUM);
            Serial.print("]:");
            Serial.println(msj);
        }    else {
            Serial.println("Error leyendo la humedad desde DHT11");
        }
    }
}