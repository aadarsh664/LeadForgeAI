import React from "react";
import { Card, H3, Text, Button, ProgressBar, Badge } from "../../design-system/components";
import { Loader, XCircle, RotateCcw } from "lucide-react";

interface JobProgressCardProps {
  job: any;
  onCancel: () => void;
  onRetry: () => void;
}

export default function JobProgressCard({ job, onCancel, onRetry }: JobProgressCardProps) {
  if (!job) return null;

  const isCompleted = job.status === "Completed";
  const isFailed = job.status === "Failed";
  const isCancelled = job.status === "Cancelled";
  const isActive = !isCompleted && !isFailed && !isCancelled;

  return (
    <Card style={{ padding: "32px", maxWidth: "600px", margin: "64px auto", display: "flex", flexDirection: "column", gap: "24px" }}>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
        <div>
          <H3 style={{ margin: 0 }}>Search Execution</H3>
          <Text style={{ margin: "4px 0 0 0", color: "var(--color-text-secondary)", fontSize: "0.85rem" }}>
            ID: {job.id}
          </Text>
        </div>
        <Badge variant={
          isCompleted ? "success" : 
          isFailed ? "danger" : 
          isCancelled ? "warning" : "default"
        }>
          {job.status}
        </Badge>
      </div>

      <div style={{ display: "flex", flexDirection: "column", gap: "8px" }}>
        <div style={{ display: "flex", justifyContent: "space-between", fontSize: "0.85rem" }}>
          <span style={{ fontWeight: 600 }}>{job.progress?.stage || "Initializing..."}</span>
          <span style={{ color: "var(--color-text-secondary)" }}>{job.progress?.percentage || 0}%</span>
        </div>
        <ProgressBar progress={job.progress?.percentage || 0} />
      </div>

      <div style={{ display: "flex", flexDirection: "column", gap: "4px", fontSize: "0.85rem", color: "var(--color-text-secondary)", background: "var(--color-bg-subtle)", padding: "12px", borderRadius: "var(--radius-sm)" }}>
        <div style={{ display: "flex", justifyContent: "space-between" }}>
          <span>Provider</span>
          <span style={{ fontWeight: 500, color: "var(--color-text-primary)" }}>{job.provider}</span>
        </div>
        <div style={{ display: "flex", justifyContent: "space-between" }}>
          <span>Target</span>
          <span style={{ fontWeight: 500, color: "var(--color-text-primary)" }}>{job.request.category} in {job.request.location}</span>
        </div>
        {job.error && (
          <div style={{ display: "flex", justifyContent: "space-between", marginTop: "8px", color: "var(--color-danger)" }}>
            <span>Error</span>
            <span>{job.error}</span>
          </div>
        )}
      </div>

      <div style={{ display: "flex", justifyContent: "flex-end", gap: "12px", marginTop: "8px" }}>
        {isActive && (
          <Button variant="ghost" onClick={onCancel} icon={<XCircle size={16}/>}>Cancel Search</Button>
        )}
        {(isFailed || isCancelled) && (
          <Button variant="primary" onClick={onRetry} icon={<RotateCcw size={16}/>}>Retry Search</Button>
        )}
      </div>
    </Card>
  );
}
