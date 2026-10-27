import { useEffect, useRef, useState } from "react";
import "./App.css";

// Si VITE_API_URL no está definida, usa "" (ruta relativa al mismo dominio)
const API_URL = import.meta.env.VITE_API_URL || "";
const USER_ID = "julietalopezceratto";

const INITIAL_MESSAGE = {
  role: "assistant",
  content:
    "¡Hola Julieta! 👋 Soy tu asistente IoT del hogar. Puedo consultar los sensores de temperatura, humedad y luz de tu ESP32, o encender/apagar el LED. ¿En qué te ayudo?",
};

const QUICK_PROMPTS = [
  { icon: "🌡️", label: "¿Cuál es la temperatura y humedad actual?" },
  { icon: "☀️", label: "¿Cómo está el nivel de luz en la habitación?" },
  { icon: "💡", label: "Encender la luz LED" },
  { icon: "🌑", label: "Apagar la luz LED" },
];

function renderFormattedText(text) {
  if (!text) return null;
  const parts = text.split(/(\*\*.*?\*\*|\`.*?\`|\n)/g);
  return parts.map((part, i) => {
    if (part.startsWith("**") && part.endsWith("**")) {
      return <strong key={i}>{part.slice(2, -2)}</strong>;
    }
    if (part.startsWith("`") && part.endsWith("`")) {
      return <code key={i}>{part.slice(1, -1)}</code>;
    }
    if (part === "\n") {
      return <br key={i} />;
    }
    return part;
  });
}

export default function App() {
  const [messages, setMessages] = useState([INITIAL_MESSAGE]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [connected, setConnected] = useState(false);
  const bottomRef = useRef(null);
  const inputRef = useRef(null);

  const checkHealth = async () => {
    try {
      const response = await fetch(`${API_URL}/api/health`, {
        headers: {
          "ngrok-skip-browser-warning": "true",
        },
      });
      if (!response.ok) throw new Error("Servidor offline");
      const data = await response.json();
      setConnected(data.status === "ok");
    } catch {
      setConnected(false);
    }
  };

  useEffect(() => {
    checkHealth();
    const interval = setInterval(checkHealth, 8000);
    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  async function sendMessage(text = input) {
    const content = text.trim();
    if (!content || loading) return;

    setInput("");
    setError("");
    setLoading(true);

    setMessages((previous) => [...previous, { role: "user", content }]);

    try {
      const response = await fetch(`${API_URL}/api/chat`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "ngrok-skip-browser-warning": "true",
        },
        body: JSON.stringify({
          message: content,
          id_user: USER_ID,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Ocurrió un problema en la consulta.");
      }

      setMessages((previous) => [
        ...previous,
        {
          role: "assistant",
          content: data.reply,
          tools: data.tools_used || [],
        },
      ]);

      setConnected(true);
    } catch (err) {
      setError(err.message || "No se pudo conectar con el servidor.");
      setConnected(false);
    } finally {
      setLoading(false);
      setTimeout(() => inputRef.current?.focus(), 50);
    }
  }

  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  return (
    <div className="app-layout">
      <header className="app-header">
        <div className="header-brand">
          <div className="chip-icon">🤖</div>
          <div>
            <h1>ESP32 Smart Home</h1>
            <p>Agente de Control Ambiental & IoT</p>
          </div>
        </div>

        <div className={`status-pill ${connected ? "online" : "offline"}`}>
          <span className="pulse-dot"></span>
          <span>{connected ? "ESP32 Conectado" : "Servidor Desconectado"}</span>
        </div>
      </header>

      <main className="chat-feed">
        {messages.map((msg, idx) => (
          <div key={idx} className={`message-row ${msg.role}`}>
            <span className="sender-label">
              {msg.role === "user" ? "Julieta" : "Asistente IoT"}
            </span>

            <div className="message-bubble">
              {renderFormattedText(msg.content)}
            </div>

            {msg.tools && msg.tools.length > 0 && (
              <div className="tools-container">
                {msg.tools.map((tool, tIdx) => (
                  <span key={tIdx} className="tool-badge">
                    ⚡ {tool}
                  </span>
                ))}
              </div>
            )}
          </div>
        ))}

        {loading && (
          <div className="message-row assistant">
            <span className="sender-label">Asistente IoT</span>
            <div className="typing-indicator">
              <div className="dots-wrapper">
                <span></span>
                <span></span>
                <span></span>
              </div>
              <span>Consultando sensores / Ejecutando...</span>
            </div>
          </div>
        )}

        {error && <div className="error-card">⚠️ {error}</div>}
        <div ref={bottomRef} />
      </main>

      <div className="prompts-bar">
        {QUICK_PROMPTS.map((prompt, idx) => (
          <button
            key={idx}
            className="prompt-btn"
            onClick={() => sendMessage(prompt.label)}
            disabled={loading}
          >
            <span>{prompt.icon}</span>
            <span>{prompt.label}</span>
          </button>
        ))}
      </div>

      <footer className="input-area">
        <div className="input-wrapper">
          <textarea
            ref={inputRef}
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Escribe un comando (ej: '¿Cuál es la humedad actual?')..."
            rows={1}
            disabled={loading}
          />
          <button
            onClick={() => sendMessage()}
            disabled={loading || !input.trim()}
            className="send-btn"
          >
            Enviar
          </button>
        </div>
      </footer>
    </div>
  );
}