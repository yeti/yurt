import { nanoid } from 'nanoid';
import pino from 'pino';
import { LOG_LEVEL } from '~/config';

export const logger = pino({
  level: LOG_LEVEL || 'info',
  transport: {
    target: 'pino-pretty',
    options: {
      colorize: true,
    },
  },
});
