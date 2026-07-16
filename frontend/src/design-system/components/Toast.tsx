import React from "react";
interface ToastProps {
  message: string;
  type?: "success" | "error" | "info";
}
export function Toast({ message, type = "info" }: ToastProps) {
  return (
    <div className="ds-card" style={{ position: 'fixed', bottom: '24px', right: '24px', zIndex: 100, padding: '12px 24px', display: 'flex', alignItems: 'center', gap: '8px', backgroundColor: type === 'error' ? 'var(--color-danger)' : 'var(--color-bg-base)', color: type === 'error' ? 'white' : 'inherit' }}>
      <span style={{ fontSize: '14px', fontWeight: 500 }}>{message}</span>
    </div>
  );
}
