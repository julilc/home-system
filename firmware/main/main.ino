#include "sensor_dht11.h"
#include <WiFi.h>
#include <PubSubClient.h>
#include <string.h>

// ==================== WIFI ====================
#define WIFI_SSID "Personal-405"
#define WIFI_PASS "20040306"

// ==================== MQTT ====================
#define MQTT_BROKER "broker.hivemq.com"
#define MQTT_PORT 1883

// ==================== SENSORES ====================
#define DHT_PIN 23
#define DHT_TYPE DHT11
#define LDR_PIN 34

// ==================== LED ====================
#define LED_PIN 27

// ==================== TOPICOS MQTT ====================
#define TOPIC_TEMP "homeHASIODNAOO/sensors/dht11/temperature"
#define TOPIC_HUM "homeHASIODNAOO/sensors/dht11/humidity"
#define TOPIC_LUM "homeHASIODNAOO/sensors/ldr/luminosity"

#define TOPIC_LED "homeHASIODNAOO/actuators/led"
#define TOPIC_LED_STATUS "homeHASIODNAOO/actuators/led/status"

// ==================== OBJETOS ====================
SensorDHT11 dhtSensor(DHT_PIN, DHT_TYPE);

WiFiClient wifiClient;
PubSubClient mqtt(wifiClient);

// ==================== TEMPORIZADOR ====================
unsigned long tiempoAnterior = 0;
const unsigned long intervaloSensores = 10000;

// ==================== WIFI ====================
void conectarWiFi() {
    if (WiFi.status() == WL_CONNECTED) {
        return;
    }

    Serial.print("Conectando a WiFi");

    WiFi.mode(WIFI_STA);
    WiFi.begin(WIFI_SSID, WIFI_PASS);

    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
    }

    Serial.println();
    Serial.println("WiFi conectado");
    Serial.print("IP: ");
    Serial.println(WiFi.localIP());
}

// ==================== CALLBACK MQTT ====================
// Formato recibido: ON|cocina o OFF|cocina
void callbackMQTT(
    char* topic,
    byte* payload,
    unsigned int length
) {
    if (strcmp(topic, TOPIC_LED) != 0) {
        return;
    }

    char mensaje[100];

    if (length == 0 || length >= sizeof(mensaje)) {
        Serial.println("Mensaje MQTT demasiado largo o vacio");
        return;
    }

    memcpy(mensaje, payload, length);
    mensaje[length] = '\0';

    char* separador = strchr(mensaje, '|');

    if (separador == nullptr) {
        Serial.println("Formato invalido. Usar ON|habitacion u OFF|habitacion");
        return;
    }

    *separador = '\0';

    char* orden = mensaje;
    char* room = separador + 1;

    // Validar habitacion
    if (room[0] == '\0') {
        Serial.println("No se especifico la habitacion");
        return;
    }

    // Aplicar la orden
    if (strcmp(orden, "ON") == 0) {
        digitalWrite(LED_PIN, HIGH);
    } else if (strcmp(orden, "OFF") == 0) {
        digitalWrite(LED_PIN, LOW);
    } else {
        Serial.println("Orden de LED desconocida");
        return;
    }

    // Leer el nivel logico aplicado al pin
    bool encendido = (digitalRead(LED_PIN) == HIGH);

    const char* estado = encendido ? "ON" : "OFF";

    // Construir confirmacion: ON|cocina o OFF|cocina
    char confirmacion[100];

    snprintf(
        confirmacion,
        sizeof(confirmacion),
        "%s|%s",
        estado,
        room
    );

    Serial.print("Orden recibida para ");
    Serial.print(room);
    Serial.print(": ");
    Serial.println(orden);

    // Publicar confirmacion solamente si MQTT esta conectado
    bool publicado = mqtt.publish(
        TOPIC_LED_STATUS,
        confirmacion,
        false
    );

    if (publicado) {
        Serial.print("Confirmacion publicada: ");
        Serial.println(confirmacion);
    } else {
        Serial.println("ERROR: no se pudo publicar la confirmacion");
    }
}

// ==================== MQTT ====================
void conectarMQTT() {
    while (!mqtt.connected()) {
        Serial.print("Conectando a MQTT...");

        // ID unico para esta placa
        String clientId = "ESP32_DHT11_LDR_";
        clientId += String((uint32_t)ESP.getEfuseMac(), HEX);

        if (mqtt.connect(clientId.c_str())) {
            Serial.println(" conectado");

            if (mqtt.subscribe(TOPIC_LED)) {
                Serial.println("Suscripcion al control LED correcta");
            } else {
                Serial.println("Error al suscribirse al control LED");
            }
        } else {
            Serial.print("Error MQTT: ");
            Serial.println(mqtt.state());

            delay(2000);
        }
    }
}

// ==================== PUBLICAR SENSORES ====================
void publicarSensores() {
    // ---------- TEMPERATURA ----------
    float temperatura = dhtSensor.readTemperature();

    if (!isnan(temperatura)) {
        char mensaje[16];

        dtostrf(temperatura, 4, 1, mensaje);

        if (mqtt.publish(TOPIC_TEMP, mensaje)) {
            Serial.print("Temperatura: ");
            Serial.println(mensaje);
        } else {
            Serial.println("Error publicando temperatura");
        }
    } else {
        Serial.println("Error leyendo temperatura DHT11");
    }

    // ---------- HUMEDAD ----------
    float humedad = dhtSensor.readHumidity();

    if (!isnan(humedad)) {
        char mensaje[16];

        dtostrf(humedad, 4, 1, mensaje);

        if (mqtt.publish(TOPIC_HUM, mensaje)) {
            Serial.print("Humedad: ");
            Serial.println(mensaje);
        } else {
            Serial.println("Error publicando humedad");
        }
    } else {
        Serial.println("Error leyendo humedad DHT11");
    }

    // ---------- LUMINOSIDAD ----------
    int luminosidad = analogRead(LDR_PIN);

    char mensajeLum[16];
    snprintf(
        mensajeLum,
        sizeof(mensajeLum),
        "%d",
        luminosidad
    );

    if (mqtt.publish(TOPIC_LUM, mensajeLum)) {
        Serial.print("Luminosidad: ");
        Serial.println(mensajeLum);
    } else {
        Serial.println("Error publicando luminosidad");
    }
}

// ==================== SETUP ====================
void setup() {
    Serial.begin(115200);

    // Sensores
    dhtSensor.begin();
    pinMode(LDR_PIN, INPUT);

    // LED
    pinMode(LED_PIN, OUTPUT);
    digitalWrite(LED_PIN, LOW);

    // Conexion WiFi
    conectarWiFi();

    // Configuracion MQTT
    mqtt.setServer(MQTT_BROKER, MQTT_PORT);
    mqtt.setCallback(callbackMQTT);
    mqtt.setBufferSize(256);
    mqtt.setKeepAlive(30);
    mqtt.setSocketTimeout(3);

    conectarMQTT();

    Serial.println("ESP32 iniciado correctamente");
}

// ==================== LOOP ====================
void loop() {
    // Reconectar WiFi si se pierde la conexion
    if (WiFi.status() != WL_CONNECTED) {
        conectarWiFi();
    }

    // Reconectar MQTT si se pierde la conexion
    if (!mqtt.connected()) {
        conectarMQTT();
    }

    // Procesar mensajes MQTT entrantes
    mqtt.loop();

    // Publicar sensores cada 10 segundos
    unsigned long ahora = millis();

    if (ahora - tiempoAnterior >= intervaloSensores) {
        tiempoAnterior = ahora;
        publicarSensores();
    }
}
