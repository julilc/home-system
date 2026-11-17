# HOME SYSTEM

Home System is an intelligent home automation project that combines an ESP32 device, MQTT messaging, a Python backend, a SQL Server database, and a conversational AI assistant. 

The system reads environmental data such as temperature, humidity, and luminosity, stores it persistently, exposes it through a FastAPI API, and lets the user interact through a React frontend. The assistant can answer questions about the home state and invoke tools to turn lights on/off, check sensor values, and report the current status of the environment.

---

## 1. OVERVIEW

This project integrates:
* ESP32 firmware for collecting sensor data
* MQTT broker communication for telemetry and actuator commands
* Python backend with FastAPI and AI tool-calling
* SQL Server database for persistence
* React + Vite frontend for user interaction
* KiCad electrical/electronic design files for the hardware
* AI agent layer using an external model API

---

## 2. MAIN FEATURES

* SENSOR MONITORING:
  - Temperature
  - Humidity
  - Luminosity
  - Light status

* DEVICE CONTROL:
  - LED on/off commands through MQTT

* CONVERSATIONAL INTERFACE:
  - Spanish assistant named Carlitos
  - Tool-based responses for home automation tasks

* PERSISTENT MEMORY:
  - User conversations and metadata stored in SQL Server

* WEB DASHBOARD:
  - React chat interface for interaction with the home system

* HARDWARE DOCUMENTATION:
  - KiCad schematics and PCB files

---

## 3. ARCHITECTURE

The system is organized in layers. In practice:
1. The ESP32 publishes sensor values to MQTT topics.
2. A Python listener consumes those messages and persists the values in the database.
3. The backend API receives chat requests from the frontend.
4. The assistant decides whether to answer directly or call a tool.
5. Tool calls can read the database or trigger MQTT commands to control the LED.

---

## 4. TECH STACK

* BACKEND: Python, FastAPI, Paho MQTT, pyodbc, pandas, dotenv, SQL Server
* FRONTEND: React, Vite, JavaScript / JSX
* EMBEDDED / HARDWARE: ESP32, DHT11 (temp/humidity), LDR (light), MQTT protocol, Arduino C++
* AI LAYER: OpenRouter API, Chat-completions model, Tool-calling architecture
* ELECTRONICS / PCB: KiCad for schematic and PCB design

---

## 5. ENVIRONMENT CONFIGURATION

This project uses environment variables stored in a `.env` file at the project root. 

IMPORTANT:
* Do not commit real secrets or API keys.
* The repository already includes a `.gitignore` to avoid pushing `.env` files.

---

## 6. DATABASE

The project uses Microsoft SQL Server and expects a database called `home`.

SQL Scripts:
* `database_config/create_database.sql`: Creates the database
* `database_config/create_tables_and_views.sql`: Creates the tables (Temperature, Humidity, Luminosity, LightStatus, MusicPlayed, PersonsRegistered, HomeStatus, LedStatus, Memories)

Database Access:
* Connection logic is defined in: `backend/database/sql/conection.py`
* Main queries and insert helpers: `backend/database/sql/insert.py` & `backend/database/sql/select.py`

---

## 7. BACKEND & API

The backend is built with FastAPI and is defined in: `backend/api_services/api.py`

Endpoints:
* `GET /api/health`: Returns service status
* `POST /api/chat`: Receives a user message, returns an AI response (using tool calling if needed), and persists the conversation.

---

## 8. AGENT AND TOOLS

The AI assistant uses:
* `agent/planning.py`: Defines the system prompt for the assistant.
* `agent/tools.json`: Describes the tool APIs exposed to the model.
* `backend/services/agent_services/tool_registry.py`: Registers actual Python functions behind each tool name.

Available tools: 
get_temperature, get_humidity, get_luminosity, get_home_status, get_light_status, get_music_played, get_persons_registered, turn_on_light, turn_off_light, play_music.

---

## 9. MQTT LISTENER

Implemented in: `backend/services/mqtt_services/mqtt_listener.py`
It subscribes to sensor topics (Temperature, Humidity, Luminosity, LED control, LED confirmation/status) and inserts the received values into the database.

---

## 10. FRONTEND

The frontend is a React app created with Vite located in the `frontend/` directory.
It displays chat messages, sends messages to the backend, shows server/ESP32 status, and provides quick action buttons.

---

## 11. FIRMWARE & HARDWARE BEHAVIOR

Located in `firmware/main/main.ino` (and related folders).

Hardware behavior:
* Connects to WiFi and MQTT broker.
* Publishes sensor data every 10 seconds (DHT11 temp/humidity, LDR luminosity).
* Detects sound events via an interrupt.
* Subscribes to LED control messages and publishes confirmation messages back to MQTT.

Pin mapping:
* DHT11: GPIO 23
* LDR: GPIO 34
* SOUND: GPIO 26
* LED: GPIO 27

---

## 12. DOCUMENTATION & TEST FILES

* HARDWARE DESIGN: `documentation/KiCad/` includes schematics, PCB layouts, footprints, and the ESP32 symbol library.
* TEST FILES: `test/sql/insert_memories.py` demonstrates how memory records can be inserted for validation.

---

## 13. DEVELOPMENT SETUP & USAGE

1. PYTHON BACKEND: Create a virtual environment, install requirements, and run the FastAPI server via uvicorn.
2. FRONTEND: Navigate to `frontend/`, run `npm install`, then `npm run dev`.
3. MQTT LISTENER: Run the MQTT Python script to start listening to the broker.
4. FIRMWARE: Open `firmware/main/main.ino` in Arduino IDE, select the ESP32 board, configure WiFi, and upload.

USAGE EXAMPLE:
Once everything is running, open the browser and chat with the assistant.
Try prompts like:
* “¿Cuál es la temperatura actual?”
* “¿Cómo está la humedad?”
* “Enciende la luz del dormitorio”

---

NOTES:
* This is an educational/prototype system.
* It relies on a real MQTT broker and SQL Server instance.
* API credentials must be kept private in the `.env` file.