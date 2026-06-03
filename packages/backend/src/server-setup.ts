import cors from "cors";
import express from "express";
import { createYoga } from "graphql-yoga";
import helmet from "helmet";
import { NODE_ENV } from "~/config";
import { createContext } from "~/context";
import { runWithRequestLogger } from "~/loggers";
import pinoLogger from "~/plugins/logger";
import sentryPlugin from "~/plugins/sentry";

export function createExpressApp() {
  const app = express();
  app.use((_req, _res, next) => {
    runWithRequestLogger(() => next());
  });
  app.use(cors({ exposedHeaders: ["Authorization"] }));
  app.use(
    helmet({
      contentSecurityPolicy: {
        directives: {
          imgSrc: [`'self'`, "data:"],
          scriptSrc: [`'self'`, `https: 'unsafe-inline'`],
          manifestSrc: [`'self'`],
          frameSrc: [`'self'`],
        },
      },
    })
  );
  app.get("/healthz", (_req, res) => {
    res.send("Ok");
  });
  return app;
}

export async function createYogaServer() {
  await import("./schemaModules");
  const { builder } = await import("~/schema");
  const schema = builder.toSchema();

  const yoga = createYoga<{ req: express.Request; res: express.Response }>({
    schema,
    context: ({ req }) => createContext({ req }),
    logging: NODE_ENV === "test" ? false : pinoLogger,
    plugins: [sentryPlugin],
  });

  return yoga;
}
