import { useState, useEffect } from "react";
import type { StartupStatusResponse } from "./types/system";

function App() {
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
    
    return () => {
      if (interval) clearInterval(interval);
    };
  }, [isChecking]);

  const handleStart = async () => {
    try {
      setIsChecking(true);
      const res = await fetch("http://localhost:8000/api/v1/system/startup", {
        method: "POST"
      });
      if (!res.ok) {
        setIsChecking(false);
        setStatus(prev => ({...prev, overall_status: "failed", message: "Failed to initiate startup sequence."}));
      }
    } catch (error) {
      setIsChecking(false);
      setStatus(prev => ({...prev, overall_status: "failed", message: "Network error. Backend unreachable."}));
    }
  };

  const allSteps = ["Backend", "Database", "Docker", "n8n", "Workspace", "Ready"];

  if (status.is_ready) {
    return (
      <main className="app-shell">
        <section className="status-card" style={{ textAlign: "center" }}>
          <div className="icon-success">✓</div>
          <h1>LeadForgeAI is Ready</h1>
          <p className="subtitle">{status.message}</p>
          <button className="primary-button" type="button">
            Continue
          </button>
        </section>
      </main>
    );
  }

  return (
    <main className="app-shell">
      <section className="status-card">
        <p className="eyebrow">Lead Intelligence Platform</p>
        <h1>LeadForgeAI</h1>
        <p className="subtitle">System Boot</p>

        {status.overall_status === "idle" && !isChecking ? (
          <div style={{ textAlign: "center", margin: "40px 0" }}>
            <button
              className="power-button"
              onClick={handleStart}
              type="button"
            >
              POWER ON
            </button>
          </div>
        ) : (
          <div className="startup-progress">
            <div className="progress-bar-container">
              <div 
                className="progress-bar-fill" 
                style={{ width: `${status.progress_percentage}%` }}
              ></div>
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
                <button
                  className="primary-button"
                  onClick={handleStart}
                  type="button"
                >
                  Retry Startup
                </button>
              </div>
            )}
          </div>
        )}
      </section>
    </main>
  );
}

export default App;
