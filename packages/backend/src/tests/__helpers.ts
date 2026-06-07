import http from "node:http";
import supertest, { type Agent } from "supertest";
import { GRAPHQL_PATH } from "~/config";
import { createExpressApp, createYogaServer } from "~/server-setup";

export interface TestContext {
  request: Agent;
  stopServer: () => Promise<void>;
}

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
    stopServer: () =>
      new Promise<void>((resolve) => {
        httpServer.close(() => resolve());
      }),
  };
}

export { createTestContext };
