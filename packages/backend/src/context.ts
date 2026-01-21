import type { IncomingHttpHeaders } from 'http';
import prisma from '~/prismaClient';
import type { PrismaClient } from '../prisma/generated/client/client.js';
import type { BaseContext } from '@apollo/server';

export interface Context extends BaseContext {
  headers: IncomingHttpHeaders;
  prisma: PrismaClient;
}

export async function createContext({ req }: { req: any }): Promise<Context> {
  return {
    headers: req.headers,
    prisma: prisma,
  };
}
