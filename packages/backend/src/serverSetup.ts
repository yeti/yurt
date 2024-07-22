import { ApolloServer } from '@apollo/server';
import { ApolloServerPluginDrainHttpServer } from '@apollo/server/plugin/drainHttpServer';
import { applyMiddleware } from 'graphql-middleware';
import express from 'express';
import helmet from 'helmet';
import cors from 'cors';
import http from 'http';
import { schema } from '~/schema';
import permissions from '~/permissions';
import { logger } from '~/loggers';
// import sentryPlugin from '~/apolloPlugins/sentry'; // Uncomment this line if you have Sentry set up
import pinoLogger from '~/apolloPlugins/logger';
import { NODE_ENV } from '~/config';

export function createExpressApp() {
  const app = express();

  app.use(
    cors({
      exposedHeaders: ['Authorization'],
    }),
  );

  app.use(
    helmet({
      contentSecurityPolicy: {
        // these directives are required for the Apollo sandbox to work
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

export function createApolloServer(httpServer: http.Server) {
  const graphqlSchema = applyMiddleware(schema, permissions);

  const server = new ApolloServer({
    schema: graphqlSchema,
    introspection: NODE_ENV !== 'production',
    ...(NODE_ENV !== 'test' ? { logger: logger } : {}), // Only add logger if not in test
    plugins: [
      // sentryPlugin,
      ApolloServerPluginDrainHttpServer({ httpServer }),
      ...(NODE_ENV !== 'test' ? [pinoLogger] : []), // Only add pinoLogger if not in test
    ],
  });

  return server;
}
