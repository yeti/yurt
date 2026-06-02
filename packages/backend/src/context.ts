import type { Request } from "express";
import type { IncomingHttpHeaders } from "http";
import type { PrismaClient } from "~/generated/prisma/client.js";
import prisma from "~/prismaClient";

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
