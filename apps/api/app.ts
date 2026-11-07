import express, { Application } from 'express';
import apiRouter from './core/routes/index.js';
import { ReportResultListener } from './services/report-result.listener.js';

export class App {
  public app: Application;
  private resultListener: ReportResultListener;

  constructor() {
    this.app = express();
    this.resultListener = new ReportResultListener();

    this.middlewares();
    this.routes();
    this.initBackgroundServices();
  }

  private middlewares(): void {
    this.app.use(express.json());
  }

  private routes(): void {
    this.app.use(express.static('public'));
    this.app.use('/api', apiRouter);
  }

  /**
   * Inicia los servicios de escucha en segundo plano (Redis Pub/Sub / List)
   */
  private initBackgroundServices(): void {
    this.resultListener.listen();
  }
}

export default new App().app;