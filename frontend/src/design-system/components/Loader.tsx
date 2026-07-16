import React from "react";
import { Loader2 } from "lucide-react";
export function Loader({ size = 24, className = "" }: { size?: number, className?: string }) {
  return <Loader2 size={size} className={className} style={{ animation: 'spin 1s linear infinite', color: 'var(--color-primary)' }} />;
}
