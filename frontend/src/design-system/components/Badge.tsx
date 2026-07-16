import React from "react";
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
