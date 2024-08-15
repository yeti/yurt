import { makeSchema } from 'nexus';
import { NODE_ENV } from '~/config';
import * as types from '~/schemaTypes';
import path from 'path';

const packageRootDir = process.cwd();

export const schema = makeSchema({
  types,
  outputs: {
    schema: path.join(packageRootDir, '/schema.graphql'),
    typegen: path.join(
      packageRootDir,
      '/src/shared/types/gen/nexus-typegen/index.d.ts',
    ),
  },
  ...(NODE_ENV === 'development' && {
    contextType: {
      module: path.join(packageRootDir, '/src/context.ts'),
      export: 'Context',
    },
  }),
  shouldExitAfterGenerateArtifacts: process.argv.includes('--nexusTypegen'),
});
