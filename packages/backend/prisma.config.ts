import { config } from "dotenv";
import { defineConfig, env } from "prisma/config";

config();

export default defineConfig({
  schema: "./prisma",
  datasource: { url: env("DATABASE_URL") },
  migrations: {
    path: "./prisma/migrations",
  },
});
