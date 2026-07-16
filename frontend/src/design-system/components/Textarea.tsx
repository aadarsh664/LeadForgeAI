import React from "react";
interface TextareaProps extends React.TextareaHTMLAttributes<HTMLTextAreaElement> {
  label?: string;
  error?: string;
}
export function Textarea({ label, error, className = "", ...props }: TextareaProps) {
  return (
    <div className={`ds-input-wrapper ${className}`}>
      {label && <label className="ds-typography-label">{label}</label>}
      <textarea className="ds-input" style={{ resize: 'vertical', minHeight: '80px' }} {...props} />
      {error && <span className="ds-input-error" style={{ color: "var(--color-danger)", fontSize: "var(--font-size-xs)" }}>{error}</span>}
    </div>
  );
}
