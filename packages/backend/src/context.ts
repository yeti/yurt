import type { IncomingHttpHeaders } from "node:http";
import type { Request } from "express";
import type { PrismaClient } from "~/generated/prisma/client.js";
import prisma from "~/prisma-client";

export interface Context {
  headers: IncomingHttpHeaders;
  prisma: PrismaClient;
}

export function createContext({ req }: { req: Request }): Context {
  return {
    headers: req.headers,
    prisma,
  };
}
