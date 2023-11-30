import { extendType, inputObjectType, nonNull } from 'nexus';

export const UserInput = inputObjectType({
  name: 'UserInput',
  definition(t) {
    t.nonNull.string('email');
    t.nullable.string('name');
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
      resolve(_root, { input: { email, name } }, { prisma }) {
        return prisma.user.create({
          data: {
            email,
            name,
          },
          select: {
            id: true,
            email: true,
            name: true,
          },
        });
      },
    });
  },
});
