import { useState } from "react";
import UploadForm from "./components/UploadForm";
import StatusFeedback from "./components/StatusFeedback";
import { analyzeSalesData } from "./api/client";

export default function App() {
  const [status, setStatus] = useState("idle"); // idle | loading | success | error
  const [summary, setSummary] = useState("");
  const [error, setError] = useState("");
  const [email, setEmail] = useState("");
  const [responseMessage, setResponseMessage] = useState("");

  const handleSubmit = async (file, recipientEmail) => {
    setStatus("loading");
    setError("");
    setSummary("");
    setEmail(recipientEmail);

    try {
      const result = await analyzeSalesData(file, recipientEmail);
      setSummary(result.summary);
      setResponseMessage(result.message);
      setStatus("success");
    } catch (err) {
      setError(err.message || "An unexpected error occurred.");
      setStatus("error");
    }
  };

  const handleReset = () => {
    setStatus("idle");
    setSummary("");
    setResponseMessage("");
    setError("");
    setEmail("");
  };

  return (
    <div className="app">
      {/* Animated background blobs */}
      <div className="bg-blur">
        <div className="blob blob-1" />
        <div className="blob blob-2" />
        <div className="blob blob-3" />
      </div>

      <main className="container">
        {/* Header */}
        <header className="header">
          <div className="logo">
            <svg width="36" height="36" viewBox="0 0 24 24" fill="none" stroke="url(#grad)" strokeWidth="2">
              <defs>
                <linearGradient id="grad" x1="0%" y1="0%" x2="100%" y2="100%">
                  <stop offset="0%" style={{ stopColor: "#818cf8" }} />
                  <stop offset="100%" style={{ stopColor: "#c084fc" }} />
                </linearGradient>
              </defs>
              <path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z" />
              <polyline points="3.27 6.96 12 12.01 20.73 6.96" />
              <line x1="12" y1="22.08" x2="12" y2="12" />
            </svg>
          </div>
          <h1>Sales Insight <span className="gradient-text">Automator</span></h1>
          <p className="tagline">
            Upload your sales data, get an AI-powered executive brief delivered to any inbox in seconds.
          </p>
        </header>

        {/* Card */}
        <div className="card">
          {status === "idle" || status === "loading" ? (
            <UploadForm onSubmit={handleSubmit} isLoading={status === "loading"} />
          ) : (
            <StatusFeedback
              status={status}
              summary={summary}
              message={responseMessage}
              error={error}
              email={email}
              onReset={handleReset}
            />
          )}
        </div>

        {/* Footer */}
        <footer className="footer">
          <p>
            Powered by <strong>Google Gemini</strong>
          </p>
        </footer>
      </main>
    </div>
  );
}
