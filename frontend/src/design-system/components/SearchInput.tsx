import React from "react";
import { Search } from "lucide-react";

interface SearchInputProps extends React.InputHTMLAttributes<HTMLInputElement> {}

export function SearchInput({ className = "", ...props }: SearchInputProps) {
  return (
    <div className={`ds-search-wrapper ${className}`} style={{ position: 'relative', display: 'inline-block', width: '100%' }}>
      <Search size={16} style={{ position: 'absolute', left: '12px', top: '50%', transform: 'translateY(-50%)', color: 'var(--color-text-tertiary)' }} />
      <input className="ds-input" style={{ paddingLeft: '36px' }} {...props} />
    </div>
  );
}
