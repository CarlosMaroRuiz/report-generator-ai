import { Request, Response } from 'express';

export class WelcomeController {
    public getWelcomeMessage(req: Request, res: Response): void {
        res.json({ message: "Welcome to the API!" });
    }
}