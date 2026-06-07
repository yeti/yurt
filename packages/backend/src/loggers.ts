import { AsyncLocalStorage } from "node:async_hooks";
import { nanoid } from "nanoid";
import pino, { type Logger } from "pino";
import { LOG_LEVEL } from "~/config";

export const logger = pino({
  level: LOG_LEVEL || "info",
  transport: {
    target: "pino-pretty",
    options: {
      colorize: true,
    },
  },
});

const requestLoggerStore = new AsyncLocalStorage<Logger>();

export function getRequestLogger(): Logger {
  return requestLoggerStore.getStore() ?? logger;
}

export function runWithRequestLogger<T>(fn: () => T): T {
  const child = logger.child({ requestId: nanoid() });

  return requestLoggerStore.run(child, fn);
}
