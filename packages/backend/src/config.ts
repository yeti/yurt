import 'dotenv/config';
import { z } from 'zod';

const envSchema = z.object({
  DATABASE_URL: z.string().url(),
  LOG_LEVEL: z.string(),
  NODE_ENV: z.string(),
  PORT: z.string(),
  GRAPHQL_PATH: z.string(),
});

const env = envSchema.parse(process.env);

export const DATABASE_URL = env.DATABASE_URL;
export const LOG_LEVEL = env.LOG_LEVEL;
export const NODE_ENV = env.NODE_ENV;
export const PORT = env.PORT;
export const GRAPHQL_PATH = env.GRAPHQL_PATH;
