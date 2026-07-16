import React from "react";
export function Tooltip({ children, text }: { children: React.ReactNode; text: string }) {
  return (
    <div style={{ position: 'relative', display: 'inline-block' }} className="ds-tooltip-container">
      {children}
      <div className="ds-tooltip" style={{ position: 'absolute', bottom: '100%', left: '50%', transform: 'translateX(-50%)', marginBottom: '8px', padding: '4px 8px', backgroundColor: 'var(--color-primary)', color: 'var(--color-text-inverse)', fontSize: 'var(--font-size-xs)', borderRadius: '4px', whiteSpace: 'nowrap', opacity: 0, pointerEvents: 'none', transition: 'opacity 0.2s' }}>
        {text}
      </div>
      <style>{`.ds-tooltip-container:hover .ds-tooltip { opacity: 1; }`}</style>
    </div>
  );
}
