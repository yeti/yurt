import { makeSchema } from 'nexus';
import { NODE_ENV } from '~/config';
import * as types from '~/schemaTypes';
import path from 'path';

export const schema = makeSchema({
  types,
  outputs: {
    schema: path.join(__dirname, '/../schema.graphql'),
    typegen: path.join(
      __dirname,
      '../node_modules/@types/nexus-typegen/index.d.ts',
    ),
  },
  ...(NODE_ENV === 'development' && {
    contextType: {
      module: path.join(__dirname, 'context.ts'),
      export: 'Context',
    },
  }),
  shouldExitAfterGenerateArtifacts: process.argv.includes('--nexusTypegen'),
});
