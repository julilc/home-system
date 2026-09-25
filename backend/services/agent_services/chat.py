import requests
import json
import os
import time
from backend.database.sql.insert import save_message
from backend.database.sql.select import load_memory
from agent.planning import SYSTEM_PROMPT
import json
from pathlib import Path
from backend.services.agent_services.tool_registry import TOOL_FUNCTIONS


BASE_DIR = Path(__file__).resolve().parents[3]

TOOLS_PATH = BASE_DIR / "agent" / "tools.json"

MODEL = os.getenv("MODEL")

with open(TOOLS_PATH, "r", encoding="utf-8") as f:
    TOOLS = json.load(f)

def call_model(messages):

    response = requests.post(
        os.getenv("API_URL"),
        headers={
            "Authorization": f"Bearer {os.getenv('OPEN_ROUTER_API_KEY')}",
            "Content-Type": "application/json"
        },
        json={
            "model":MODEL,
            "messages": messages,
            "tools": TOOLS,
            "reasoning": {
                "enabled": True
            }
        }
    )

    response.raise_for_status()

    return response.json()
def start_chat():

    id_user = "julietalopezceratto"

    # Recuperar memoria desde SQL
    memory = load_memory(id_user, top_k=10)

    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        }
    ]

    messages.extend(memory)

    while True:

        user_message = input(
            "\nEnter your message (or '0' to exit): "
        )

        if user_message == "0":
            break

        
        # User message
        

        user_msg = {
            "role": "user",
            "content": user_message,
            "reasoning_details": {}
        }

        messages.append(user_msg)

        save_message(
            id_user,
            user_msg,
            MODEL
        )

        # AGENT LOOP
        
        while True:

            # -------------------------
            # Model call
            # -------------------------
            print("\n[Model] Calling the model...")
            result = call_model(messages)

            assistant_message = result["choices"][0]["message"]

            # -------------------------
            # Check for tool calls
            # -------------------------

            tool_calls = assistant_message.get("tool_calls")

            if tool_calls:

                # save the assistant message exactly as returned by the model
                
                assistant_msg = {
                    "role": "assistant",
                    "content": assistant_message.get("content"),
                    "reasoning_details": assistant_message.get(
                        "reasoning_details",
                        {}
                    ),
                    "tool_calls": tool_calls
                }

                messages.append(assistant_msg)

                
                # Execute tool calls
                
                for tool_call in tool_calls:

                    function_name = tool_call["function"]["name"]

                    arguments = json.loads(
                        tool_call["function"]["arguments"]
                    )

                    print(
                        f"\n[Tool] Ejecutando: {function_name}"
                    )

                    print(
                        f"[Tool] Argumentos: {arguments}"
                    )

                    # Search for the function in the TOOL_FUNCTIONS dictionary
                    function = TOOL_FUNCTIONS.get(function_name)

                    if function is None:

                        tool_result = {
                            "error": (
                                f"La herramienta "
                                f"'{function_name}' no existe."
                            )
                        }

                    else:

                        try:

                            tool_result = function(**arguments)

                        except Exception as e:

                            tool_result = {
                                "error": str(e)
                            }

                    print(
                        f"[Tool] Resultado: {tool_result}"
                    )

                    # Retrieve the tool result and append it to the messages

                    tool_msg = {
                        "role": "tool",
                        "tool_call_id": tool_call["id"],
                        "content": json.dumps(
                            tool_result,
                            ensure_ascii=False
                        )
                    }

                    messages.append(tool_msg)

                continue

            # No tool calls, proceed to save the assistant message and break the loop

            assistant_msg = {
                "role": "assistant",
                "content": assistant_message.get("content"),
                "reasoning_details": assistant_message.get(
                    "reasoning_details",
                    {}
                )
            }

            messages.append(assistant_msg)

            save_message(
                id_user,
                assistant_msg,
                MODEL
            )

            print("\nAssistant:")
            print(assistant_msg["content"])

            break