import { BaseRoutes } from "../core/routes/base.routes";
import { ReportController } from "../controller/report.controller";

export class ReportRoutes extends BaseRoutes<ReportController> {
  constructor() {
    super(ReportController);
  }

  protected initRoutes(): void {
    // POST /api/report/generate -> Encola el reporte y retorna taskId
    this.router.post('/generate', this.controller.generateReport);

    // GET /api/report/subscribe/:taskId -> Suscripción SSE en vivo
    this.router.get('/subscribe/:taskId', this.controller.subscribeToReport);
  }
}