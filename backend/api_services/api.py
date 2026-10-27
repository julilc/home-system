import json
import os
import sys 
sys.path.append(os.path.abspath("."))

from pathlib import Path

from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

import requests
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from agent.planning import SYSTEM_PROMPT
from backend.database.sql.insert import save_message
from backend.database.sql.select import load_memory
from backend.services.agent_services.tool_registry import TOOL_FUNCTIONS


# Cargar el .env desde la raíz de home-system.
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
load_dotenv(PROJECT_ROOT / ".env")

MODEL = os.getenv("MODEL")
API_URL = os.getenv(
    "MODEL_API_URL",
    "https://openrouter.ai/api/v1/chat/completions",
)
API_KEY = os.getenv("OPEN_ROUTER_API_KEY")

TOOLS_PATH = PROJECT_ROOT / "agent" / "tools.json"

with open(TOOLS_PATH, "r", encoding="utf-8") as file:
    TOOLS = json.load(file)


app = FastAPI(title="Home System Chat API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Habilita peticiones desde cualquier origen/ngrok
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=10000)
    id_user: str = Field(default="julietalopezceratto", min_length=1)


class ChatResponse(BaseModel):
    reply: str
    tools_used: list[str] = []


def call_model(messages):
    if not API_KEY or not MODEL:
        raise RuntimeError(
            "Falta configurar OPENROUTER_API_KEY o MODEL en el .env"
        )

    response = requests.post(
        API_URL,
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "model": MODEL,
            "messages": messages,
            "tools": TOOLS,
            "reasoning": {"enabled": True},
        },
        timeout=60,
    )

    if not response.ok:
        raise RuntimeError(
            f"OpenRouter respondió HTTP {response.status_code}: "
            f"{response.text[:1000]}"
        )

    return response.json()


@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.post("/api/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    user_message = request.message.strip()

    if not user_message:
        raise HTTPException(400, "El mensaje no puede estar vacío.")

    try:
        # Recuperar memoria persistida del usuario.
        memory = load_memory(request.id_user, top_k=10) or []

        messages = [
            {"role": "system", "content": SYSTEM_PROMPT}
        ]
        messages.extend(memory)

        user_msg = {
            "role": "user",
            "content": user_message,
            "reasoning_details": {},
        }
        messages.append(user_msg)

        save_message(request.id_user, user_msg, MODEL)

        tools_used = []

        # Ejecutar las herramientas y continuar la conversación.
        for _ in range(8):
            result = call_model(messages)
            assistant = result["choices"][0]["message"]
            tool_calls = assistant.get("tool_calls") or []

            if not tool_calls:
                reply = assistant.get("content") or (
                    "El modelo no devolvió texto."
                )

                assistant_msg = {
                    "role": "assistant",
                    "content": reply,
                    "reasoning_details": assistant.get(
                        "reasoning_details", {}
                    ),
                }

                messages.append(assistant_msg)
                save_message(request.id_user, assistant_msg, MODEL)

                return ChatResponse(
                    reply=reply,
                    tools_used=tools_used,
                )

            # Mantener el mensaje original de llamadas a herramientas.
            messages.append(assistant)

            for tool_call in tool_calls:
                function_name = tool_call["function"]["name"]
                tools_used.append(function_name)

                function = TOOL_FUNCTIONS.get(function_name)

                if function is None:
                    tool_result = {
                        "error": f"La herramienta '{function_name}' no existe."
                    }
                else:
                    try:
                        arguments = json.loads(
                            tool_call["function"]["arguments"]
                        )
                        tool_result = function(**arguments)
                    except Exception as exc:
                        tool_result = {"error": str(exc)}

                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call["id"],
                    "content": json.dumps(
                        tool_result,
                        ensure_ascii=False,
                        default=str,
                    ),
                })

        raise HTTPException(
            status_code=502,
            detail="Se alcanzó el límite de llamadas a herramientas.",
        )

    except HTTPException:
        raise
    except requests.RequestException as exc:
        raise HTTPException(
            status_code=502,
            detail=f"No se pudo conectar con OpenRouter: {exc}",
        ) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Error procesando el chat: {exc}",
        ) from exc

DIST_DIR = PROJECT_ROOT / "frontend" / "dist"

if DIST_DIR.exists():
    app.mount("/assets", StaticFiles(directory=DIST_DIR / "assets"), name="assets")

    @app.get("/{full_path:path}")
    def serve_spa(full_path: str):
        file_path = DIST_DIR / full_path
        if file_path.exists() and file_path.is_file():
            return FileResponse(file_path)
        return FileResponse(DIST_DIR / "index.html")