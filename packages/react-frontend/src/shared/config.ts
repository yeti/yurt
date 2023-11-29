import { z } from 'zod';

const envSchema = z.object({
  VITE_AUTH0_DOMAIN: z.string(),
  VITE_AUTH0_CLIENT_ID: z.string(),
  VITE_AUTH0_AUDIENCE: z.string(),
});

const env = envSchema.parse(import.meta.env);

export const AUTH0_DOMAIN = env.VITE_AUTH0_DOMAIN;
export const AUTH0_CLIENT_ID = env.VITE_AUTH0_CLIENT_ID;
export const AUTH0_AUDIENCE = env.VITE_AUTH0_AUDIENCE;
