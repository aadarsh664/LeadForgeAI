import React from "react";
export function EmptyState({ title, description, icon, action }: { title: string; description: string; icon?: React.ReactNode; action?: React.ReactNode }) {
  return (
    <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', padding: '64px', textAlign: 'center', border: '1px dashed var(--color-border-default)', borderRadius: 'var(--radius-lg)' }}>
      {icon && <div style={{ color: 'var(--color-text-tertiary)', marginBottom: '16px' }}>{icon}</div>}
      <h3 className="ds-typography-h3" style={{ marginBottom: '8px' }}>{title}</h3>
      <p className="ds-typography-body" style={{ marginBottom: '24px' }}>{description}</p>
      {action}
    </div>
  );
}
