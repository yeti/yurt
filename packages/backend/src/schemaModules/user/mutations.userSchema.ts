import { extendType, inputObjectType, nonNull } from 'nexus';

export const UserInput = inputObjectType({
  name: 'UserInput',
  definition(t) {
    t.nonNull.string('email');
    t.string('name');
  },
});

export const UserMutation = extendType({
  type: 'Mutation',
  definition(t) {
    t.nonNull.field('createUser', {
      type: 'User',
      args: {
        input: nonNull(UserInput),
      },
      resolve(_root, { input: { email } }, { prisma }) {
        return prisma.user.create({
          data: {
            email,
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
