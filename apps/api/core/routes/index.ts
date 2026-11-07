import { Router } from "express";
import { WelcomeRoutes } from "../../routes/welcome.route";
import { ReportRoutes } from "../../routes/report.route";
import { ReportController } from "../../controller/report.controller.js";
const apiRouter: Router = Router();

apiRouter.use(new WelcomeRoutes().router);
apiRouter.use("/reports", new ReportRoutes(new ReportController()).router);

export default apiRouter;