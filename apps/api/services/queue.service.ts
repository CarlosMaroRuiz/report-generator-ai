import { Queue } from 'bullmq';

export interface ReportJobData {
  taskId: string;
  msg: string;
}

export class QueueService {
  private reportQueue: Queue<ReportJobData>;

  constructor() {
    // REDIS_URL viene de docker-compose.yml
    const redisUrl = process.env.REDIS_URL;
    const parsedUrl = new URL(redisUrl);

    this.reportQueue = new Queue<ReportJobData>('report-queue', {
      connection: {
        host: parsedUrl.hostname,
        port: Number(parsedUrl.port) || 6379,
        username: parsedUrl.username || undefined,
        password: parsedUrl.password || undefined,
      },
    });
  }

  /**
   * Encola una tarea de generación de reporte para el worker de Python
   */
  public async addReportJob(taskId: string, msg: string): Promise<void> {
    await this.reportQueue.add(
      'generate-report',
      { taskId, msg },
      {
        jobId: taskId,           
        attempts: 3,      
        backoff: {
          type: 'exponential',
          delay: 1000,
        },
        removeOnComplete: true,
      }
    );
  }
}