// import * as Sentry from "@sentry/node";
import express from 'express';
import cors from 'cors';
import helmet from 'helmet';
import { ApolloServer } from '@apollo/server';
import { expressMiddleware } from '@apollo/server/express4';
import { ApolloServerPluginDrainHttpServer } from '@apollo/server/plugin/drainHttpServer';
import { applyMiddleware } from 'graphql-middleware';
import http from 'http';
import { logger } from '~/loggers';
import { createContext } from '~/context';
import { schema } from '~/schema';
import { NODE_ENV, PORT } from '~/config';
import permissions from '~/permissions';
// import sentryPlugin from '~/apolloPlugins/sentry';
import pinoLogger from '~/apolloPlugins/logger';

const start = async () => {
  const app = express();

  app.use(
    helmet({
      contentSecurityPolicy: {
        // these directives are needed for the apollo sandbox
        directives: {
          imgSrc: [
            `'self'`,
            'data:',
            'apollo-server-landing-page.cdn.apollographql.com',
          ],
          scriptSrc: [`'self'`, `https: 'unsafe-inline'`],
          manifestSrc: [
            `'self'`,
            'apollo-server-landing-page.cdn.apollographql.com',
          ],
          frameSrc: [`'self'`, 'sandbox.embed.apollographql.com'],
        },
      },
    }),
  );

  app.use(
    cors({
      exposedHeaders: ['Authorization'],
    }),
  );

  // health check endpoint
  app.get('/healthz', (_req, res) => {
    res.send('Ok');
  });

  const httpServer = http.createServer(app);

  const graphqlPath = '/api/graphql';
  const graphqlSchema = applyMiddleware(schema, permissions);

  const server = new ApolloServer({
    schema: graphqlSchema,
    introspection: NODE_ENV !== 'production',
    logger: logger,
    plugins: [
      // sentryPlugin,
      ApolloServerPluginDrainHttpServer({ httpServer }),
      pinoLogger,
    ],
  });

  await server.start();

  app.use(
    graphqlPath,
    cors<cors.CorsRequest>(),
    express.json({ limit: '50mb' }),
    expressMiddleware(server, { context: createContext }),
  );

  await new Promise<void>((resolve) =>
    httpServer.listen({ port: PORT }, resolve),
  );

  logger.info(`🚀 Server ready at http://localhost:${PORT}${graphqlPath}`);
};

start();
