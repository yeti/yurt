import type { IncomingHttpHeaders } from "http";
import prisma from "~/prismaClient";
import type { PrismaClient } from "~/generated/prisma/client.js";
import type { Request } from "express";

export interface Context {
  headers: IncomingHttpHeaders;
  prisma: PrismaClient;
}

export async function createContext({
  req,
}: {
  req: Request;
}): Promise<Context> {
  return {
    headers: req.headers,
    prisma,
  };
}
