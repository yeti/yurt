import * as Sentry from '@sentry/node';
import { Context } from '~/context';
import {
  ApolloServerPlugin,
  GraphQLRequestContextDidEncounterErrors,
} from '@apollo/server';

const sentryPlugin: ApolloServerPlugin<Context> = {
  async requestDidStart() {
    return {
      didEncounterErrors: async (
        ctx: GraphQLRequestContextDidEncounterErrors<Context>,
      ) => {
        if (!ctx.operation) {
          return;
        }

        for (const err of ctx.errors) {
          // Add scoped report details and send to Sentry
          Sentry.withScope((scope) => {
            // Annotate whether failing operation was query/mutation/subscription
            scope.setTag('kind', ctx.operation?.operation);

            // Log query
            scope.setExtra('query', ctx.request.query);

            if (err.path) {
              scope.addBreadcrumb({
                category: 'query-path',
                message: err.path.join(' > '),
                level: 'debug',
              });
            }

            const transactionId =
              ctx.request.http?.headers.get('x-transaction-id');
            if (transactionId) {
              scope.setTransactionName(transactionId);
            }

            Sentry.captureException(err);
          });
        }
      },
    };
  },
};

export default sentryPlugin;
