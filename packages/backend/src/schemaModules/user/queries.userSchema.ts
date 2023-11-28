import { extendType, intArg, nonNull } from 'nexus';

export const UserQuery = extendType({
  type: 'Query',
  definition(t) {
    t.field('user', {
      type: 'User',
      args: { userId: nonNull(intArg()) },
      async resolve(_root, { userId }, { prisma }) {
        return await prisma.user.findUnique({
          where: {
            id: Number(userId),
          },
          select: {
            id: true,
            email: true,
          },
        });
      },
    });
  },
});
