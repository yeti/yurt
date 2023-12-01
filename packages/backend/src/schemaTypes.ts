import { z } from 'zod';
import { objectType, scalarType } from 'nexus';
import { Kind } from 'graphql';

const stringSchema = z.string();
const dateSchema = z.date();

export * from './schemaModules/user';

export const Query = objectType({
  name: 'Query',
  definition() {
    null;
  },
});

export const Mutation = objectType({
  name: 'Mutation',
  definition() {
    null;
  },
});

export const DateScalar = scalarType({
  name: 'Date',
  asNexusMethod: 'date',
  description: 'Date custom scalar type',
  parseValue(value) {
    return new Date(stringSchema.parse(value));
  },
  serialize(value) {
    return dateSchema.parse(value).getTime();
  },
  parseLiteral(ast) {
    if (ast.kind === Kind.INT) {
      return new Date(ast.value);
    }
    return null;
  },
});
