import type { ExpressContext } from 'apollo-server-express/dist/ApolloServer';
import type { IncomingHttpHeaders } from 'http';
import prisma from './prismaClient';
import type { PrismaClient } from '@prisma/client';
import type { BaseContext } from '@apollo/server';

export interface Context extends BaseContext {
  headers: IncomingHttpHeaders;
  prisma: PrismaClient;
}

export async function createContext({ req }: ExpressContext): Promise<Context> {
  return {
    headers: req.headers,
    prisma: prisma,
  };
}
