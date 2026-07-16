import os

components = {
    "SearchInput.tsx": """import React from "react";
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
""",
    "Textarea.tsx": """import React from "react";
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
""",
    "Dropdown.tsx": """import React from "react";
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
""",
    "Switch.tsx": """import React from "react";
interface SwitchProps extends Omit<React.InputHTMLAttributes<HTMLInputElement>, 'type'> {
  label?: string;
}
export function Switch({ label, className = "", ...props }: SwitchProps) {
  return (
    <label className={`ds-switch-wrapper ${className}`} style={{ display: 'flex', alignItems: 'center', gap: '8px', cursor: 'pointer' }}>
      <input type="checkbox" style={{ accentColor: 'var(--color-primary)' }} {...props} />
      {label && <span className="ds-typography-label" style={{ margin: 0 }}>{label}</span>}
    </label>
  );
}
""",
    "Checkbox.tsx": """import React from "react";
interface CheckboxProps extends Omit<React.InputHTMLAttributes<HTMLInputElement>, 'type'> {
  label?: string;
}
export function Checkbox({ label, className = "", ...props }: CheckboxProps) {
  return (
    <label className={`ds-checkbox-wrapper ${className}`} style={{ display: 'flex', alignItems: 'center', gap: '8px', cursor: 'pointer' }}>
      <input type="checkbox" style={{ accentColor: 'var(--color-primary)' }} {...props} />
      {label && <span className="ds-typography-label" style={{ margin: 0 }}>{label}</span>}
    </label>
  );
}
""",
    "Radio.tsx": """import React from "react";
interface RadioProps extends Omit<React.InputHTMLAttributes<HTMLInputElement>, 'type'> {
  label?: string;
}
export function Radio({ label, className = "", ...props }: RadioProps) {
  return (
    <label className={`ds-radio-wrapper ${className}`} style={{ display: 'flex', alignItems: 'center', gap: '8px', cursor: 'pointer' }}>
      <input type="radio" style={{ accentColor: 'var(--color-primary)' }} {...props} />
      {label && <span className="ds-typography-label" style={{ margin: 0 }}>{label}</span>}
    </label>
  );
}
""",
    "Modal.tsx": """import React from "react";
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
""",
    "Dialog.tsx": """import React from "react";
import { Modal } from "./Modal";
interface DialogProps {
  isOpen: boolean;
  onClose: () => void;
  onConfirm: () => void;
  title: string;
  message: string;
}
export function Dialog({ isOpen, onClose, onConfirm, title, message }: DialogProps) {
  return (
    <Modal isOpen={isOpen} onClose={onClose} title={title}>
      <p className="ds-typography-body">{message}</p>
      <div style={{ marginTop: '24px', display: 'flex', gap: '8px', justifyContent: 'flex-end' }}>
        <button className="ds-btn ds-btn-secondary" onClick={onClose}>Cancel</button>
        <button className="ds-btn ds-btn-primary" onClick={onConfirm}>Confirm</button>
      </div>
    </Modal>
  );
}
""",
    "Chip.tsx": """import React from "react";
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
""",
    "Toast.tsx": """import React from "react";
interface ToastProps {
  message: string;
  type?: "success" | "error" | "info";
}
export function Toast({ message, type = "info" }: ToastProps) {
  return (
    <div className="ds-card" style={{ position: 'fixed', bottom: '24px', right: '24px', zIndex: 100, padding: '12px 24px', display: 'flex', alignItems: 'center', gap: '8px', backgroundColor: type === 'error' ? 'var(--color-danger)' : 'var(--color-bg-base)', color: type === 'error' ? 'white' : 'inherit' }}>
      <span style={{ fontSize: '14px', fontWeight: 500 }}>{message}</span>
    </div>
  );
}
""",
    "ProgressBar.tsx": """import React from "react";
export function ProgressBar({ progress, className = "" }: { progress: number; className?: string }) {
  return (
    <div style={{ width: '100%', height: '8px', backgroundColor: 'var(--color-bg-muted)', borderRadius: '4px', overflow: 'hidden' }} className={className}>
      <div style={{ width: `${progress}%`, height: '100%', backgroundColor: 'var(--color-primary)', transition: 'width 0.3s ease' }} />
    </div>
  );
}
""",
    "Loader.tsx": """import React from "react";
import { Loader2 } from "lucide-react";
export function Loader({ size = 24, className = "" }: { size?: number, className?: string }) {
  return <Loader2 size={size} className={className} style={{ animation: 'spin 1s linear infinite', color: 'var(--color-primary)' }} />;
}
""",
    "Tooltip.tsx": """import React from "react";
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
""",
    "Avatar.tsx": """import React from "react";
export function Avatar({ src, alt, fallback, size = 32 }: { src?: string; alt?: string; fallback: string; size?: number }) {
  return (
    <div style={{ width: size, height: size, borderRadius: '50%', backgroundColor: 'var(--color-secondary)', display: 'flex', alignItems: 'center', justifyContent: 'center', overflow: 'hidden', fontWeight: 600, fontSize: size * 0.4, color: 'var(--color-text-secondary)' }}>
      {src ? <img src={src} alt={alt} style={{ width: '100%', height: '100%', objectFit: 'cover' }} /> : fallback}
    </div>
  );
}
""",
    "EmptyState.tsx": """import React from "react";
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
""",
    "SectionHeader.tsx": """import React from "react";
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
""",
    "PageHeader.tsx": """import React from "react";
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
"""
}

for name, content in components.items():
    with open(f"frontend/src/design-system/components/{name}", "w", encoding="utf-8") as f:
        f.write(content)

with open("frontend/src/design-system/components/index.ts", "w", encoding="utf-8") as f:
    f.write("export * from './Button';\n")
    f.write("export * from './Input';\n")
    f.write("export * from './SearchInput';\n")
    f.write("export * from './Textarea';\n")
    f.write("export * from './Dropdown';\n")
    f.write("export * from './Switch';\n")
    f.write("export * from './Checkbox';\n")
    f.write("export * from './Radio';\n")
    f.write("export * from './Card';\n")
    f.write("export * from './Modal';\n")
    f.write("export * from './Dialog';\n")
    f.write("export * from './Badge';\n")
    f.write("export * from './Chip';\n")
    f.write("export * from './Toast';\n")
    f.write("export * from './ProgressBar';\n")
    f.write("export * from './Loader';\n")
    f.write("export * from './Divider';\n")
    f.write("export * from './Tooltip';\n")
    f.write("export * from './Avatar';\n")
    f.write("export * from './EmptyState';\n")
    f.write("export * from './SectionHeader';\n")
    f.write("export * from './PageHeader';\n")
    f.write("export * from './Typography';\n")
