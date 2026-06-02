import { PrismaPg } from "@prisma/adapter-pg";
import pg from "pg";
import { DATABASE_URL } from "~/config";
import { PrismaClient } from "~/generated/prisma/client.js";

const pool = new pg.Pool({
  connectionString: DATABASE_URL,
  max: 20,
  idleTimeoutMillis: 30_000,
  connectionTimeoutMillis: 2000,
});

const adapter = new PrismaPg(pool);

const prisma = new PrismaClient({
  adapter,
  log:
    process.env.NODE_ENV === "development"
      ? ["query", "error", "warn"]
      : ["error"],
});

export default prisma;
