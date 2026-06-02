import { builder } from "~/schema";
import { getRequestLogger } from "~/loggers";
import UserService from "~/services/User/User.service";

const UserInput = builder.inputType("UserInput", {
  fields: (t) => ({
    email: t.string({ required: true }),
    firstName: t.string({ required: false }),
  }),
});

builder.mutationField("createUser", (t) =>
  t.prismaField({
    type: "User",
    args: {
      input: t.arg({ type: UserInput, required: true }),
    },
    resolve: async (_query, _root, { input }, { prisma }) => {
      getRequestLogger().info({ email: input.email }, "Creating user");
      return UserService.create(
        { email: input.email, name: input.firstName ?? undefined },
        { prisma }
      );
    },
  })
);
