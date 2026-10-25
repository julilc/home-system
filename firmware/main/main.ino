#include "sensor_dht11.h"
#include <WiFi.h>
#include <PubSubClient.h>

// Credenciales de red
#define WIFI_SSID "Personal-405"
#define WIFI_PASS "20040306"
#define MQTT_BROKER "broker.hivemq.com" // O la IP de tu broker local

// Pines y configuración del sensor DHT
#define DHT_PIN 23
#define DHT_TYPE DHT11

// --- PINES DEL LDR ---
#define LDR_PIN 34 // Pin analógico ADC1 para el LDR (ESP32)

// --- TÓPICOS MQTT ---
#define TOPIC_TEMP "homeHASIODNAOO/sensors/dht11/temperature" 
#define TOPIC_HUM "homeHASIODNAOO/sensors/dht11/humidity"
#define TOPIC_LUM "homeHASIODNAOO/sensors/ldr/luminosity"

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
        if (mqtt.connect("ESP32_DHT11_LDR_Node")) {
            Serial.println("MQTT conectado");
        } else {
            delay(2000);
        }
    }
}

void setup() {
    Serial.begin(115200);
    dhtSensor.begin();
    
    // Configuración del pin LDR
    pinMode(LDR_PIN, INPUT);
    
    conectarWiFi();
    mqtt.setServer(MQTT_BROKER, 1883);
}

void loop() {
    if (!mqtt.connected()) {
        conectarMQTT();
    }
    mqtt.loop();

    // Publica cada 10 segundos (según el 10000 de la condición)
    if (millis() - tiempoAnterior >= 10000) {
        tiempoAnterior = millis();

        // --- LECTURA DE TEMPERATURA ---
        float t = dhtSensor.readTemperature();
        if (!isnan(t)) {
            char mensaje[16];
            dtostrf(t, 4, 1, mensaje);
            mqtt.publish(TOPIC_TEMP, mensaje);

            Serial.print("Temperatura publicada en [");
            Serial.print(TOPIC_TEMP);
            Serial.print("]: ");
            Serial.println(mensaje);
        } else {
            Serial.println("Error leyendo la temperatura desde DHT11");
        }

        // --- LECTURA DE HUMEDAD ---
        float h = dhtSensor.readHumidity();
        if (!isnan(h)) {
            char msj[16];
            dtostrf(h, 4, 1, msj);
            mqtt.publish(TOPIC_HUM, msj);

            Serial.print("Humedad publicada en [");
            Serial.print(TOPIC_HUM);
            Serial.print("]: ");
            Serial.println(msj);
        } else {
            Serial.println("Error leyendo la humedad desde DHT11");
        }

        // --- LECTURA DE LUMINOSIDAD (LDR) ---
        // El ESP32 tiene un ADC de 12 bits (valores de 0 a 4095)
        int ldrValue = analogRead(LDR_PIN);
        
        char msjLum[16];
        // Convertimos el número entero a cadena (string) para enviarlo
        snprintf(msjLum, sizeof(msjLum), "%d", ldrValue);
        
        mqtt.publish(TOPIC_LUM, msjLum);

        Serial.print("Luminosidad publicada en [");
        Serial.print(TOPIC_LUM);
        Serial.print("]: ");
        Serial.println(msjLum);
    }
}