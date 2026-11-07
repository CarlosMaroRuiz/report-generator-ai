import { Request, Response } from 'express';
import { validate as validateUuid, v4 as uuidv4 } from 'uuid';
import { CreateReportDTO, ReportResponseDTO } from '../dto/report.dto.js';
import { QueueService } from '../services/queue.service.js';
import { SSEService } from '../services/sse.service.js';

export class ReportController {
  private queueService: QueueService;
  private sseService: SSEService;

  constructor() {
    this.queueService = new QueueService();
    this.sseService = SSEService.getInstance();
  }

  // 1. Encola la tarea en Redis usando QueueService
  public generateReport = async (
    req: Request<{}, ReportResponseDTO, CreateReportDTO>,
    res: Response<ReportResponseDTO>
  ): Promise<void> => {
    try {
      const { msg, taskId: requestedTaskId } = req.body;

      if (!msg) {
        res.status(400).json({
          taskId: '',
          msg: 'El campo "msg" es requerido.',
          status: 'error',
          createdAt: new Date().toISOString(),
        });
        return;
      }

      if (requestedTaskId !== undefined && !validateUuid(requestedTaskId)) {
        res.status(400).json({
          taskId: '',
          msg: 'El campo "taskId" debe ser un UUID válido.',
          status: 'error',
          createdAt: new Date().toISOString(),
        });
        return;
      }

      const taskId: string = requestedTaskId ?? uuidv4();

      // Enviar la tarea a la cola de BullMQ en Redis
      await this.queueService.addReportJob(taskId, msg);

      res.status(202).json({
        taskId,
        msg: `Reporte encolado exitosamente: ${msg}`,
        status: 'pending',
        createdAt: new Date().toISOString(),
      });
    } catch (error) {
      res.status(500).json({
        taskId: '',
        msg: (error as Error).message,
        status: 'error',
        createdAt: new Date().toISOString(),
      });
    }
  };

  // 2. Abre el canal de Server-Sent Events (SSE) usando SSEService
  public subscribeToReport = (req: Request<{ taskId: string }>, res: Response): void => {
    const { taskId } = req.params;

    if (!taskId) {
      res.status(400).json({ error: 'El parámetro taskId es requerido.' });
      return;
    }

    // Cabeceras HTTP necesarias para streaming de Server-Sent Events
    res.setHeader('Content-Type', 'text/event-stream');
    res.setHeader('Cache-Control', 'no-cache');
    res.setHeader('Connection', 'keep-alive');
    res.flushHeaders();

    // Guardar la conexión del cliente asociada al taskId
    this.sseService.addClient(taskId, res);

    // Evento de confirmación de suscripción
    res.write(`data: ${JSON.stringify({ status: 'subscribed', taskId })}\n\n`);
  };
}