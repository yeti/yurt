import { nanoid } from 'nanoid';
import pino from 'pino';
import { LOG_LEVEL } from '~/config';

export const logger = pino({
  //TODO: log request id with every log
  requestId: nanoid(),
  level: LOG_LEVEL || 'info',
  transport: {
    target: 'pino-pretty',
    options: {
      colorize: true,
    },
  },
});
