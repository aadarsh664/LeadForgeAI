import { Search, UserCircle } from "lucide-react";

interface TopBarProps {
  mode: "user" | "developer";
}

export default function TopBar({ mode }: TopBarProps) {
  return (
    <header className="top-bar">
      <div className="top-bar-left">
        <div className="app-logo">
          <span className="logo-icon">forge</span>
          <span className="app-name">LeadForgeAI</span>
        </div>
        <div className="workspace-selector">
          <span className="workspace-name">Default Workspace</span>
        </div>
      </div>
      
      <div className="top-bar-center">
        <div className="search-placeholder">
          <Search size={16} />
          <span>Search...</span>
        </div>
      </div>

      <div className="top-bar-right">
        {mode === "developer" && (
          <div className="developer-badge">Developer Mode</div>
        )}
        <div className="profile-placeholder">
          <UserCircle size={24} />
        </div>
      </div>
    </header>
  );
}
