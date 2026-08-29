import { useState, useRef, useEffect } from "react";
import "./App.css";

const API_URL = "http://127.0.0.1:8000";

const STEP_ICONS = {
  agent_decision: "🧠",
  retrieve: "🔍",
  relevance_check: "✅",
  reformulate: "🔄",
  answer_directly: "💬",
  final_answer: "🎯",
  error: "⚠️",
};

function TraceView({ trace }) {
  return (
    <div className="trace">
      {trace.map((event, i) => (
        <div key={i} className={`trace-step step-${event.step}`}>
          <span className="trace-icon">{STEP_ICONS[event.step] || "•"}</span>
          <span className="trace-label">{event.step.replace(/_/g, " ")}</span>
          <span className="trace-detail">{event.detail}</span>
        </div>
      ))}
    </div>
  );
}

function Message({ role, content, trace }) {
  const [showTrace, setShowTrace] = useState(false);

  return (
    <div className={`message ${role}`}>
      <div className="bubble">{content}</div>
      {role === "assistant" && trace && trace.length > 0 && (
        <div className="trace-toggle-wrap">
          <button className="trace-toggle" onClick={() => setShowTrace(!showTrace)}>
            {showTrace ? "Hide reasoning" : "Show reasoning"} ({trace.length} steps)
          </button>
          {showTrace && <TraceView trace={trace} />}
        </div>
      )}
    </div>
  );
}

export default function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [uploadStatus, setUploadStatus] = useState("");
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  async function sendMessage() {
    const query = input.trim();
    if (!query || loading) return;

    setMessages((prev) => [...prev, { role: "user", content: query }]);
    setInput("");
    setLoading(true);

    try {
      const res = await fetch(`${API_URL}/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query }),
      });
      const data = await res.json();

      if (!res.ok) throw new Error(data.detail || "Something went wrong");

      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: data.answer, trace: data.trace },
      ]);
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: `Error: ${err.message}`, trace: [] },
      ]);
    } finally {
      setLoading(false);
    }
  }

  async function handleUpload(e) {
    const file = e.target.files[0];
    if (!file) return;

    setUploadStatus(`Uploading ${file.name}...`);
    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await fetch(`${API_URL}/upload`, { method: "POST", body: formData });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || "Upload failed");
      setUploadStatus(`✅ ${data.filename} added — ${data.chunks_added} chunks`);
    } catch (err) {
      setUploadStatus(`❌ ${err.message}`);
    } finally {
      e.target.value = "";
    }
  }

  function handleKeyDown(e) {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  }

  return (
    <div className="app">
      <header className="header">
        <h1>Agentic RAG</h1>
        <label className="upload-btn">
          📄 Add PDF
          <input type="file" accept=".pdf" onChange={handleUpload} hidden />
        </label>
      </header>

      {uploadStatus && <div className="upload-status">{uploadStatus}</div>}

      <div className="chat-window">
        {messages.length === 0 && (
          <div className="empty-state">Ask a question about your documents.</div>
        )}
        {messages.map((m, i) => (
          <Message key={i} role={m.role} content={m.content} trace={m.trace} />
        ))}
        {loading && (
          <div className="message assistant">
            <div className="bubble loading">Thinking...</div>
          </div>
        )}
        <div ref={bottomRef} />
      </div>

      <div className="input-bar">
        <textarea
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Ask something..."
          rows={1}
        />
        <button onClick={sendMessage} disabled={loading}>
          Send
        </button>
      </div>
    </div>
  );
}