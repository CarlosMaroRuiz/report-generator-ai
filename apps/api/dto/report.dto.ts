export interface CreateReportDTO {
  taskId?: string;
  msg: string;
}

export interface ReportResponseDTO {
  taskId: string;
  msg: string;
  status: string;
  createdAt: string;
}