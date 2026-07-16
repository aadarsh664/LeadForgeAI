import os

pages = [
    ("DashboardPage", "Dashboard", "Overview of your application"),
    ("WorkspacePage", "Workspace", "Manage your current workspace"),
    ("BusinessPage", "Businesses", "Search and manage businesses"),
    ("PeoplePage", "People", "Search and manage people"),
    ("CampaignPage", "Campaigns", "Manage your outreach campaigns"),
    ("AutomationPage", "Automation", "Manage n8n workflows"),
    ("AIPage", "AI Assistant", "Interact with AI"),
    ("ExportPage", "Exports", "Manage data exports"),
    ("SettingsPage", "Settings", "Application settings"),
    ("DeveloperPage", "Developer", "Developer mode and diagnostics")
]

template = """export default function {component}() {{
  return (
    <div className="page-container">
      <header className="page-header">
        <h1 className="page-title">{title}</h1>
        <p className="page-subtitle">{subtitle}</p>
      </header>
      <div className="page-content">
        <div className="coming-soon-card">
          <p>Coming Soon</p>
        </div>
      </div>
    </div>
  );
}}
"""

for component, title, subtitle in pages:
    path = f"frontend/src/pages/{component}.tsx"
    with open(path, "w") as f:
        f.write(template.format(component=component, title=title, subtitle=subtitle))
