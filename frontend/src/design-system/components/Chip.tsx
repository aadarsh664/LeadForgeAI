import React from "react";
interface ChipProps extends React.HTMLAttributes<HTMLSpanElement> {
  onRemove?: () => void;
}
export function Chip({ children, onRemove, className = "", ...props }: ChipProps) {
  return (
    <span className={`ds-badge ${className}`} style={{ borderRadius: '16px', display: 'inline-flex', alignItems: 'center', gap: '4px', padding: '4px 12px' }} {...props}>
      {children}
      {onRemove && <button onClick={onRemove} style={{ background: 'transparent', border: 'none', cursor: 'pointer', fontSize: '10px', padding: 0 }}>✕</button>}
    </span>
  );
}
