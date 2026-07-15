export interface StartupStatusResponse {
  current_step: string;
  completed_steps: string[];
  progress_percentage: number;
  overall_status: "idle" | "running" | "success" | "failed";
  is_ready: boolean;
  message: string;
}
