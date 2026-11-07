import { Router } from "express";

export abstract class BaseRoutes<T> {
    public router: Router;
    public controller: T;
    
    constructor(ControllerClass: new () => T) {
        this.router = Router();
        this.controller = new ControllerClass();
        this.initRoutes();
    }
    protected abstract initRoutes(): void;
}