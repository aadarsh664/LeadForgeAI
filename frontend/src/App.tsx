import { useState } from "react";
import type { HealthResponse } from "./types/health";

type RequestState = "idle" | "checking" | "completed" | "error";

const DEFAULT_MESSAGE = "Press the button to verify backend connectivity.";

async function fetchHealthStatus(): Promise<HealthResponse> {
  const response = await fetch("http://localhost:8000/api/v1/health");

  if (!response.ok) {
    throw new Error(`Health check request failed: ${response.statusText}`);
  }

  return (await response.json()) as HealthResponse;
}

function App() {
  const [requestState, setRequestState] = useState<RequestState>("idle");
  const [healthData, setHealthData] = useState<HealthResponse | null>(null);
  const [statusMessage, setStatusMessage] = useState(DEFAULT_MESSAGE);

  const handleHealthCheck = async () => {
    try {
      setRequestState("checking");
      setStatusMessage("Checking system health...");

      const health = await fetchHealthStatus();

      setRequestState("completed");
      setHealthData(health);
      setStatusMessage(
        health.overall_status === "healthy"
          ? `${health.application} system is fully healthy.`
          : `${health.application} system has issues.`
      );
    } catch (error) {
      setRequestState("error");
      setHealthData(null);
      setStatusMessage(
        error instanceof Error
          ? error.message
          : "Unable to connect to the backend."
      );
    }
  };

  return (
    <main className="app-shell">
      <section className="status-card">
        <p className="eyebrow">Lead Intelligence Platform</p>
        <h1>{healthData ? healthData.application : "LeadForgeAI"}</h1>
        <p className="subtitle">Desktop Bootstrap</p>

        <dl className="status-list">
          <div className="status-row">
            <dt>Application Version</dt>
            <dd>{healthData?.version || "Unknown"}</dd>
          </div>
          <div className="status-row">
            <dt>Backend Status</dt>
            <dd>{healthData?.backend || "Not checked"}</dd>
          </div>
          <div className="status-row">
            <dt>Database Status</dt>
            <dd>{healthData?.database || "Not checked"}</dd>
          </div>
          <div className="status-row">
            <dt>Docker Status</dt>
            <dd>{healthData?.docker || "Not checked"}</dd>
          </div>
          <div className="status-row">
            <dt>n8n Status</dt>
            <dd>{healthData?.n8n || "Not checked"}</dd>
          </div>
          <div className="status-row">
            <dt>Overall Status</dt>
            <dd>{healthData?.overall_status || "Unknown"}</dd>
          </div>
        </dl>

        <button
          className="primary-button"
          onClick={handleHealthCheck}
          type="button"
          disabled={requestState === "checking"}
        >
          {requestState === "checking" ? "Checking..." : "Refresh Status"}
        </button>

        <p
          className={`feedback ${
            requestState === "error"
              ? "feedback-error"
              : "feedback-neutral"
          }`}
        >
          {statusMessage}
        </p>
      </section>
    </main>
  );
}

export default App;
