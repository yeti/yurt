import supertest, { Agent } from 'supertest';
import http from 'http';
import { createExpressApp, createYogaServer } from '~/serverSetup';
import { GRAPHQL_PATH } from '~/config';

export type TestContext = {
  request: Agent;
  stopServer: () => Promise<void>;
};

async function createTestContext() {
  const app = createExpressApp();
  const yoga = await createYogaServer();

  app.use(GRAPHQL_PATH, async (req, res) => {
    await yoga(req, res);
  });

  const httpServer = http.createServer(app);

  const request: Agent = supertest(app);

  return {
    request,
    stopServer: async () => {
      httpServer.close();
    },
  };
}

export { createTestContext };
