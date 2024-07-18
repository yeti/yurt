import supertest, { Agent } from 'supertest';
import http from 'http';
import { createExpressApp, createApolloServer } from '~/serverSetup';
import express from 'express';
import cors from 'cors';
import { expressMiddleware } from '@apollo/server/express4';
import { createContext } from '~/context';
import { GRAPHQL_PATH } from '~/config';

export type TestContext = {
  request: Agent;
  stopServer: () => Promise<void>;
};

async function createTestContext() {
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

  const request: Agent = supertest(app);

  return {
    request,
    stopServer: async () => {
      await server.stop();
      httpServer.close();
    },
  };
}

export { createTestContext };
