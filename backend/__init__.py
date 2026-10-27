import os
from dotenv import load_dotenv

load_dotenv()

SQL_DB_SERVER = os.getenv("SQL_DB_SERVER")
SQL_DB_NAME = os.getenv("SQL_DB_NAME")
SQL_DB_USER = os.getenv("SQL_DB_USER")
SQL_DB_PASSWORD = os.getenv("SQL_DB_PASSWORD")  
MODEL = os.getenv("MODEL")
OPEN_ROUTER_API_KEY = os.getenv("OPEN_ROUTER_API_KEY")
API_URL = os.getenv("API_URL")
MQTT_BROKER = os.getenv("MQTT_BROKER")
MQTT_PORT = int(os.getenv("MQTT_PORT"))
MQTT_TEMP_TOPIC = os.getenv("MQTT_TEMP_TOPIC")
MQTT_HUM_TOPIC = os.getenv("MQTT_HUM_TOPIC")
MQTT_LUMINOSITY_TOPIC = os.getenv("MQTT_LUMINOSITY_TOPIC")
MQTT_LED_TOPIC = os.getenv("MQTT_LED_TOPIC")
MQTT_LED_STATUS_TOPIC = os.getenv("MQTT_LED_STATUS_TOPIC")