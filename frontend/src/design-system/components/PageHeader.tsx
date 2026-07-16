import React from "react";
import { H1, Text } from "./Typography";
export function PageHeader({ title, description, action }: { title: string; description?: string; action?: React.ReactNode }) {
  return (
    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '32px' }}>
      <div>
        <H1 style={{ margin: 0 }}>{title}</H1>
        {description && <Text style={{ marginTop: '8px' }}>{description}</Text>}
      </div>
      {action && <div>{action}</div>}
    </div>
  );
}
