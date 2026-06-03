import type { Prisma, PrismaClient } from "~/generated/prisma/client.js";

export type PrismaContext = Readonly<{
  prisma: PrismaClient;
  tx?: Prisma.TransactionClient;
}>;

export async function withTransaction<T>({
  prisma,
  tx,
  fn,
}: PrismaContext & {
  fn: (tx: Prisma.TransactionClient) => Promise<T> | T;
}): Promise<T> {
  if (tx) {
    return await fn(tx);
  }
  return await prisma.$transaction(async (newTx) => fn(newTx));
}
