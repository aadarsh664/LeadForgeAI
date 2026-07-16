import os

css_content = """
/* Design Tokens */
:root {
  /* Colors */
  --color-primary: #111827;
  --color-primary-hover: #374151;
  --color-secondary: #f3f4f6;
  --color-secondary-hover: #e5e7eb;
  --color-danger: #ef4444;
  --color-danger-hover: #dc2626;
  --color-success: #10b981;
  
  --color-text-primary: #111827;
  --color-text-secondary: #6b7280;
  --color-text-tertiary: #9ca3af;
  --color-text-inverse: #ffffff;
  
  --color-bg-base: #ffffff;
  --color-bg-subtle: #f9fafb;
  --color-bg-muted: #f3f4f6;
  
  --color-border-subtle: #f3f4f6;
  --color-border-default: #e5e7eb;
  --color-border-strong: #d1d5db;
  
  /* Spacing */
  --space-4: 4px;
  --space-8: 8px;
  --space-12: 12px;
  --space-16: 16px;
  --space-24: 24px;
  --space-32: 32px;
  --space-40: 40px;
  --space-48: 48px;
  --space-64: 64px;
  --space-96: 96px;
  
  /* Radii */
  --radius-sm: 4px;
  --radius-md: 8px;
  --radius-lg: 12px;
  --radius-xl: 16px;
  
  /* Shadows */
  --shadow-sm: 0 1px 2px 0 rgb(0 0 0 / 0.05);
  --shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1);
  --shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1);
  
  /* Typography */
  --font-family-base: 'Inter', 'Helvetica Neue', sans-serif;
  --font-family-mono: 'JetBrains Mono', monospace;
  
  --font-size-xs: 0.75rem;
  --font-size-sm: 0.875rem;
  --font-size-base: 1rem;
  --font-size-lg: 1.125rem;
  --font-size-xl: 1.25rem;
  --font-size-2xl: 1.5rem;
  --font-size-3xl: 1.875rem;
  --font-size-4xl: 2.25rem;
  
  --font-weight-regular: 400;
  --font-weight-medium: 500;
  --font-weight-semibold: 600;
  --font-weight-bold: 700;
  
  /* Transitions */
  --transition-fast: 150ms ease;
  --transition-normal: 200ms ease;
  --transition-slow: 250ms ease;
}

[data-theme="dark"] {
  --color-primary: #f9fafb;
  --color-primary-hover: #d1d5db;
  --color-secondary: #374151;
  --color-secondary-hover: #4b5563;
  
  --color-text-primary: #f9fafb;
  --color-text-secondary: #9ca3af;
  --color-text-tertiary: #6b7280;
  --color-text-inverse: #111827;
  
  --color-bg-base: #111827;
  --color-bg-subtle: #1f2937;
  --color-bg-muted: #374151;
  
  --color-border-subtle: #1f2937;
  --color-border-default: #374151;
  --color-border-strong: #4b5563;
  
  --shadow-sm: 0 1px 2px 0 rgb(0 0 0 / 0.5);
  --shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.4), 0 2px 4px -2px rgb(0 0 0 / 0.4);
  --shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.4), 0 4px 6px -4px rgb(0 0 0 / 0.4);
}

body {
  background-color: var(--color-bg-base);
  color: var(--color-text-primary);
  font-family: var(--font-family-base);
  transition: background-color var(--transition-normal), color var(--transition-normal);
}

/* Component Styles */
.ds-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: var(--space-8);
  font-family: var(--font-family-base);
  font-weight: var(--font-weight-medium);
  font-size: var(--font-size-sm);
  border-radius: var(--radius-md);
  padding: var(--space-8) var(--space-16);
  cursor: pointer;
  transition: all var(--transition-fast);
  border: none;
}
.ds-btn:disabled { opacity: 0.5; cursor: not-allowed; }
.ds-btn-primary { background: var(--color-primary); color: var(--color-text-inverse); }
.ds-btn-primary:hover:not(:disabled) { background: var(--color-primary-hover); }
.ds-btn-secondary { background: var(--color-secondary); color: var(--color-text-primary); }
.ds-btn-secondary:hover:not(:disabled) { background: var(--color-secondary-hover); }
.ds-btn-ghost { background: transparent; color: var(--color-text-secondary); }
.ds-btn-ghost:hover:not(:disabled) { background: var(--color-secondary); color: var(--color-text-primary); }
.ds-btn-danger { background: var(--color-danger); color: white; }
.ds-btn-danger:hover:not(:disabled) { background: var(--color-danger-hover); }

.ds-input {
  width: 100%;
  padding: var(--space-8) var(--space-12);
  border-radius: var(--radius-md);
  border: 1px solid var(--color-border-default);
  background: var(--color-bg-base);
  color: var(--color-text-primary);
  font-family: var(--font-family-base);
  font-size: var(--font-size-sm);
  transition: border-color var(--transition-fast);
}
.ds-input:focus { outline: none; border-color: var(--color-primary); }
.ds-input:disabled { opacity: 0.5; background: var(--color-bg-muted); cursor: not-allowed; }

.ds-card {
  background: var(--color-bg-base);
  border: 1px solid var(--color-border-subtle);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-sm);
  padding: var(--space-24);
}

.ds-badge {
  display: inline-flex;
  align-items: center;
  padding: 2px var(--space-8);
  border-radius: var(--radius-sm);
  font-size: var(--font-size-xs);
  font-weight: var(--font-weight-medium);
  background: var(--color-secondary);
  color: var(--color-text-primary);
}
.ds-badge-success { background: var(--color-success); color: white; }
.ds-badge-danger { background: var(--color-danger); color: white; }

.ds-divider {
  height: 1px;
  background: var(--color-border-subtle);
  width: 100%;
  margin: var(--space-16) 0;
}

.ds-typography-h1 { font-size: var(--font-size-4xl); font-weight: var(--font-weight-bold); margin-bottom: var(--space-16); }
.ds-typography-h2 { font-size: var(--font-size-3xl); font-weight: var(--font-weight-semibold); margin-bottom: var(--space-12); }
.ds-typography-h3 { font-size: var(--font-size-2xl); font-weight: var(--font-weight-semibold); margin-bottom: var(--space-8); }
.ds-typography-body { font-size: var(--font-size-base); color: var(--color-text-secondary); line-height: 1.5; }
.ds-typography-label { font-size: var(--font-size-sm); font-weight: var(--font-weight-medium); display: block; margin-bottom: var(--space-4); }

"""

