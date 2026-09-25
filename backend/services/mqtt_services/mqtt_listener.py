import paho.mqtt.client as mqtt
import json
import os
import sys
from database.sql.insert import insert_temperature, insert_humidity, insert_luminosity  

# Config Broker MQTT
MQTT_BROKER = os.getenv("MQTT_BROKER")
MQTT_PORT = int(os.getenv("MQTT_PORT"))
MQTT_TEMP_TOPIC = os.getenv("MQTT_TEMP_TOPIC")
MQTT_HUM_TOPIC = os.getenv("MQTT_HUM_TOPIC")
MQTT_LUMINOSITY_TOPIC = os.getenv("MQTT_LUMINOSITY_TOPIC")

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("[MQTT] Successfully connected to the Broker!")
        client.subscribe(MQTT_TEMP_TOPIC)
        client.subscribe(MQTT_HUM_TOPIC)
        client.subscribe(MQTT_LUMINOSITY_TOPIC)
    else:
        print(f"[MQTT] Connection error, result code: {rc}")

def on_message(client, userdata, msg):
    try:
        # 1. Reads the message payload and decodes it to a string
        payload_str = msg.payload.decode("utf-8")
        print(f"[MQTT] Message received on [{msg.topic}]: {payload_str}")
        if msg.topic == MQTT_TEMP_TOPIC:
            # 2. Casts the payload to a float and prints it
            temperature = float(payload_str)
            print(f"[MQTT] Temperature received: {temperature}°C")
            # 3. Inserts the temperature into the database
            insert_temperature(1,temperature)
        elif msg.topic == MQTT_HUM_TOPIC:
            #2. Casts the payload to a float and prints it
            humidity = float(payload_str)
            print(f"[MQTT] Humidity received: {humidity}%")
            # 3. Inserts the humidity into the database
            insert_humidity(1,humidity)  
        elif msg.topic == MQTT_LUMINOSITY_TOPIC:
            #2. Casts the payload to a float and prints it
            luminosity = float(payload_str)
            print(f"[MQTT] Luminosity received: {luminosity}")
            # 3. Inserts the luminosity into the database
            insert_luminosity(1,luminosity)
    except json.JSONDecodeError:
        print(f"[MQTT Error] Could not decode JSON from message: {msg.payload}")
    except ValueError:
        print(f"[MQTT Error] Could not convert value to number: {msg.payload}")
    except Exception as e:
        print(f"[MQTT Error] An error occurred while processing the message: {e}")

def start_mqtt_listener():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    
    # Inits the MQTT client loop in a separate thread to allow the main program to continue running
    client.loop_start()
    print("[MQTT] Listener en segundo plano iniciado correctamente.")

def mqtt_listener():
    start_mqtt_listener()
    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("[MQTT] Stopping listener...")