import React from "react";
interface RadioProps extends Omit<React.InputHTMLAttributes<HTMLInputElement>, 'type'> {
  label?: string;
}
export function Radio({ label, className = "", ...props }: RadioProps) {
  return (
    <label className={`ds-radio-wrapper ${className}`} style={{ display: 'flex', alignItems: 'center', gap: '8px', cursor: 'pointer' }}>
      <input type="radio" style={{ accentColor: 'var(--color-primary)' }} {...props} />
      {label && <span className="ds-typography-label" style={{ margin: 0 }}>{label}</span>}
    </label>
  );
}
