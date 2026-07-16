import React from "react";
interface SwitchProps extends Omit<React.InputHTMLAttributes<HTMLInputElement>, 'type'> {
  label?: string;
}
export function Switch({ label, className = "", ...props }: SwitchProps) {
  return (
    <label className={`ds-switch-wrapper ${className}`} style={{ display: 'flex', alignItems: 'center', gap: '8px', cursor: 'pointer' }}>
      <input type="checkbox" style={{ accentColor: 'var(--color-primary)' }} {...props} />
      {label && <span className="ds-typography-label" style={{ margin: 0 }}>{label}</span>}
    </label>
  );
}
