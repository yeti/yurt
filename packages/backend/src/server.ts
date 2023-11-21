import { ApolloServer } from '@apollo/server';
import { startStandaloneServer } from '@apollo/server/standalone';
import { applyMiddleware } from 'graphql-middleware';
import { logger } from '~/loggers';
import { createContext } from '~/context';
import { schema } from '~/schema';
import { NODE_ENV, PORT } from '~/config';
import permissions from '~/permissions';

// Apollo server
// ----------------------------------------------------------------------------
async function start() {
  const graphqlPath = 'api/graphql';
  const graphqlSchema = applyMiddleware(schema, permissions);

  const server = new ApolloServer({
    schema: graphqlSchema,
    introspection: NODE_ENV !== 'production',
    logger: logger,
  });

  const { url } = await startStandaloneServer(server, {
    context: createContext,
    listen: {
      path: graphqlPath,
      port: Number(PORT),
    },
  });

  logger.info(`🚀 Server ready at ${url}${graphqlPath}`);
}

start();
