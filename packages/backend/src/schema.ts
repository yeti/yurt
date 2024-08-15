import { makeSchema } from 'nexus';
import { NODE_ENV } from '~/config';
import * as types from '~/schemaTypes';
import path from 'path';

const rootDir = process.cwd();

export const schema = makeSchema({
  types,
  outputs: {
    schema: path.join(rootDir, '/schema.graphql'),
    typegen: path.join(
      rootDir,
      '/src/shared/types/gen/nexus-typegen/index.d.ts',
    ),
  },
  ...(NODE_ENV === 'development' && {
    contextType: {
      module: path.join(rootDir, '/src/context.ts'),
      export: 'Context',
    },
  }),
  shouldExitAfterGenerateArtifacts: process.argv.includes('--nexusTypegen'),
});
