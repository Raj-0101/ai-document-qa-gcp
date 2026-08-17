import { useState } from "react";
import "./App.css";

const API_URL = "https://ai-document-qa-backend-104102848745.asia-south1.run.app";

function App() {
  const [file, setFile] = useState(null);
  const [documentId, setDocumentId] = useState("");
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [sources, setSources] = useState([]);
  const [uploading, setUploading] = useState(false);
  const [asking, setAsking] = useState(false);
  const [error, setError] = useState("");

  const uploadFile = async () => {
    if (!file) {
      setError("Please select a PDF first.");
      return;
    }

    setUploading(true);
    setError("");
    setAnswer("");
    setSources("");

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
    if (!documentId) {
      setError("Please upload a PDF first.");
      return;
    }

    if (!question.trim()) {
      setError("Please enter a question.");
      return;
    }

    setAsking(true);
    setError("");
    setAnswer("");
    setSources([]);

    try {
      const response = await fetch(`${API_URL}/api/ask`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          document_id: documentId,
          question,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Failed to get answer.");
      }

      setAnswer(data.answer);
      setSources(data.sources || []);
    } catch (err) {
      setError(err.message);
    } finally {
      setAsking(false);
    }
  };

  const resetDocument = () => {
    setFile(null);
    setDocumentId("");
    setQuestion("");
    setAnswer("");
    setSources([]);
    setError("");
  };

  return (
    <div className="app">
      <header className="header">
        <div className="logo">📄 AI Document Q&A</div>
        <div className="badge">Powered by Gemini</div>
      </header>

      <main className="container">
        <section className="hero">
          <h1>Chat with your documents</h1>
          <p>
            Upload a PDF and ask questions. AI finds the relevant information
            and gives you an answer.
          </p>
        </section>

        <section className="card">
          <div className="section-title">
            <span className="step">1</span>
            <div>
              <h2>Upload your document</h2>
              <p>Only PDF files are supported.</p>
            </div>
          </div>

          <div className="upload-area">
            <input
              id="file-input"
              type="file"
              accept=".pdf"
              onChange={(e) => setFile(e.target.files[0])}
            />

            <label htmlFor="file-input" className="file-label">
              <span className="upload-icon">☁️</span>
              <strong>
                {file ? file.name : "Choose a PDF file"}
              </strong>
              <span>
                {file
                  ? "Ready to upload"
                  : "Click here to select your document"}
              </span>
            </label>
          </div>

          <button
            className="primary-button"
            onClick={uploadFile}
            disabled={uploading || !file}
          >
            {uploading ? "Uploading..." : "Upload PDF"}
          </button>

          {documentId && (
            <div className="success-box">
              <span>✓</span>
              Document uploaded successfully
            </div>
          )}
        </section>

        <section className="card">
          <div className="section-title">
            <span className="step">2</span>
            <div>
              <h2>Ask a question</h2>
              <p>Ask anything about your uploaded document.</p>
            </div>
          </div>

          <textarea
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            placeholder="Example: What is the CGPA of the student?"
            rows={4}
            disabled={!documentId}
          />

          <button
            className="primary-button"
            onClick={askQuestion}
            disabled={asking || !documentId || !question.trim()}
          >
            {asking ? "Finding answer..." : "Ask Question →"}
          </button>
        </section>

        {error && <div className="error-box">⚠️ {error}</div>}

        {answer && (
          <section className="card answer-card">
            <div className="answer-header">
              <div>
                <span className="answer-label">AI ANSWER</span>
                <h2>🤖 Here's what I found</h2>
              </div>
            </div>

            <div className="answer">
              {answer}
            </div>

            {sources.length > 0 && (
              <div className="sources">
                <h3>📚 Sources</h3>

                {sources.map((source) => (
                  <div className="source" key={source.chunk_index}>
                    <div>
                      <strong>Chunk {source.chunk_index}</strong>
                      <p>{source.text}</p>
                    </div>

                    <span className="similarity">
                      {(source.similarity * 100).toFixed(1)}% match
                    </span>
                  </div>
                ))}
              </div>
            )}
          </section>
        )}

        {documentId && (
          <button className="reset-button" onClick={resetDocument}>
            ↻ Upload another document
          </button>
        )}
      </main>

      <footer>
        AI Document Q&A • FastAPI + React + Google Cloud + Gemini
      </footer>
    </div>
  );
}

export default App;