import React, { useState, useEffect } from "react";
import { 
  Card, Button, H2, H3, Text, Divider, Badge, Input, SectionHeader 
} from "../design-system/components";
import { 
  ArrowLeft, Clock, Bookmark, Search, Trash2, Play, Copy, Star, MapPin 
} from "lucide-react";

interface SearchHistoryProps {
  onBack: () => void;
  onRunSearch: (request: any) => void;
}

export default function SearchHistory({ onBack, onRunSearch }: SearchHistoryProps) {
  const [activeTab, setActiveTab] = useState<"recent" | "saved">("recent");
  const [recent, setRecent] = useState<any[]>([]);
  const [saved, setSaved] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  const fetchData = async () => {
    setLoading(true);
    try {
      const [histRes, savedRes] = await Promise.all([
        fetch("http://localhost:8000/api/v1/history/history"),
        fetch("http://localhost:8000/api/v1/history/saved")
      ]);
      setRecent(await histRes.json());
      setSaved(await savedRes.json());
    } catch (e) {
      console.error("Failed to load history", e);
    }
    setLoading(false);
  };

  useEffect(() => {
    fetchData();
  }, []);

  const handleDeleteHistory = async (id: string) => {
    await fetch(`http://localhost:8000/api/v1/history/history/${id}`, { method: "DELETE" });
    fetchData();
  };

  const handleClearHistory = async () => {
    await fetch("http://localhost:8000/api/v1/history/history", { method: "POST" });
    fetchData();
  };

  const handleDeleteSaved = async (id: string) => {
    await fetch(`http://localhost:8000/api/v1/history/saved/${id}`, { method: "DELETE" });
    fetchData();
  };

  const handleToggleFavorite = async (id: string, current: boolean) => {
    await fetch(`http://localhost:8000/api/v1/history/saved/${id}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ is_favorite: !current })
    });
    fetchData();
  };

  const handleRename = async (id: string, currentName: string) => {
    const newName = prompt("Rename search:", currentName);
    if (newName && newName !== currentName) {
      const res = await fetch(`http://localhost:8000/api/v1/history/saved/${id}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name: newName })
      });
      if (!res.ok) alert("Failed to rename, name might be taken.");
      fetchData();
    }
  };

  const runSaved = async (id: string, req: any) => {
    await fetch(`http://localhost:8000/api/v1/history/saved/${id}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ run: true })
    });
    onRunSearch(req);
  };

  return (
    <div style={{ display: "flex", gap: "32px", alignItems: "flex-start" }}>
      
      {/* Sidebar */}
      <div style={{ width: "240px", flexShrink: 0, display: "flex", flexDirection: "column", gap: "16px" }}>
        <Button variant="ghost" onClick={onBack} icon={<ArrowLeft size={16}/>} style={{ alignSelf: "flex-start", marginBottom: "8px" }}>
          Back to Search
        </Button>
        <div style={{ display: "flex", flexDirection: "column", gap: "4px" }}>
          <button 
            style={{ 
              display: "flex", alignItems: "center", gap: "12px", padding: "10px 16px",
              borderRadius: "var(--radius-md)", cursor: "pointer", border: "none",
              background: activeTab === "recent" ? "var(--color-bg-subtle)" : "transparent",
              color: activeTab === "recent" ? "var(--color-text-primary)" : "var(--color-text-secondary)",
              fontWeight: activeTab === "recent" ? 600 : 400, textAlign: "left"
            }}
            onClick={() => setActiveTab("recent")}
          >
            <Clock size={18} /> Recent Searches
          </button>
          <button 
            style={{ 
              display: "flex", alignItems: "center", gap: "12px", padding: "10px 16px",
              borderRadius: "var(--radius-md)", cursor: "pointer", border: "none",
              background: activeTab === "saved" ? "var(--color-bg-subtle)" : "transparent",
              color: activeTab === "saved" ? "var(--color-text-primary)" : "var(--color-text-secondary)",
              fontWeight: activeTab === "saved" ? 600 : 400, textAlign: "left"
            }}
            onClick={() => setActiveTab("saved")}
          >
            <Bookmark size={18} /> Saved Searches
          </button>
        </div>
      </div>

      {/* Main Content */}
      <div style={{ flex: 1, display: "flex", flexDirection: "column", gap: "24px" }}>
        <Card style={{ padding: "24px", display: "flex", justifyContent: "space-between", alignItems: "center" }}>
          <div>
            <H2 style={{ margin: 0 }}>{activeTab === "recent" ? "Recent Searches" : "Saved Searches"}</H2>
            <Text style={{ margin: "4px 0 0 0", color: "var(--color-text-secondary)" }}>
              {activeTab === "recent" ? "Your search history across all providers." : "Your bookmarked and frequent searches."}
            </Text>
          </div>
          {activeTab === "recent" && recent.length > 0 && (
            <Button variant="ghost" onClick={handleClearHistory} icon={<Trash2 size={16}/>}>Clear History</Button>
          )}
        </Card>

        {loading ? (
          <Text>Loading...</Text>
        ) : activeTab === "recent" ? (
          <div style={{ display: "flex", flexDirection: "column", gap: "16px" }}>
            {recent.length === 0 ? (
              <Card style={{ textAlign: "center", padding: "64px" }}>
                <Clock size={48} style={{ margin: "0 auto 16px auto", opacity: 0.2 }} />
                <H3>No Search History</H3>
                <Text style={{ color: "var(--color-text-secondary)" }}>Your recent searches will appear here.</Text>
              </Card>
            ) : (
              recent.map((item) => (
                <Card key={item.id} style={{ display: "flex", justifyContent: "space-between", alignItems: "center", padding: "16px 24px" }}>
                  <div style={{ display: "flex", flexDirection: "column", gap: "8px" }}>
                    <div style={{ display: "flex", alignItems: "center", gap: "12px" }}>
                      <span style={{ fontWeight: 600, fontSize: "1.1rem" }}>{item.request.category}</span>
                      <span style={{ color: "var(--color-text-tertiary)" }}>in</span>
                      <span style={{ display: "flex", alignItems: "center", gap: "4px", color: "var(--color-primary)" }}><MapPin size={14}/> {item.request.location}</span>
                    </div>
                    <div style={{ display: "flex", gap: "16px", fontSize: "0.85rem", color: "var(--color-text-secondary)" }}>
                      <span style={{ display: "flex", alignItems: "center", gap: "4px" }}><Clock size={14}/> {new Date(item.created_at).toLocaleString()}</span>
                      <span style={{ display: "flex", alignItems: "center", gap: "4px" }}><Search size={14}/> {item.result_count} results</span>
                      <Badge variant="default" style={{ zoom: 0.8 }}>{item.provider}</Badge>
                    </div>
                  </div>
                  <div style={{ display: "flex", gap: "8px" }}>
                    <Button variant="ghost" icon={<Play size={16}/>} onClick={() => onRunSearch(item.request)}>Run Again</Button>
                    <Button variant="ghost" icon={<Trash2 size={16}/>} onClick={() => handleDeleteHistory(item.id)} />
                  </div>
                </Card>
              ))
            )}
          </div>
        ) : (
          <div style={{ display: "flex", flexDirection: "column", gap: "16px" }}>
            {saved.length === 0 ? (
              <Card style={{ textAlign: "center", padding: "64px" }}>
                <Bookmark size={48} style={{ margin: "0 auto 16px auto", opacity: 0.2 }} />
                <H3>No Saved Searches</H3>
                <Text style={{ color: "var(--color-text-secondary)" }}>Save frequent searches to access them quickly.</Text>
              </Card>
            ) : (
              saved.map((item) => (
                <Card key={item.id} style={{ display: "flex", justifyContent: "space-between", alignItems: "center", padding: "16px 24px" }}>
                  <div style={{ display: "flex", flexDirection: "column", gap: "8px" }}>
                    <div style={{ display: "flex", alignItems: "center", gap: "12px" }}>
                      <Star 
                        size={18} 
                        fill={item.is_favorite ? "currentColor" : "none"} 
                        color={item.is_favorite ? "#f59e0b" : "var(--color-text-tertiary)"}
                        style={{ cursor: "pointer" }}
                        onClick={() => handleToggleFavorite(item.id, item.is_favorite)}
                      />
                      <span style={{ fontWeight: 600, fontSize: "1.1rem" }}>{item.name}</span>
                    </div>
                    <div style={{ display: "flex", gap: "16px", fontSize: "0.85rem", color: "var(--color-text-secondary)", alignItems: "center" }}>
                      <span>{item.request.category} • {item.request.location}</span>
                      {item.last_used && (
                        <span>Last used: {new Date(item.last_used).toLocaleDateString()}</span>
                      )}
                    </div>
                  </div>
                  <div style={{ display: "flex", gap: "8px" }}>
                    <Button variant="secondary" icon={<Play size={16}/>} onClick={() => runSaved(item.id, item.request)}>Run</Button>
                    <Dropdown 
                      label="More"
                      value=""
                      onChange={(e) => {
                        if (e.target.value === "rename") handleRename(item.id, item.name);
                        if (e.target.value === "delete") handleDeleteSaved(item.id);
                        if (e.target.value === "duplicate") onRunSearch(item.request); // Just load into form
                      }}
                      options={[
                        { label: "Actions...", value: "" },
                        { label: "Rename", value: "rename" },
                        { label: "Edit in Form", value: "duplicate" },
                        { label: "Delete", value: "delete" }
                      ]}
                    />
                  </div>
                </Card>
              ))
            )}
          </div>
        )}
      </div>
    </div>
  );
}
