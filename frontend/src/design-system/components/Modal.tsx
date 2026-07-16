import React from "react";
interface ModalProps {
  isOpen: boolean;
  onClose: () => void;
  title?: string;
  children: React.ReactNode;
}
export function Modal({ isOpen, onClose, title, children }: ModalProps) {
  if (!isOpen) return null;
  return (
    <div style={{ position: 'fixed', inset: 0, zIndex: 50, display: 'flex', alignItems: 'center', justifyContent: 'center', backgroundColor: 'rgba(0,0,0,0.5)' }}>
      <div className="ds-card" style={{ width: '100%', maxWidth: '500px', backgroundColor: 'var(--color-bg-base)' }}>
        {title && <h3 className="ds-typography-h3" style={{ marginBottom: '16px' }}>{title}</h3>}
        <div>{children}</div>
        <div style={{ marginTop: '24px', textAlign: 'right' }}>
          <button className="ds-btn ds-btn-secondary" onClick={onClose}>Close</button>
        </div>
      </div>
    </div>
  );
}
