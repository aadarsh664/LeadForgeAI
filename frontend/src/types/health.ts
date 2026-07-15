export interface HealthResponse {
  application: string;
  version: string;
  backend: string;
  database: string;
  docker: string;
  n8n: string;
  timestamp: string;
  overall_status: string;
}
