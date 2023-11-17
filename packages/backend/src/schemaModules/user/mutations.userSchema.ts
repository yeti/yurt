import { extendType, inputObjectType, nonNull } from 'nexus';

export const UserInput = inputObjectType({
  name: 'UserInput',
  nonNullDefaults: {
    input: true,
  },
  definition(t) {
    t.nonNull.string('email');
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
      resolve(_root, { input: { email } }, context) {
        return context.prisma.user.create({
          data: {
            email,
          },
        });
      },
    });
  },
});
