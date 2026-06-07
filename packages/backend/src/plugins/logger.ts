import type { YogaLogger } from "graphql-yoga";
import { getRequestLogger } from "~/loggers";

const pinoLogger: YogaLogger = {
  error: (message, ...args) => getRequestLogger().error({ message, args }),
  warn: (message, ...args) => getRequestLogger().warn({ message, args }),
  info: (message, ...args) => getRequestLogger().info({ message, args }),
  debug: (message, ...args) => getRequestLogger().debug({ message, args }),
};

export default pinoLogger;
