import Redis from 'ioredis';
import { SSEService } from './sse.service.js';

export class ReportResultListener {
  private redisClient: Redis;
  private sseService: SSEService;

  constructor() {
    const redisUrl = process.env.REDIS_URL;
    this.redisClient = new Redis(redisUrl);
    this.sseService = SSEService.getInstance();
  }

  /**
   * Escucha de forma continua en segundo plano la lista de resultados de Redis
   */
  public listen(): void {
    const pollResults = async () => {
      while (true) {
        try {
          // Bucle bloqueante blpop sobre la clave 'report-results'
          const res = await this.redisClient.blpop('report-results', 0);
          if (res) {
            const [, payloadRaw] = res;
            const data = JSON.parse(payloadRaw);

            // Transmite el evento SSE directo al navegador del usuario
            this.sseService.sendEventToClient(data.taskId, data);
          }
        } catch (error) {
          console.error('[ReportResultListener] Error en el bus de eventos:', error);
          await new Promise((resolve) => setTimeout(resolve, 2000));
        }
      }
    };

    pollResults();
  }
}