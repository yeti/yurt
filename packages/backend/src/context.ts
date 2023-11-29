import type { IncomingHttpHeaders } from 'http';
import prisma from '~/prismaClient';
import type { PrismaClient } from '@prisma/client';
import type { BaseContext } from '@apollo/server';
import { ExpressContextFunctionArgument } from '@apollo/server/dist/esm/express4';

export interface Context extends BaseContext {
  headers: IncomingHttpHeaders;
  prisma: PrismaClient;
}

export async function createContext({
  req,
}: ExpressContextFunctionArgument): Promise<Context> {
  return {
    headers: req.headers,
    prisma: prisma,
  };
}
