import type express from "express";
import type { NextFunction, Request, Response } from "express";

export const unless =
  (paths: string[], middleware: express.Handler) =>
  (req: Request, res: Response, next: NextFunction) => {
    if (
      paths.includes(req.path) ||
      paths.filter((path) => path.includes(req.path)).length > 0
    ) {
      return next();
    }
    return middleware(req, res, next);
  };
