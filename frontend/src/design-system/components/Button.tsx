import React from "react";
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
