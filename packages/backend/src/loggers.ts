import pino from 'pino';
import { LOG_LEVEL } from './config';

// main logger
export const logger = pino({ level: LOG_LEVEL || 'info' });

// child loggers
export const prismaLogger = logger.child({ module: 'prisma' });
export const httpLogger = logger.child({ module: 'http' });
