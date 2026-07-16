import Sidebar from "./Sidebar";
import TopBar from "./TopBar";
import StatusBar from "./StatusBar";
import { useNavigation } from "../../store/navigation";

// Import pages
import DashboardPage from "../../pages/DashboardPage";
import WorkspacePage from "../../pages/WorkspacePage";
import BusinessPage from "../../pages/BusinessPage";
import PeoplePage from "../../pages/PeoplePage";
import CampaignPage from "../../pages/CampaignPage";
import AutomationPage from "../../pages/AutomationPage";
import AIPage from "../../pages/AIPage";
import ExportPage from "../../pages/ExportPage";
import SettingsPage from "../../pages/SettingsPage";
import DeveloperPage from "../../pages/DeveloperPage";

interface AppLayoutProps {
  mode: "user" | "developer";
}

export default function AppLayout({ mode }: AppLayoutProps) {
  const { currentPage } = useNavigation();

  const renderPage = () => {
    switch (currentPage) {
      case "dashboard": return <DashboardPage />;
      case "workspace": return <WorkspacePage />;
      case "businesses": return <BusinessPage />;
      case "people": return <PeoplePage />;
      case "campaigns": return <CampaignPage />;
      case "automation": return <AutomationPage />;
      case "ai": return <AIPage />;
      case "exports": return <ExportPage />;
      case "settings": return <SettingsPage />;
      case "developer": return <DeveloperPage />;
      default: return <DashboardPage />;
    }
  };

  return (
    <div className="app-layout-container">
      <TopBar mode={mode} />
      <div className="app-layout-body">
        <Sidebar mode={mode} />
        <main className="app-main-content">
          {renderPage()}
        </main>
      </div>
      <StatusBar mode={mode} />
    </div>
  );
}
