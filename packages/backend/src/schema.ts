import { makeSchema } from 'nexus';
import { NODE_ENV } from '~/config';
import * as types from '~/schemaTypes';
import path from 'path';
import { fileURLToPath } from 'url';

const directoryPath = path.dirname(fileURLToPath(import.meta.url));

export const schema = makeSchema({
  types,
  outputs: {
    schema: path.join(directoryPath, '/../schema.graphql'),
    typegen: path.join(
      directoryPath,
      './shared/types/gen/nexus-typegen/index.d.ts',
    ),
  },
  ...(NODE_ENV === 'development' && {
    contextType: {
      module: path.join(directoryPath, 'context.ts'),
      export: 'Context',
    },
  }),
  shouldExitAfterGenerateArtifacts: process.argv.includes('--nexusTypegen'),
});
