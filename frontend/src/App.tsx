import { useState } from "react";

import type { HealthResponse } from "./types/health";

type RequestState = "idle" | "checking" | "healthy" | "error";

const DEFAULT_MESSAGE = "Press the button to verify backend connectivity.";

async function fetchHealthStatus(): Promise<HealthResponse> {
  const response = await fetch("/health");

  if (!response.ok) {
    throw new Error("Health check request failed.");
  }

  return (await response.json()) as HealthResponse;
}

function App() {
  const [requestState, setRequestState] = useState<RequestState>("idle");
  const [backendStatus, setBackendStatus] = useState("Not checked");
  const [statusMessage, setStatusMessage] = useState(DEFAULT_MESSAGE);

  const handleHealthCheck = async () => {
    try {
      setRequestState("checking");
      setStatusMessage("Checking backend health...");

      const health = await fetchHealthStatus();

      setRequestState("healthy");
      setBackendStatus(health.status);
      setStatusMessage(`${health.application} backend is healthy.`);
    } catch (error) {
      setRequestState("error");
      setBackendStatus("Unavailable");
      setStatusMessage(
        error instanceof Error
          ? error.message
          : "Unable to connect to the backend.",
      );
    }
  };

  return (
    <main className="app-shell">
      <section className="status-card">
        <p className="eyebrow">Lead Intelligence Platform</p>
        <h1>LeadForgeAI</h1>
        <p className="subtitle">Application Bootstrapped</p>

        <dl className="status-list">
          <div className="status-row">
            <dt>Application Status</dt>
            <dd>Ready</dd>
          </div>
          <div className="status-row">
            <dt>Backend Status</dt>
            <dd>{backendStatus}</dd>
          </div>
        </dl>

        <button
          className="primary-button"
          onClick={handleHealthCheck}
          type="button"
          disabled={requestState === "checking"}
        >
          {requestState === "checking" ? "Checking..." : "Health Check Button"}
        </button>

        <p
          className={`feedback ${
            requestState === "error" ? "feedback-error" : "feedback-neutral"
          }`}
        >
          {statusMessage}
        </p>
      </section>
    </main>
  );
}

export default App;
