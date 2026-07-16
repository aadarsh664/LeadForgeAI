import React from "react";
interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
}
export function Input({ label, error, className = "", ...props }: InputProps) {
  return (
    <div className={`ds-input-wrapper ${className}`}>
      {label && <label className="ds-typography-label">{label}</label>}
      <input className="ds-input" {...props} />
      {error && <span className="ds-input-error" style={{ color: "var(--color-danger)", fontSize: "var(--font-size-xs)" }}>{error}</span>}
    </div>
  );
}
