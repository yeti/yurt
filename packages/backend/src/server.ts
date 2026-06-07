import http from "node:http";
import { GRAPHQL_PATH, PORT } from "~/config";
import { logger } from "~/loggers";
import { createExpressApp, createYogaServer } from "./server-setup";

const app = createExpressApp();
const yoga = await createYogaServer();

app.use(GRAPHQL_PATH, async (req, res) => {
  await yoga(req, res);
});

const httpServer = http.createServer(app);

await new Promise<void>((resolve) =>
  httpServer.listen({ port: PORT }, resolve)
);

logger.info(`Server ready on port ${PORT}${GRAPHQL_PATH}`);
