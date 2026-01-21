import http from 'http';
import { logger } from '~/loggers';
import { PORT, GRAPHQL_PATH } from '~/config';
import { createExpressApp, createApolloServer } from './serverSetup';

export async function startServer(): Promise<void> {
  const app = createExpressApp();
  const httpServer = http.createServer(app);

  await createApolloServer(app, httpServer);

  await new Promise<void>((resolve) =>
    httpServer.listen({ port: PORT }, resolve),
  );

  logger.info(`🚀 Server ready at http://localhost:${PORT}${GRAPHQL_PATH}`);
}

startServer();
