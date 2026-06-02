import { builder } from "~/schema";

builder.prismaObject("User", {
  fields: (t) => ({
    id: t.exposeInt("id", { nullable: false }),
    email: t.exposeString("email", { nullable: false }),
    name: t.exposeString("firstName", { nullable: true }),
  }),
});
