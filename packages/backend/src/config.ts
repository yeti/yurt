import 'dotenv/config';
import { z } from 'zod';

const envSchema = z.object({
  NODE_ENV: z.string(),
  PORT: z.string(),
  LOG_LEVEL: z.string(),
  DATABASE_URL: z.string().url(),
});

const env = envSchema.parse(process.env);

export const NODE_ENV = env.NODE_ENV;
export const PORT = env.PORT;
export const LOG_LEVEL = env.LOG_LEVEL;
export const DATABASE_URL = env.DATABASE_URL;
