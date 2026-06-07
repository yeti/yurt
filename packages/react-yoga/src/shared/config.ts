import { z } from "zod";

const envSchema = z.object({
  VITE_GRAPHQL_URL: z.string(),
});

const env = envSchema.parse(import.meta.env);

export const GRAPHQL_URL = env.VITE_GRAPHQL_URL;
