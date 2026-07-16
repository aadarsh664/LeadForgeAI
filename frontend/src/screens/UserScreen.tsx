import { useState, useEffect } from "react";
import type { StartupStatusResponse } from "../types/system";

interface UserScreenProps {
  onEnterApp: () => void;
}

export default function UserScreen({ onEnterApp }: UserScreenProps) {
  const [status, setStatus] = useState<StartupStatusResponse>({
    current_step: "idle",
    completed_steps: [],
    progress_percentage: 0,
    overall_status: "idle",
    is_ready: false,
    message: "Ready to start.",
  });
  const [isChecking, setIsChecking] = useState(false);

  useEffect(() => {
    let interval: ReturnType<typeof setInterval>;
    if (isChecking) {
      interval = setInterval(async () => {
        try {
          const res = await fetch("http://localhost:8000/api/v1/system/startup/status");
          if (res.ok) {
            const data: StartupStatusResponse = await res.json();
            setStatus(data);
            if (data.overall_status === "success" || data.overall_status === "failed") {
              setIsChecking(false);
            }
          }
        } catch (error) {
          console.error("Failed to poll status", error);
        }
      }, 500);
    }
    return () => { if (interval) clearInterval(interval); };
  }, [isChecking]);

  const handleStart = async () => {
    try {
      setIsChecking(true);
      const res = await fetch("http://localhost:8000/api/v1/system/startup", { method: "POST" });
      if (!res.ok) {
        setIsChecking(false);
        setStatus(prev => ({...prev, overall_status: "failed", message: "Failed to initiate startup."}));
      }
    } catch (error) {
      setIsChecking(false);
      setStatus(prev => ({...prev, overall_status: "failed", message: "Network error."}));
    }
  };

  if (status.is_ready) {
    return (
      <main className="app-shell user-mode">
        <section className="status-card" style={{ textAlign: "center", padding: "64px 32px", width: "100%", maxWidth: "600px" }}>
          <h1>LeadForgeAI</h1>
          <p className="subtitle" style={{ color: "#059669", fontWeight: 500 }}>Application Ready</p>
          
          <div style={{ margin: "32px 0", textAlign: "left", background: "#f9fafb", padding: "24px", borderRadius: "12px", border: "1px solid #e5e7eb" }}>
            <h3 style={{ margin: "0 0 8px 0", fontSize: "1rem", color: "#4b5563" }}>Current Workspace</h3>
            <p style={{ margin: 0, fontWeight: 600, fontSize: "1.2rem" }}>Default Workspace</p>
          </div>

          <div style={{ margin: "32px 0", textAlign: "left", background: "#f9fafb", padding: "24px", borderRadius: "12px", border: "1px solid #e5e7eb" }}>
            <h3 style={{ margin: "0 0 16px 0", fontSize: "1rem", color: "#4b5563" }}>Recent Workspaces</h3>
            <ul style={{ margin: 0, padding: "0 0 0 20px", color: "#6b7280", lineHeight: "1.8" }}>
              <li>Acme Corp</li>
              <li>Globex Inc</li>
            </ul>
          </div>
          
          <button className="primary-button" type="button" style={{ width: "100%" }} onClick={onEnterApp}>
            Enter Workspace
          </button>
        </section>
      </main>
    );
  }

  return (
    <main className="app-shell user-mode">
      <section className="status-card" style={{ textAlign: "center", padding: "64px 32px", width: "100%", maxWidth: "600px" }}>
        <h1>LeadForgeAI</h1>
        <p className="subtitle" style={{ marginBottom: "48px" }}>Welcome to your intelligent lead generation platform.</p>

        {status.overall_status === "idle" && !isChecking ? (
          <button className="primary-button" onClick={handleStart} type="button" style={{ padding: "0 48px", height: "56px", fontSize: "1.1rem" }}>
            Start Application
          </button>
        ) : (
          <div className="startup-progress" style={{ maxWidth: "300px", margin: "0 auto" }}>
            <div className="progress-bar-container">
              <div className="progress-bar-fill" style={{ width: `${status.progress_percentage}%` }}></div>
            </div>
            <p className="current-message" style={{ color: "#6b7280", fontWeight: "normal" }}>Loading systems...</p>
            
            {status.overall_status === "failed" && (
              <button className="primary-button" onClick={handleStart} type="button" style={{ marginTop: "16px" }}>
                Retry
              </button>
            )}
          </div>
        )}
      </section>
    </main>
  );
}
