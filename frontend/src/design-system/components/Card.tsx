import React from "react";
export function Card({ children, className = "", ...props }: React.HTMLAttributes<HTMLDivElement>) {
  return (
    <div className={`ds-card ${className}`} {...props}>
      {children}
    </div>
  );
}
