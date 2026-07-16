import React, { useState, useEffect } from "react";
import { PageHeader, Card, H3, Text, Badge, Divider } from "../design-system/components";
import { Activity, Server, ShieldAlert, Cpu, Settings as SettingsIcon } from "lucide-react";

export default function DeveloperPage() {
  const [diagnostics, setDiagnostics] = useState<any>(null);

  useEffect(() => {
    const fetchDiag = async () => {
      try {
        const res = await fetch("http://localhost:8000/api/v1/diagnostics/diagnostics");
        if (res.ok) {
          setDiagnostics(await res.json());
        }
      } catch(e) {
        console.error(e);
      }
    };
    fetchDiag();
    const int = setInterval(fetchDiag, 2000);
    return () => clearInterval(int);
  }, []);

  return (
    <div className="page-container" style={{ padding: "0 16px 64px 16px" }}>
      <PageHeader 
        title="Developer Diagnostics" 
        description="Monitor provider framework, adapters, and system health."
      />
      
      {!diagnostics ? (
        <Text>Loading diagnostics...</Text>
      ) : (
        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "24px", alignItems: "start" }}>
          
          <Card>
            <div style={{ display: "flex", alignItems: "center", gap: "8px", marginBottom: "16px" }}>
              <Server size={20} color="var(--color-primary)" />
              <H3 style={{ margin: 0 }}>Provider Status</H3>
            </div>
            
            <div style={{ display: "flex", flexDirection: "column", gap: "12px", fontSize: "0.85rem" }}>
              <div style={{ display: "flex", justifyContent: "space-between" }}>
                <span style={{ color: "var(--color-text-secondary)" }}>Active Provider</span>
                <span style={{ fontWeight: 600 }}>{diagnostics.provider} (v{diagnostics.version})</span>
              </div>
              <div style={{ display: "flex", justifyContent: "space-between" }}>
                <span style={{ color: "var(--color-text-secondary)" }}>Capabilities</span>
                <span style={{ fontWeight: 600 }}>{diagnostics.capabilities.join(", ")}</span>
              </div>
              <div style={{ display: "flex", justifyContent: "space-between" }}>
                <span style={{ color: "var(--color-text-secondary)" }}>Health</span>
                <Badge variant={diagnostics.health.status === "Ready" ? "success" : "warning"}>
                  {diagnostics.health.status}
                </Badge>
              </div>
            </div>
          </Card>

          <Card>
            <div style={{ display: "flex", alignItems: "center", gap: "8px", marginBottom: "16px" }}>
              <SettingsIcon size={20} color="var(--color-primary)" />
              <H3 style={{ margin: 0 }}>Framework Config</H3>
            </div>

            <div style={{ display: "flex", flexDirection: "column", gap: "12px", fontSize: "0.85rem" }}>
              <div style={{ display: "flex", justifyContent: "space-between" }}>
                <span style={{ color: "var(--color-text-secondary)" }}>Rate Limit</span>
                <span style={{ fontWeight: 600 }}>{diagnostics.config.rate_limit_rpm} RPM</span>
              </div>
              <div style={{ display: "flex", justifyContent: "space-between" }}>
                <span style={{ color: "var(--color-text-secondary)" }}>Search Delay</span>
                <span style={{ fontWeight: 600 }}>{diagnostics.config.search_delay}s</span>
              </div>
              <div style={{ display: "flex", justifyContent: "space-between" }}>
                <span style={{ color: "var(--color-text-secondary)" }}>Max Retries</span>
                <span style={{ fontWeight: 600 }}>{diagnostics.config.retries}</span>
              </div>
              <div style={{ display: "flex", justifyContent: "space-between" }}>
                <span style={{ color: "var(--color-text-secondary)" }}>Timeout</span>
                <span style={{ fontWeight: 600 }}>{diagnostics.config.timeout}s</span>
              </div>
              <div style={{ display: "flex", justifyContent: "space-between" }}>
                <span style={{ color: "var(--color-text-secondary)" }}>Headless Mode</span>
                <span style={{ fontWeight: 600 }}>{diagnostics.config.headless_mode ? "Enabled" : "Disabled"}</span>
              </div>
            </div>
          </Card>

          <Card style={{ gridColumn: "span 2" }}>
            <div style={{ display: "flex", alignItems: "center", gap: "8px", marginBottom: "16px" }}>
              <Cpu size={20} color="var(--color-primary)" />
              <H3 style={{ margin: 0 }}>Active Adapter & Live Diagnostics</H3>
            </div>
            
            <div style={{ padding: "16px", background: "var(--color-bg-subtle)", borderRadius: "var(--radius-sm)", border: "1px dashed var(--color-border-strong)", marginBottom: "24px" }}>
              <Text style={{ margin: 0, textAlign: "center", color: "var(--color-text-secondary)" }}>
                {diagnostics.adapter === "Connected" ? (
                  <>
                    <span style={{ color: "var(--color-success)", fontWeight: 600 }}>Playwright Adapter</span> - Connected & Ready
                  </>
                ) : (
                  <>
                    <span style={{ color: "var(--color-danger)", fontWeight: 600 }}>Playwright Adapter</span> - {diagnostics.adapter || "Initialization Failed"}
                  </>
                )}
              </Text>
            </div>

            <div style={{ display: "grid", gridTemplateColumns: "repeat(4, 1fr)", gap: "16px", fontSize: "0.85rem" }}>
              <div style={{ display: "flex", flexDirection: "column", gap: "4px" }}>
                <span style={{ color: "var(--color-text-secondary)", fontWeight: 600 }}>Businesses Extracted</span>
                <span style={{ fontSize: "1.2rem", fontWeight: 700, color: "var(--color-primary)" }}>{diagnostics.stats?.extracted || "0"}</span>
              </div>
              <div style={{ display: "flex", flexDirection: "column", gap: "4px" }}>
                <span style={{ color: "var(--color-text-secondary)", fontWeight: 600 }}>Duplicate Count</span>
                <span style={{ fontSize: "1.2rem", fontWeight: 700 }}>{diagnostics.stats?.duplicates || "0"}</span>
              </div>
              <div style={{ display: "flex", flexDirection: "column", gap: "4px" }}>
                <span style={{ color: "var(--color-text-secondary)", fontWeight: 600 }}>Current Scroll</span>
                <span style={{ fontSize: "1.2rem", fontWeight: 700 }}>{diagnostics.stats?.scroll || "0"}px</span>
              </div>
              <div style={{ display: "flex", flexDirection: "column", gap: "4px" }}>
                <span style={{ color: "var(--color-text-secondary)", fontWeight: 600 }}>Pages Loaded</span>
                <span style={{ fontSize: "1.2rem", fontWeight: 700 }}>{diagnostics.stats?.pages || "0"}</span>
              </div>
              <div style={{ display: "flex", flexDirection: "column", gap: "4px" }}>
                <span style={{ color: "var(--color-text-secondary)", fontWeight: 600 }}>Extraction Speed</span>
                <span style={{ fontSize: "1.2rem", fontWeight: 700, color: "var(--color-success)" }}>{diagnostics.stats?.speed || "0"} ms/biz</span>
              </div>
              <div style={{ display: "flex", flexDirection: "column", gap: "4px" }}>
                <span style={{ color: "var(--color-text-secondary)", fontWeight: 600 }}>Businesses Per Minute</span>
                <span style={{ fontSize: "1.2rem", fontWeight: 700 }}>{diagnostics.stats?.bpm || "0"} BPM</span>
              </div>
              <div style={{ display: "flex", flexDirection: "column", gap: "4px" }}>
                <span style={{ color: "var(--color-text-secondary)", fontWeight: 600 }}>Memory Usage</span>
                <span style={{ fontSize: "1.2rem", fontWeight: 700 }}>{diagnostics.stats?.memory || "142 MB"}</span>
              </div>
              <div style={{ display: "flex", flexDirection: "column", gap: "4px" }}>
                <span style={{ color: "var(--color-text-secondary)", fontWeight: 600 }}>Browser Status</span>
                <Badge variant={diagnostics.adapter === "Connected" ? "success" : "danger"} style={{ width: "fit-content" }}>
                  {diagnostics.adapter === "Connected" ? "Active" : "Closed"}
                </Badge>
              </div>
            </div>
          </Card>

        </div>
      )}
    </div>
  );
}
