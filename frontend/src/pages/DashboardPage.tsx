import { useEffect, useState } from "react";
import { 
  Card, 
  H2, 
  H3, 
  Text, 
  Badge, 
  Button, 
  PageHeader, 
  SectionHeader, 
  Divider,
  Avatar
} from "../design-system/components";
import { 
  Building2, 
  Users, 
  Megaphone, 
  Workflow, 
  Bot, 
  Upload, 
  Download, 
  Settings, 
  CheckCircle2, 
  XCircle,
  Activity,
  Calendar,
  Search
} from "lucide-react";
import type { HealthResponse } from "../../src/types/health";

export default function DashboardPage() {
  const [health, setHealth] = useState<HealthResponse | null>(null);

  useEffect(() => {
    fetch("http://localhost:8000/api/v1/health")
      .then(res => res.json())
      .then(data => setHealth(data))
      .catch(console.error);
  }, []);

  const quickActions = [
    { label: "Search Businesses", icon: <Building2 size={20} />, color: "#3b82f6" },
    { label: "Search People", icon: <Users size={20} />, color: "#8b5cf6" },
    { label: "New Campaign", icon: <Megaphone size={20} />, color: "#10b981" },
    { label: "Automation", icon: <Workflow size={20} />, color: "#f59e0b" },
    { label: "AI Assistant", icon: <Bot size={20} />, color: "#ec4899" },
    { label: "Import", icon: <Upload size={20} />, color: "#6b7280" },
    { label: "Export", icon: <Download size={20} />, color: "#6b7280" },
    { label: "Settings", icon: <Settings size={20} />, color: "#4b5563" },
  ];

  return (
    <div className="page-container" style={{ padding: "0 16px 64px 16px" }}>
      <PageHeader 
        title="Dashboard" 
        description="Overview of your workspace and recent activity."
        action={<Button variant="primary">New Campaign</Button>}
      />

      <div style={{ display: "grid", gridTemplateColumns: "1fr 300px", gap: "32px", alignItems: "start" }}>
        
        {/* Main Content Column */}
        <div style={{ display: "flex", flexDirection: "column", gap: "32px" }}>
          
          {/* Welcome & Workspace Overview */}
          <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "24px" }}>
            <Card style={{ background: "var(--color-bg-subtle)", border: "1px solid var(--color-border-default)" }}>
              <div style={{ display: "flex", gap: "16px", alignItems: "center", marginBottom: "24px" }}>
                <Avatar fallback="A" size={48} />
                <div>
                  <H2 style={{ margin: 0, fontSize: "1.25rem" }}>Welcome back, Aadarsh</H2>
                  <Text style={{ margin: 0 }}>Ready to generate some leads?</Text>
                </div>
              </div>
              <div style={{ display: "flex", gap: "12px" }}>
                <Badge variant="success">Pro Plan</Badge>
                <Badge>Credits: 4,500</Badge>
              </div>
            </Card>

            <Card>
              <H3 style={{ fontSize: "1rem", marginBottom: "16px", color: "var(--color-text-secondary)" }}>Workspace Overview</H3>
              <div style={{ display: "flex", flexDirection: "column", gap: "16px" }}>
                <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                  <span style={{ fontWeight: 500 }}>Default Workspace</span>
                  <Badge variant="success">Active</Badge>
                </div>
                <Divider style={{ margin: "4px 0" }} />
                <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "16px" }}>
                  <div>
                    <Text style={{ fontSize: "0.75rem", margin: "0 0 4px 0" }}>Total Businesses</Text>
                    <div style={{ fontSize: "1.5rem", fontWeight: 700 }}>1,204</div>
                  </div>
                  <div>
                    <Text style={{ fontSize: "0.75rem", margin: "0 0 4px 0" }}>Active Campaigns</Text>
                    <div style={{ fontSize: "1.5rem", fontWeight: 700 }}>3</div>
                  </div>
                </div>
              </div>
            </Card>
          </div>

          {/* Quick Actions */}
          <section>
            <SectionHeader title="Quick Actions" />
            <div style={{ display: "grid", gridTemplateColumns: "repeat(4, 1fr)", gap: "16px" }}>
              {quickActions.map((action, i) => (
                <button 
                  key={i}
                  style={{
                    display: "flex",
                    flexDirection: "column",
                    alignItems: "center",
                    justifyContent: "center",
                    gap: "12px",
                    padding: "24px 16px",
                    backgroundColor: "var(--color-bg-base)",
                    border: "1px solid var(--color-border-subtle)",
                    borderRadius: "var(--radius-lg)",
                    cursor: "pointer",
                    transition: "all var(--transition-fast)",
                    boxShadow: "var(--shadow-sm)"
                  }}
                  onMouseOver={(e) => {
                    e.currentTarget.style.transform = "translateY(-2px)";
                    e.currentTarget.style.borderColor = "var(--color-border-strong)";
                    e.currentTarget.style.boxShadow = "var(--shadow-md)";
                  }}
                  onMouseOut={(e) => {
                    e.currentTarget.style.transform = "none";
                    e.currentTarget.style.borderColor = "var(--color-border-subtle)";
                    e.currentTarget.style.boxShadow = "var(--shadow-sm)";
                  }}
                >
                  <div style={{ color: action.color, backgroundColor: "var(--color-bg-subtle)", padding: "12px", borderRadius: "50%" }}>
                    {action.icon}
                  </div>
                  <span style={{ fontSize: "0.85rem", fontWeight: 500, color: "var(--color-text-primary)" }}>{action.label}</span>
                </button>
              ))}
            </div>
          </section>

          {/* Activity & Tasks */}
          <div style={{ display: "grid", gridTemplateColumns: "2fr 1fr", gap: "24px" }}>
            <Card>
              <SectionHeader title="Recent Activity" />
              <div style={{ display: "flex", flexDirection: "column", gap: "16px" }}>
                {[1, 2, 3].map(i => (
                  <div key={i} style={{ display: "flex", gap: "16px", alignItems: "flex-start" }}>
                    <div style={{ background: "var(--color-bg-subtle)", padding: "8px", borderRadius: "50%", color: "var(--color-text-secondary)" }}>
                      <Activity size={16} />
                    </div>
                    <div style={{ flex: 1 }}>
                      <p style={{ margin: "0 0 4px 0", fontSize: "0.9rem", fontWeight: 500 }}>Campaign "Q3 Tech Outreach" started</p>
                      <p style={{ margin: 0, fontSize: "0.8rem", color: "var(--color-text-tertiary)" }}>2 hours ago</p>
                    </div>
                  </div>
                ))}
              </div>
            </Card>

            <Card>
              <SectionHeader title="Upcoming Tasks" />
              <div style={{ display: "flex", flexDirection: "column", gap: "16px" }}>
                <div style={{ display: "flex", gap: "12px", alignItems: "center" }}>
                  <Calendar size={16} color="var(--color-text-tertiary)" />
                  <span style={{ fontSize: "0.85rem" }}>Review 45 new leads</span>
                </div>
                <div style={{ display: "flex", gap: "12px", alignItems: "center" }}>
                  <Calendar size={16} color="var(--color-text-tertiary)" />
                  <span style={{ fontSize: "0.85rem" }}>Update email templates</span>
                </div>
              </div>
            </Card>
          </div>

        </div>
        
        {/* Sidebar Column */}
        <div style={{ display: "flex", flexDirection: "column", gap: "24px" }}>
          
          <Card>
            <SectionHeader title="System Status" />
            
            {health ? (
              <div style={{ display: "flex", flexDirection: "column", gap: "16px", fontFamily: "var(--font-family-mono)", fontSize: "0.8rem" }}>
                
                <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                  <span style={{ color: "var(--color-text-secondary)" }}>Global</span>
                  {health.overall_status === "healthy" ? <CheckCircle2 size={16} color="var(--color-success)"/> : <XCircle size={16} color="var(--color-danger)"/>}
                </div>
                
                <Divider style={{ margin: 0 }} />
                
                <div style={{ display: "flex", justifyContent: "space-between" }}>
                  <span>Backend</span>
                  <span style={{ color: health.backend === "connected" ? "var(--color-success)" : "var(--color-danger)" }}>
                    {health.backend}
                  </span>
                </div>
                
                <div style={{ display: "flex", justifyContent: "space-between" }}>
                  <span>Database</span>
                  <span style={{ color: health.database === "connected" ? "var(--color-success)" : "var(--color-danger)" }}>
                    {health.database}
                  </span>
                </div>
                
                <div style={{ display: "flex", justifyContent: "space-between" }}>
                  <span>Docker</span>
                  <span style={{ color: health.docker === "connected" ? "var(--color-success)" : "var(--color-danger)" }}>
                    {health.docker}
                  </span>
                </div>
                
                <div style={{ display: "flex", justifyContent: "space-between" }}>
                  <span>n8n</span>
                  <span style={{ color: health.n8n === "connected" ? "var(--color-success)" : "var(--color-danger)" }}>
                    {health.n8n}
                  </span>
                </div>
                
                <div style={{ display: "flex", justifyContent: "space-between" }}>
                  <span>Workspace</span>
                  <span style={{ color: "var(--color-success)" }}>
                    connected
                  </span>
                </div>
                
                <Divider style={{ margin: 0 }} />
                
                <div style={{ display: "flex", justifyContent: "space-between", color: "var(--color-text-tertiary)" }}>
                  <span>Version</span>
                  <span>{health.version}</span>
                </div>
              </div>
            ) : (
              <Text>Loading status...</Text>
            )}
          </Card>

          <Card>
            <SectionHeader title="Recent Searches" />
            <div style={{ display: "flex", flexDirection: "column", gap: "12px" }}>
              {["Software companies in NY", "Marketing agencies UK", "CEO at tech startups"].map((search, i) => (
                <div key={i} style={{ display: "flex", gap: "8px", alignItems: "center", color: "var(--color-text-secondary)", fontSize: "0.85rem" }}>
                  <Search size={14} />
                  <span>{search}</span>
                </div>
              ))}
            </div>
          </Card>

        </div>
      </div>
    </div>
  );
}
