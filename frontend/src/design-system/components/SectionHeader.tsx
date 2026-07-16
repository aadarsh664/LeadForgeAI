import React from "react";
import { H3, Text } from "./Typography";
export function SectionHeader({ title, description, action }: { title: string; description?: string; action?: React.ReactNode }) {
  return (
    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '24px' }}>
      <div>
        <H3 style={{ margin: 0 }}>{title}</H3>
        {description && <Text style={{ marginTop: '4px' }}>{description}</Text>}
      </div>
      {action && <div>{action}</div>}
    </div>
  );
}
