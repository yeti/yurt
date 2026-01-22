import supertest, { Agent } from 'supertest';
import http from 'http';
import { createExpressApp, createApolloServer } from '~/serverSetup';

export type TestContext = {
  request: Agent;
  stopServer: () => Promise<void>;
};

async function createTestContext() {
  const app = createExpressApp();
  const httpServer = http.createServer(app);

  const server = await createApolloServer(app, httpServer);

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
