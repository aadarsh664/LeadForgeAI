import React from "react";
export function ProgressBar({ progress, className = "" }: { progress: number; className?: string }) {
  return (
    <div style={{ width: '100%', height: '8px', backgroundColor: 'var(--color-bg-muted)', borderRadius: '4px', overflow: 'hidden' }} className={className}>
      <div style={{ width: `${progress}%`, height: '100%', backgroundColor: 'var(--color-primary)', transition: 'width 0.3s ease' }} />
    </div>
  );
}
