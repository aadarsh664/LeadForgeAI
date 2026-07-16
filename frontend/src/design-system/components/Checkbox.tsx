import React from "react";
interface CheckboxProps extends Omit<React.InputHTMLAttributes<HTMLInputElement>, 'type'> {
  label?: string;
}
export function Checkbox({ label, className = "", ...props }: CheckboxProps) {
  return (
    <label className={`ds-checkbox-wrapper ${className}`} style={{ display: 'flex', alignItems: 'center', gap: '8px', cursor: 'pointer' }}>
      <input type="checkbox" style={{ accentColor: 'var(--color-primary)' }} {...props} />
      {label && <span className="ds-typography-label" style={{ margin: 0 }}>{label}</span>}
    </label>
  );
}
