import requests
import json
import os
import time
from backend.database.sql.insert import save_message
from backend.database.sql.select import load_memory
from agent.planning import SYSTEM_PROMPT

def call_model(messages):

    response = requests.post(
        os.getenv("API_URL"),
        headers={
            "Authorization": f"Bearer {os.getenv('OPEN_ROUTER_API_KEY')}",
            "Content-Type": "application/json"
        },
        json={
            "model": os.getenv("MODEL"),
            "messages": messages,
            "reasoning": {
                "enabled": True
            }
        }
    )

    response.raise_for_status()

    return response.json()

def start_chat():

    id_user = "julietalopezceratto"

    # Retrieve memory from sql database
    memory = load_memory(id_user, top_k=10)

    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        }
    ]

    messages.extend(memory)
    while True:
        timeout = 10
        user_message = input(
            "\nEnter your message (or '0' to exit): "
        )

        if user_message == "0":
            break

        

        if timeout > 0:
            time.sleep(timeout)

        # User message
        
        user_msg = {
            "role": "user",
            "content": user_message,
            "reasoning_details": {}
        }

        messages.append(user_msg)

        save_message(
            id_user,
            user_msg
        )

        ## model call

        result = call_model(messages)

        assistant_message = result["choices"][0]["message"]

        assistant_msg = {
            "role": "assistant",
            "content": assistant_message.get("content"),
            "reasoning_details": assistant_message.get(
                "reasoning_details",
                {}
            )
        }

        # Agregar respuesta al contexto
        messages.append(assistant_msg)

        # Guardar respuesta en SQL
        save_message(
            id_user,
            assistant_msg
        )

        print("\nAssistant:")
        print(assistant_msg["content"])