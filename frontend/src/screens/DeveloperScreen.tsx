import { useState, useEffect } from "react";
import type { StartupStatusResponse } from "../types/system";

export default function DeveloperScreen() {
  const [status, setStatus] = useState<StartupStatusResponse>({
    current_step: "idle",
    completed_steps: [],
    progress_percentage: 0,
    overall_status: "idle",
    is_ready: false,
    message: "Ready to start.",
  });
  const [isChecking, setIsChecking] = useState(false);
  const [logs, setLogs] = useState<string[]>([]);

  useEffect(() => {
    let interval: ReturnType<typeof setInterval>;
    if (isChecking) {
      interval = setInterval(async () => {
        try {
          const res = await fetch("http://localhost:8000/api/v1/system/startup/status");
          if (res.ok) {
            const data: StartupStatusResponse = await res.json();
            setStatus(prev => {
                if (prev.message !== data.message) {
                    setLogs(l => [...l, `[${new Date().toISOString()}] ${data.message}`]);
                }
                return data;
            });
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
      setLogs(["Initializing Developer Startup Sequence..."]);
      const res = await fetch("http://localhost:8000/api/v1/system/startup", { method: "POST" });
      if (!res.ok) {
        setIsChecking(false);
        setStatus(prev => ({...prev, overall_status: "failed", message: "Failed to initiate."}));
      }
    } catch (error) {
      setIsChecking(false);
      setStatus(prev => ({...prev, overall_status: "failed", message: "Network error."}));
    }
  };

  const allSteps = ["Backend", "Database", "Docker", "n8n", "Workspace", "Ready"];

  return (
    <main className="app-shell dev-mode">
      <section className="status-card" style={{ maxWidth: "800px", width: "100%" }}>
        <p className="eyebrow">Developer Mode</p>
        <h1>System Boot Controller</h1>
        <p className="subtitle">Detailed technical diagnostics</p>

        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "32px", marginTop: "32px" }}>
            <div>
                {status.overall_status === "idle" && !isChecking ? (
                <div style={{ margin: "24px 0", textAlign: "center" }}>
                    <button className="power-button" onClick={handleStart} type="button">
                    POWER ON
                    </button>
                </div>
                ) : (
                <div className="startup-progress">
                    <div className="progress-bar-container">
                    <div className="progress-bar-fill" style={{ width: `${status.progress_percentage}%` }}></div>
                    </div>
                    
                    <p className="current-message">{status.message}</p>
                    
                    <ul className="step-list">
                    {allSteps.map(step => {
                        const isCompleted = status.completed_steps.includes(step) || (status.is_ready && step === "Ready");
                        const isCurrent = status.current_step === step && status.overall_status === "running";
                        const isFailed = status.current_step === step && status.overall_status === "failed";
                        
                        let icon = "○";
                        let className = "step-pending";
                        
                        if (isCompleted) {
                        icon = "✓";
                        className = "step-completed";
                        } else if (isFailed) {
                        icon = "✗";
                        className = "step-failed";
                        } else if (isCurrent) {
                        icon = "↻";
                        className = "step-running";
                        }
                        
                        return (
                        <li key={step} className={`step-item ${className}`}>
                            <span className="step-icon">{icon}</span> {step}
                        </li>
                        );
                    })}
                    </ul>

                    {status.overall_status === "failed" && (
                    <div style={{ marginTop: "24px", textAlign: "center" }}>
                        <button className="primary-button" onClick={handleStart} type="button">
                        Retry Startup
                        </button>
                    </div>
                    )}
                    
                    {status.is_ready && (
                        <div style={{ marginTop: "24px", textAlign: "center" }}>
                            <button className="primary-button" type="button">
                            Continue
                            </button>
                        </div>
                    )}
                </div>
                )}
            </div>
            
            <div style={{ background: "#1f2937", borderRadius: "12px", padding: "16px", color: "#d1d5db", fontFamily: "JetBrains Mono, monospace", fontSize: "0.85rem", overflowY: "auto", maxHeight: "400px" }}>
                <h4 style={{ color: "#9ca3af", margin: "0 0 12px 0", textTransform: "uppercase", fontSize: "0.75rem", letterSpacing: "0.05em" }}>Startup Logs</h4>
                {logs.length === 0 ? (
                    <p style={{ opacity: 0.5 }}>No logs generated yet...</p>
                ) : (
                    logs.map((log, i) => (
                        <div key={i} style={{ marginBottom: "6px", wordBreak: "break-all" }}>{log}</div>
                    ))
                )}
            </div>
        </div>
      </section>
    </main>
  );
}
