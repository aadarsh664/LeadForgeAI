import { 
  LayoutDashboard, 
  Briefcase, 
  Building2, 
  Users, 
  Megaphone, 
  Workflow, 
  Bot, 
  Download, 
  Settings, 
  Code 
} from "lucide-react";
import { useNavigation, navigateTo, PageId } from "../../store/navigation";

interface SidebarProps {
  mode: "user" | "developer";
}

export default function Sidebar({ mode }: SidebarProps) {
  const { currentPage } = useNavigation();

  const navItems: { id: PageId; label: string; icon: React.ReactNode; hidden?: boolean }[] = [
    { id: "dashboard", label: "Dashboard", icon: <LayoutDashboard size={20} /> },
    { id: "workspace", label: "Workspace", icon: <Briefcase size={20} /> },
    { id: "businesses", label: "Businesses", icon: <Building2 size={20} /> },
    { id: "people", label: "People", icon: <Users size={20} /> },
    { id: "campaigns", label: "Campaigns", icon: <Megaphone size={20} /> },
    { id: "automation", label: "Automation", icon: <Workflow size={20} /> },
    { id: "ai", label: "AI", icon: <Bot size={20} /> },
    { id: "exports", label: "Exports", icon: <Download size={20} /> },
    { id: "settings", label: "Settings", icon: <Settings size={20} /> },
    { id: "developer", label: "Developer", icon: <Code size={20} />, hidden: mode !== "developer" },
  ];

  return (
    <aside className="sidebar">
      <nav className="sidebar-nav">
        {navItems.filter(i => !i.hidden).map(item => (
          <button
            key={item.id}
            className={`sidebar-item ${currentPage === item.id ? "active" : ""}`}
            onClick={() => navigateTo(item.id)}
            title={item.label}
          >
            <div className="sidebar-icon">{item.icon}</div>
            <span className="sidebar-label">{item.label}</span>
          </button>
        ))}
      </nav>
    </aside>
  );
}
