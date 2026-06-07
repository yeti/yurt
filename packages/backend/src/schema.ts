import SchemaBuilder from "@pothos/core";
import PrismaPlugin from "@pothos/plugin-prisma";
import ScopeAuthPlugin from "@pothos/plugin-scope-auth";
import { Kind } from "graphql";
import type { Context } from "~/context";
import type PrismaTypes from "~/generated/pothos-types";
import { getDatamodel } from "~/generated/pothos-types";
import {
  type AuthScopes,
  defaultMutationScopes,
  defaultQueryScopes,
  getAuthScopes,
} from "~/permissions";
import prisma from "~/prisma-client";

export const builder = new SchemaBuilder<{
  PrismaTypes: PrismaTypes;
  Context: Context;
  Scalars: {
    Date: { Input: Date; Output: Date };
  };
  AuthScopes: AuthScopes;
}>({
  plugins: [ScopeAuthPlugin, PrismaPlugin],
  prisma: {
    client: prisma,
    dmmf: getDatamodel(),
  },
  scopeAuth: {
    authScopes: async () => getAuthScopes(),
  },
});

builder.scalarType("Date", {
  description: "Date custom scalar type",
  serialize: (value: Date) => value.getTime(),
  parseValue: (value: unknown) => {
    if (typeof value === "number") {
      return new Date(value);
    }
    if (typeof value === "string") {
      return new Date(value);
    }
    throw new Error("Invalid Date input");
  },
  parseLiteral: (ast) => {
    if (ast.kind === Kind.INT) {
      return new Date(Number.parseInt(ast.value, 10));
    }
    throw new Error("Invalid Date literal");
  },
});

builder.queryType({
  authScopes: defaultQueryScopes,
});

builder.mutationType({
  authScopes: defaultMutationScopes,
});
