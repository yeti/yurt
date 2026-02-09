import http from 'http';
import { logger } from '~/loggers';
import { PORT, GRAPHQL_PATH } from '~/config';
import { createExpressApp, createYogaServer } from './serverSetup';

const app = createExpressApp();
const yoga = await createYogaServer();

app.use(GRAPHQL_PATH, async (req, res) => {
  await yoga(req, res);
});

const httpServer = http.createServer(app);

await new Promise<void>((resolve) =>
  httpServer.listen({ port: PORT }, resolve),
);

logger.info(`Server ready on port ${PORT}${GRAPHQL_PATH}`);
