import { useState, useEffect } from "react";
import type { HealthResponse } from "../../../types/health";

interface StatusBarProps {
  mode: "user" | "developer";
}

export default function StatusBar({ mode }: StatusBarProps) {
  const [time, setTime] = useState(new Date().toLocaleTimeString());
  const [health, setHealth] = useState<HealthResponse | null>(null);

  useEffect(() => {
    const timer = setInterval(() => setTime(new Date().toLocaleTimeString()), 1000);
    return () => clearInterval(timer);
  }, []);

  useEffect(() => {
    fetch("http://localhost:8000/api/v1/health")
      .then(res => res.json())
      .then(data => setHealth(data))
      .catch(() => setHealth(null));
  }, []);

  return (
    <footer className="status-bar">
      <div className="status-left">
        <span>v1.0.0</span>
        <span className="status-divider">|</span>
        <span className="mode-indicator">{mode === "developer" ? "Developer Mode" : "User Mode"}</span>
      </div>
      
      <div className="status-right">
        {mode === "developer" && health && (
          <>
            <span className={`connection-status ${health.backend === "connected" ? "ok" : "error"}`}>
              Backend: {health.backend}
            </span>
            <span className="status-divider">|</span>
          </>
        )}
        <span className={`connection-status ${health?.overall_status === "healthy" ? "ok" : "error"}`}>
          System: {health ? health.overall_status : "offline"}
        </span>
        <span className="status-divider">|</span>
        <span>{time}</span>
      </div>
    </footer>
  );
}
