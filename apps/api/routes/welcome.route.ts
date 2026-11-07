import { BaseRoutes } from "../core/routes/base.routes";
import { WelcomeController } from "../controller/welcome.controller";

export class WelcomeRoutes extends BaseRoutes<WelcomeController> {
    constructor() {
        super(WelcomeController);
    }

    protected initRoutes(): void {
        this.router.get('/', this.controller.getWelcomeMessage);
    }
}