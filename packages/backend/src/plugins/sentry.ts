import { captureException, withScope } from "@sentry/node";
import type { ExecutionArgs, GraphQLError } from "graphql";
import type { Plugin } from "graphql-yoga";
import type { Context } from "~/context";

function captureGraphQLError(error: GraphQLError, args: ExecutionArgs): void {
  withScope((scope) => {
    scope.setTag("kind", args.operationName || "unknown");
    if (args.document) {
      scope.setExtra("query", args.document);
    }
    if (error.path) {
      scope.addBreadcrumb({
        category: "query-path",
        message: error.path.join(" > "),
        level: "debug",
      });
    }
    if (args.contextValue) {
      const context = args.contextValue as Context;
      const transactionId = context.headers["x-transaction-id"];
      if (transactionId) {
        scope.setTransactionName(String(transactionId));
      }
    }
    captureException(error);
  });
}

const sentryPlugin: Plugin<Context> = {
  onExecute({ args }) {
    return {
      onExecuteDone({ result }) {
        if ("errors" in result && result.errors) {
          for (const error of result.errors) {
            captureGraphQLError(error, args);
          }
        }
      },
    };
  },
};

export default sentryPlugin;
