import { makeSchema } from 'nexus';
import { NODE_ENV } from '~/config';
import * as types from '~/schemaTypes';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

export const schema = makeSchema({
  types,
  outputs: {
    schema: path.join(__dirname, '/../schema.graphql'),
    typegen: path.join(
      __dirname,
      './shared/types/gen/nexus-typegen/index.d.ts',
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