components = {
    "Button.tsx": """import React from "react";
interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: "primary" | "secondary" | "ghost" | "danger";
  icon?: React.ReactNode;
}
export function Button({ variant = "primary", icon, children, className = "", ...props }: ButtonProps) {
  return (
    <button className={`ds-btn ds-btn-${variant} ${className}`} {...props}>
      {icon && <span className="ds-btn-icon">{icon}</span>}
      {children}
    </button>
  );
}
""",
    "Input.tsx": """import React from "react";
interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
}
export function Input({ label, error, className = "", ...props }: InputProps) {
  return (
    <div className={`ds-input-wrapper ${className}`}>
      {label && <label className="ds-typography-label">{label}</label>}
      <input className="ds-input" {...props} />
      {error && <span className="ds-input-error" style={{ color: "var(--color-danger)", fontSize: "var(--font-size-xs)" }}>{error}</span>}
    </div>
  );
}
""",
    "Card.tsx": """import React from "react";
export function Card({ children, className = "", ...props }: React.HTMLAttributes<HTMLDivElement>) {
  return (
    <div className={`ds-card ${className}`} {...props}>
      {children}
    </div>
  );
}
""",
    "Badge.tsx": """import React from "react";
interface BadgeProps extends React.HTMLAttributes<HTMLSpanElement> {
  variant?: "default" | "success" | "danger";
}
export function Badge({ variant = "default", children, className = "", ...props }: BadgeProps) {
  return (
    <span className={`ds-badge ds-badge-${variant} ${className}`} {...props}>
      {children}
    </span>
  );
}
""",
    "Divider.tsx": """import React from "react";
export function Divider({ className = "" }: { className?: string }) {
  return <div className={`ds-divider ${className}`} />;
}
""",
    "Typography.tsx": """import React from "react";
export function H1({ children, className = "" }: React.HTMLAttributes<HTMLHeadingElement>) { return <h1 className={`ds-typography-h1 ${className}`}>{children}</h1>; }
export function H2({ children, className = "" }: React.HTMLAttributes<HTMLHeadingElement>) { return <h2 className={`ds-typography-h2 ${className}`}>{children}</h2>; }
export function H3({ children, className = "" }: React.HTMLAttributes<HTMLHeadingElement>) { return <h3 className={`ds-typography-h3 ${className}`}>{children}</h3>; }
export function Text({ children, className = "" }: React.HTMLAttributes<HTMLParagraphElement>) { return <p className={`ds-typography-body ${className}`}>{children}</p>; }
export function Label({ children, className = "" }: React.HTMLAttributes<HTMLLabelElement>) { return <label className={`ds-typography-label ${className}`}>{children}</label>; }
"""
}

# Theme Provider
theme_provider = """import React, { createContext, useContext, useEffect, useState } from "react";

type Theme = "light" | "dark" | "system";

interface ThemeContextType {
  theme: Theme;
  setTheme: (theme: Theme) => void;
}

const ThemeContext = createContext<ThemeContextType | undefined>(undefined);

export function ThemeProvider({ children }: { children: React.ReactNode }) {
  const [theme, setTheme] = useState<Theme>(() => {
    return (localStorage.getItem("leadforgeai_theme") as Theme) || "system";
  });

  useEffect(() => {
    const applyTheme = (t: Theme) => {
      const root = window.document.documentElement;
      if (t === "system") {
        const systemTheme = window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
        root.setAttribute("data-theme", systemTheme);
      } else {
        root.setAttribute("data-theme", t);
      }
    };
    applyTheme(theme);
    localStorage.setItem("leadforgeai_theme", theme);
  }, [theme]);

  return <ThemeContext.Provider value={{ theme, setTheme }}>{children}</ThemeContext.Provider>;
}

export function useTheme() {
  const ctx = useContext(ThemeContext);
  if (!ctx) throw new Error("useTheme must be used within ThemeProvider");
  return ctx;
}
"""

os.makedirs("frontend/src/design-system/tokens", exist_ok=True)
with open("frontend/src/design-system/tokens/design-system.css", "w") as f:
    f.write(css_content)

os.makedirs("frontend/src/design-system/components", exist_ok=True)
for name, content in components.items():
    with open(f"frontend/src/design-system/components/{name}", "w") as f:
        f.write(content)

os.makedirs("frontend/src/design-system/providers", exist_ok=True)
with open("frontend/src/design-system/providers/ThemeProvider.tsx", "w") as f:
    f.write(theme_provider)

# Append to styles.css
with open("frontend/src/styles.css", "r") as f:
    orig = f.read()
if "@import './design-system/tokens/design-system.css';" not in orig:
    with open("frontend/src/styles.css", "w") as f:
        f.write("@import './design-system/tokens/design-system.css';\n" + orig)

