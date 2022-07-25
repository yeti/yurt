import express, { Request, Response } from "express";

const app = express();

app.get("/status", (_req: Request, res: Response) => {
  res.send();
});

export default app;
