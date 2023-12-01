import type { ApolloServerPlugin } from '@apollo/server';
import { Context } from '~/context';
import { logger } from '~/loggers';

const pinoLogger: ApolloServerPlugin<Context> = {
  async requestDidStart(ctx) {
    //@ts-ignore
    ctx.logger = logger;

    if (ctx.request.operationName === 'IntrospectionQuery') {
      return;
    }

    ctx.logger.info({
      operationName: ctx.request.operationName,
      query: ctx.request.query,
      variables: ctx.request.variables,
    });

    return {
      async didEncounterErrors({ logger, errors }) {
        errors.forEach((error) => logger.warn(error));
      },
    };
  },
};

export default pinoLogger;
