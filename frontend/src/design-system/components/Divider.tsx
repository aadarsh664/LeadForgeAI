import React from "react";
export function Divider({ className = "" }: { className?: string }) {
  return <div className={`ds-divider ${className}`} />;
}
