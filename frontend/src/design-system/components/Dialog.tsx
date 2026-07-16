import React from "react";
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
