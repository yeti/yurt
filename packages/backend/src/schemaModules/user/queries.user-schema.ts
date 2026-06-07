import { getRequestLogger } from "~/loggers";
import { builder } from "~/schema";
import UserService from "~/services/User/user.service";

builder.queryField("user", (t) =>
  t.prismaField({
    type: "User",
    nullable: true,
    args: {
      userId: t.arg.int({ required: true }),
    },
    resolve: async (_query, _root, { userId }, { prisma }) => {
      getRequestLogger().info({ userId }, "Fetching user by ID");

      return await UserService.findById(userId, { prisma });
    },
  })
);
