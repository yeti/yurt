import { extendType, stringArg } from 'nexus';

export const UserQuery = extendType({
  type: 'Query',
  definition(t) {
    t.field('user', {
      type: 'User',
      args: { userId: stringArg() },
      async resolve(_root, { userId }, { prisma }) {
        return await prisma.user.findUnique({
          where: {
            id: Number(userId),
          },
        });
      },
    });
  },
});
