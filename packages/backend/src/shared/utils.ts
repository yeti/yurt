import express, { NextFunction, Request, Response } from 'express';

export const unless = function (paths: string[], middleware: express.Handler) {
  return function (req: Request, res: Response, next: NextFunction) {
    if (
      paths.includes(req.path) ||
      paths.filter((path) => path.includes(req.path)).length > 0
    ) {
      return next();
    } else {
      return middleware(req, res, next);
    }
  };
};
