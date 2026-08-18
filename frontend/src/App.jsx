import { useState } from "react";
import "./App.css";

const API_URL = "https://ai-document-qa-backend-104102848745.asia-south1.run.app";

function App() {
  const [file, setFile] = useState(null);
  const [documentId, setDocumentId] = useState("");
  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState([]);
  const [uploading, setUploading] = useState(false);
  const [asking, setAsking] = useState(false);
  const [error, setError] = useState("");
  const [expandedSources, setExpandedSources] = useState({});

  const uploadFile = async () => {
    if (!file) {
      setError("Please select a PDF first.");
      return;
    }

    setUploading(true);
    setError("");
    setMessages([]);

    try {
      const formData = new FormData();
      formData.append("file", file);

      const response = await fetch(`${API_URL}/api/upload`, {
        method: "POST",
        body: formData,
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Upload failed.");
      }

      setDocumentId(data.document_id);
    } catch (err) {
      setError(err.message);
    } finally {
      setUploading(false);
    }
  };

  const askQuestion = async () => {
    const trimmedQuestion = question.trim();

    if (!documentId) {
      setError("Please upload a PDF first.");
      return;
    }

    if (!trimmedQuestion) {
      setError("Please enter a question.");
      return;
    }

    setAsking(true);
    setError("");

    const userMessage = {
      id: `${Date.now()}-user`,
      role: "user",
      question: trimmedQuestion,
    };

    setMessages((prev) => [...prev, userMessage]);
    setQuestion("");

    try {
      const response = await fetch(`${API_URL}/api/ask`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          document_id: documentId,
          question: trimmedQuestion,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Failed to get answer.");
      }

      setMessages((prev) => [
        ...prev,
        {
          id: `${Date.now()}-ai`,
          role: "ai",
          answer: data.answer,
          sources: data.sources || [],
        },
      ]);
    } catch (err) {
      setMessages((prev) => prev.filter((message) => message.id !== userMessage.id));
      setQuestion(trimmedQuestion);
      setError(err.message);
    } finally {
      setAsking(false);
    }
  };

  const resetDocument = () => {
    setFile(null);
    setDocumentId("");
    setQuestion("");
    setMessages([]);
    setError("");
    setExpandedSources({});
  };

  const handleFileChange = (event) => {
    const selectedFile = event.target.files?.[0];
    if (!selectedFile) return;

    if (selectedFile.type !== "application/pdf") {
      setError("Please select a PDF file.");
      return;
    }

    setFile(selectedFile);
    setError("");
    setDocumentId("");
    setMessages([]);
    setExpandedSources({});
  };

  const toggleSource = (messageId, sourceIndex) => {
    const key = `${messageId}-${sourceIndex}`;
    setExpandedSources((prev) => ({
      ...prev,
      [key]: !prev[key],
    }));
  };

  return (
    <div className="app">
      <header className="header">
        <div className="brand">
          <div className="brand-icon">✦</div>
          <div>
            <div className="logo">AI Document Q&A</div>
            <span className="brand-subtitle">Intelligent document assistant</span>
          </div>
        </div>

        <div className="badge">
          <span className="status-dot" />
          Powered by Gemini
        </div>
      </header>

      <main className="container">
        {!documentId && messages.length === 0 && (
          <section className="hero">
            <div className="eyebrow">
              <span>AI-POWERED</span>
              <span className="eyebrow-dot">•</span>
              <span>DOCUMENT INTELLIGENCE</span>
            </div>

            <h1>
              Turn your documents into
              <span className="gradient-text"> intelligent answers.</span>
            </h1>

            <p>
              Upload a PDF, let AI understand it, and ask questions in plain
              English. Get clear answers backed by relevant document sources.
            </p>

            <div className="feature-row">
              <div className="feature-pill"><span>⚡</span> Gemini AI</div>
              <div className="feature-pill"><span>⌕</span> Semantic search</div>
              <div className="feature-pill"><span>☁</span> Google Cloud</div>
            </div>
          </section>
        )}

        <section className="workspace">
          <div className="section-title">
            <div className="step">1</div>
            <div>
              <h2>Upload your document</h2>
              <p>Give your document to the AI assistant.</p>
            </div>
            {documentId && <span className="ready-badge">✓ Ready</span>}
          </div>

          {!documentId ? (
            <>
              <div className="upload-area">
                <input
                  id="file-input"
                  type="file"
                  accept=".pdf,application/pdf"
                  onChange={handleFileChange}
                />

                <label htmlFor="file-input" className="file-label">
                  <div className="upload-visual">
                    <div className="document-icon">▤</div>
                    <div className="upload-plus">+</div>
                  </div>

                  <strong>{file ? file.name : "Drop your PDF here"}</strong>

                  <span>
                    {file
                      ? `${(file.size / 1024 / 1024).toFixed(2)} MB • Ready to upload`
                      : "or click to browse from your computer"}
                  </span>

                  {!file && <small>PDF files only</small>}
                </label>
              </div>

              <button
                className="primary-button"
                onClick={uploadFile}
                disabled={uploading || !file}
              >
                {uploading ? (
                  <>
                    <span className="spinner" />
                    Processing document...
                  </>
                ) : (
                  <>
                    Upload & Analyze <span>→</span>
                  </>
                )}
              </button>
            </>
          ) : (
            <div className="document-ready">
              <div className="pdf-icon">PDF</div>
              <div className="document-info">
                <strong>{file?.name || "Document"}</strong>
                <span>Your document is ready for questions.</span>
              </div>
              <button className="change-button" onClick={resetDocument}>Change</button>
            </div>
          )}
        </section>

        <section className={`workspace question-card ${!documentId ? "locked" : ""}`}>
          <div className="section-title">
            <div className="step">2</div>
            <div>
              <h2>Ask anything</h2>
              <p>Ask questions about the information inside your PDF.</p>
            </div>
          </div>

          {messages.length > 0 && (
            <div className="conversation">
              {messages.map((message) =>
                message.role === "user" ? (
                  <div className="chat-row user-row" key={message.id}>
                    <div className="chat-bubble user-bubble">
                      <span className="chat-label">YOU</span>
                      <p>{message.question}</p>
                    </div>
                  </div>
                ) : (
                  <div className="chat-row ai-row" key={message.id}>
                    <div className="ai-avatar small">✦</div>
                    <div className="chat-bubble ai-bubble">
                      <span className="chat-label ai-label">AI ANSWER</span>
                      <p>{message.answer}</p>

                      {message.sources.length > 0 && (
                        <div className="sources">
                          <div className="sources-heading">
                            <div>
                              <h3>Relevant sources</h3>
                              <p>Document sections used to generate this answer.</p>
                            </div>
                            <span>
                              {message.sources.length} source
                              {message.sources.length > 1 ? "s" : ""}
                            </span>
                          </div>

                          {message.sources.map((source, index) => {
                            const key = `${message.id}-${index}`;
                            const expanded = Boolean(expandedSources[key]);
                            const text = source.text || "";
                            const isLong = text.length > 330;

                            return (
                              <div className="source" key={`${message.id}-${source.chunk_index}-${index}`}>
                                <div className="source-number">
                                  {String(index + 1).padStart(2, "0")}
                                </div>

                                <div className="source-content">
                                  <div className="source-meta">
                                    <strong>Document chunk {source.chunk_index}</strong>
                                    <span className="similarity">
                                      {(source.similarity * 100).toFixed(1)}% match
                                    </span>
                                  </div>

                                  <p>
                                    {isLong && !expanded
                                      ? `${text.slice(0, 330)}...`
                                      : text}
                                  </p>

                                  {isLong && (
                                    <button
                                      className="show-more"
                                      onClick={() => toggleSource(message.id, index)}
                                    >
                                      {expanded ? "Show less ↑" : "Show more ↓"}
                                    </button>
                                  )}
                                </div>
                              </div>
                            );
                          })}
                        </div>
                      )}
                    </div>
                  </div>
                )
              )}

              {asking && (
                <div className="chat-row ai-row">
                  <div className="ai-avatar small">✦</div>
                  <div className="thinking-bubble">
                    <span className="thinking-dot" />
                    <span className="thinking-dot" />
                    <span className="thinking-dot" />
                    <span>AI is thinking...</span>
                  </div>
                </div>
              )}
            </div>
          )}

          <div className="question-box">
            <textarea
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              onKeyDown={(e) => {
                if ((e.ctrlKey || e.metaKey) && e.key === "Enter") {
                  askQuestion();
                }
              }}
              placeholder={
                documentId
                  ? "Ask another question about your document..."
                  : "Upload a document first to start asking questions..."
              }
              rows={3}
              disabled={!documentId || asking}
            />

            <button
              className="ask-button"
              onClick={askQuestion}
              disabled={asking || !documentId || !question.trim()}
            >
              {asking ? (
                <>
                  <span className="spinner dark" /> Thinking...
                </>
              ) : (
                <>Ask AI <span>↗</span></>
              )}
            </button>
          </div>

          {documentId && (
            <div className="shortcut">Tip: Press Ctrl + Enter to ask</div>
          )}
        </section>

        {error && (
          <div className="error-box">
            <span className="error-icon">!</span>
            <div>
              <strong>Something went wrong</strong>
              <span>{error}</span>
            </div>
          </div>
        )}

        {documentId && (
          <button className="new-document-button" onClick={resetDocument}>
            Start with another document <span>→</span>
          </button>
        )}

        <div className="trust-row">
          <span>Built with</span>
          <strong>React</strong>
          <span>•</span>
          <strong>FastAPI</strong>
          <span>•</span>
          <strong>Google Cloud</strong>
          <span>•</span>
          <strong>Gemini</strong>
        </div>
      </main>

      <footer>
        <span>AI Document Q&A</span>
        <span>Built for intelligent document search.</span>
      </footer>
    </div>
  );
}

export default App;
