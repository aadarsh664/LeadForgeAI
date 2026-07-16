import React from "react";
interface DropdownProps extends React.SelectHTMLAttributes<HTMLSelectElement> {
  label?: string;
  options: { label: string; value: string }[];
}
export function Dropdown({ label, options, className = "", ...props }: DropdownProps) {
  return (
    <div className={`ds-input-wrapper ${className}`}>
      {label && <label className="ds-typography-label">{label}</label>}
      <select className="ds-input" {...props}>
        {options.map(opt => <option key={opt.value} value={opt.value}>{opt.label}</option>)}
      </select>
    </div>
  );
}
