import "dotenv/config";
import { PrismaPg } from "@prisma/adapter-pg";
import pg from "pg";
import { PrismaClient } from "~/generated/prisma/client";

const pool = new pg.Pool({
  connectionString: process.env.DATABASE_URL,
});
const adapter = new PrismaPg(pool);
const prisma = new PrismaClient({ adapter });

async function main() {
  const alice = await prisma.user.upsert({
    where: { email: "alice@test.com" },
    update: {},
    create: {
      email: "alice@test.com",
      firstName: "Alice",
    },
  });

  const bob = await prisma.user.upsert({
    where: { email: "bob@test.com" },
    update: {},
    create: {
      email: "bob@test.com",
      firstName: "Bob",
    },
  });

  console.log({ alice, bob });
}

main()
  .then(async () => {
    await prisma.$disconnect();
  })
  .catch(async (e) => {
    console.error(e);
    await prisma.$disconnect();
    process.exit(1);
  });
