import { useState, useEffect } from "react";
import DeveloperScreen from "./screens/DeveloperScreen";
import UserScreen from "./screens/UserScreen";
import AppLayout from "./components/layout/AppLayout";

function App() {
  const [mode, setMode] = useState<"user" | "developer">("user");
  const [loading, setLoading] = useState(true);
  const [inApp, setInApp] = useState(() => localStorage.getItem("leadforgeai_in_app") === "true");

  useEffect(() => {
    const fetchMode = async () => {
      try {
        const res = await fetch("http://localhost:8000/api/v1/system/mode");
        if (res.ok) {
          const data = await res.json();
          setMode(data.mode);
        }
      } catch (err) {
        console.error("Failed to fetch mode", err);
      } finally {
        setLoading(false);
      }
    };
    fetchMode();
  }, []);

  const handleEnterApp = () => {
    setInApp(true);
    localStorage.setItem("leadforgeai_in_app", "true");
  };

  const toggleMode = async () => {
    const newMode = mode === "user" ? "developer" : "user";
    try {
      await fetch("http://localhost:8000/api/v1/system/mode", {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ mode: newMode })
      });
      setMode(newMode);
    } catch (err) {
      console.error("Failed to update mode", err);
    }
  };

  if (loading) {
    return <main className="app-shell"><p>Loading...</p></main>;
  }

  if (inApp) {
    return (
      <>
        <button 
          onClick={toggleMode} 
          style={{ position: 'fixed', bottom: 48, right: 24, opacity: 0.5, zIndex: 9999, background: "#1f2937", color: "white", border: "none", padding: "8px 16px", borderRadius: "20px", cursor: "pointer", fontSize: "0.85rem", fontWeight: 600 }}
        >
          Switch to {mode === "user" ? "Developer" : "User"} Mode
        </button>
        <AppLayout mode={mode} />
      </>
    );
  }

  return (
    <>
      <button 
        onClick={toggleMode} 
        style={{ position: 'fixed', bottom: 24, right: 24, opacity: 0.5, zIndex: 999, background: "#1f2937", color: "white", border: "none", padding: "8px 16px", borderRadius: "20px", cursor: "pointer", fontSize: "0.85rem", fontWeight: 600 }}
      >
        Switch to {mode === "user" ? "Developer" : "User"} Mode
      </button>
      {mode === "developer" ? (
        <DeveloperScreen onEnterApp={handleEnterApp} />
      ) : (
        <UserScreen onEnterApp={handleEnterApp} />
      )}
    </>
  );
}

export default App;
