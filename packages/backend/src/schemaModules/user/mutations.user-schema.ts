import { getRequestLogger } from "~/loggers";
import { builder } from "~/schema";
import UserService from "~/services/User/user.service";

const UserInput = builder.inputType("UserInput", {
  fields: (t) => ({
    email: t.string({ required: true }),
    name: t.string({ required: false }),
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
      return await UserService.create(
        { email: input.email, firstName: input.name ?? undefined },
        { prisma }
      );
    },
  })
);
