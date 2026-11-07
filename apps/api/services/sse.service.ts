import { Response } from 'express';

export class SSEService {
  private static instance: SSEService;
  private clients: Map<string, Response> = new Map();

  private constructor() {}

  public static getInstance(): SSEService {
    if (!SSEService.instance) {
      SSEService.instance = new SSEService();
    }
    return SSEService.instance;
  }

  public addClient(taskId: string, res: Response): void {
    this.clients.set(taskId, res);

    res.on('close', () => {
      this.clients.delete(taskId);
    });
  }

  /**
   * Emite el payload SSE al cliente correspondiente mediante su taskId y cierra el stream
   */
  public sendEventToClient(taskId: string, payload: object): void {
    const client = this.clients.get(taskId);

    if (client) {
      // Estructura oficial del protocolo Server-Sent Events: data: { ... }\n\n
      client.write(`data: ${JSON.stringify(payload)}\n\n`);
      
      // Finaliza la conexión HTTP una vez entregado el resultado final de Python
      client.end();
      this.clients.delete(taskId);
    }
  }
}