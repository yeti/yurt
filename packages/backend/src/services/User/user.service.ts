import { type PrismaContext, withTransaction } from "~/shared/withTransaction";

class UserService {
  findById(id: number, { prisma }: PrismaContext) {
    return prisma.user.findUnique({
      where: { id },
    });
  }

  create(
    data: { email: string; name?: string },
    { prisma, tx }: PrismaContext
  ) {
    return withTransaction({
      prisma,
      tx,
      fn: (client) =>
        client.user.create({
          data,
        }),
    });
  }
}

export default new UserService();
