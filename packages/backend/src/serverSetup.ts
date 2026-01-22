import { ApolloServer } from '@apollo/server';
import { expressMiddleware } from '@as-integrations/express5';
import { ApolloServerPluginDrainHttpServer } from '@apollo/server/plugin/drainHttpServer';
import { applyMiddleware } from 'graphql-middleware';
import express from 'express';
import helmet from 'helmet';
import cors from 'cors';
import http from 'http';
import { schema } from '~/schema';
import permissions from '~/permissions';
import { createContext } from '~/context';
import { logger } from '~/loggers';
import pinoLogger from '~/apolloPlugins/logger';
import { NODE_ENV, GRAPHQL_PATH } from '~/config';

export function createExpressApp() {
  const app = express();

  app.use(cors({ exposedHeaders: ['Authorization'] }));
  app.use(
    helmet({
      contentSecurityPolicy: {
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

  app.get('/healthz', (_req, res) => {
    res.send('Ok');
  });

  return app;
}

export async function createApolloServer(
  app: express.Application,
  httpServer: http.Server,
) {
  const graphqlSchema = applyMiddleware(schema, permissions);

  const server = new ApolloServer({
    schema: graphqlSchema,
    introspection: NODE_ENV !== 'production',
    ...(NODE_ENV !== 'test' ? { logger: logger } : {}),
    plugins: [
      ApolloServerPluginDrainHttpServer({ httpServer }),
      ...(NODE_ENV !== 'test' ? [pinoLogger] : []),
    ],
  });

  await server.start();

  app.use(
    GRAPHQL_PATH,
    express.json(),
    expressMiddleware(server, {
      context: createContext,
    }),
  );

  return server;
}
