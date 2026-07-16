import React from "react";
export function Avatar({ src, alt, fallback, size = 32 }: { src?: string; alt?: string; fallback: string; size?: number }) {
  return (
    <div style={{ width: size, height: size, borderRadius: '50%', backgroundColor: 'var(--color-secondary)', display: 'flex', alignItems: 'center', justifyContent: 'center', overflow: 'hidden', fontWeight: 600, fontSize: size * 0.4, color: 'var(--color-text-secondary)' }}>
      {src ? <img src={src} alt={alt} style={{ width: '100%', height: '100%', objectFit: 'cover' }} /> : fallback}
    </div>
  );
}
