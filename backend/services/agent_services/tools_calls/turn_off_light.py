
import os
import threading
import paho.mqtt.client as mqtt

from backend.database.sql.insert import insert_led_status


def turn_off_light(room: str) -> str:
    """
    Apaga el LED mediante MQTT y guarda el estado
    únicamente después de recibir la confirmación del ESP32.
    """
    broker = os.getenv("MQTT_BROKER")
    port = int(os.getenv("MQTT_PORT", "1883"))
    topic = os.getenv("MQTT_LED_TOPIC")
    status_topic = os.getenv("MQTT_LED_STATUS_TOPIC")

    if not all([broker, topic, status_topic]):
        return "Error: faltan variables de entorno MQTT."

    room = room.strip()

    if not room:
        return "Error: debes especificar una habitación."

    confirmation = threading.Event()
    confirmed_status = {"status": None}

    def on_message(client, userdata, msg):
        try:
            status, confirmed_room = (
                msg.payload.decode("utf-8").strip().split("|", 1)
            )

            if (
                status == "OFF"
                and confirmed_room.strip() == room
            ):
                confirmed_status["status"] = status
                confirmation.set()

        except (UnicodeDecodeError, ValueError):
            pass

    client = mqtt.Client(
        callback_api_version=mqtt.CallbackAPIVersion.VERSION2,
        client_id=f"home_light_off_{room}"
    )

    client.on_message = on_message

    try:
        client.connect(broker, port, 60)
        client.subscribe(status_topic)
        client.loop_start()

        # Dar tiempo a que la conexión y suscripción se establezcan.
        import time
        time.sleep(0.3)

        info = client.publish(
            topic,
            f"OFF|{room}",
            qos=1
        )
        info.wait_for_publish(timeout=5)

        if not info.is_published() or info.rc != 0:
            return f"Error al enviar la orden para apagar la luz de {room}."

        if not confirmation.wait(timeout=5):
            return f"El ESP32 no confirmó el apagado de {room}."

        insert_led_status(room, confirmed_status["status"])

        return f"LED apagado y estado confirmado para: {room}"

    except Exception as e:
        return f"Error al apagar la luz de {room}: {e}"

    finally:
        if client.is_connected():
            client.disconnect()
        client.loop_stop()
