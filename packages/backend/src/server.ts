import express from 'express';
import cors from 'cors';
import { expressMiddleware } from '@apollo/server/express4';
import http from 'http';
import { logger } from '~/loggers';
import { createContext } from '~/context';
import { PORT, GRAPHQL_PATH } from '~/config';
import { createExpressApp, createApolloServer } from './serverSetup';

export async function startServer(): Promise<void> {
  const app = createExpressApp();
  const httpServer = http.createServer(app);
  const server = createApolloServer(httpServer);

  await server.start();

  app.use(
    GRAPHQL_PATH,
    cors<cors.CorsRequest>(),
    express.json({ limit: '50mb' }),
    expressMiddleware(server, { context: createContext }),
  );

  await new Promise<void>((resolve) =>
    httpServer.listen({ port: PORT }, resolve),
  );

  logger.info(`🚀 Server ready at http://localhost:${PORT}${GRAPHQL_PATH}`);
}

startServer();
