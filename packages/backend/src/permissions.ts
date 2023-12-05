import { allow, shield } from 'graphql-shield';
import { NODE_ENV } from '~/config';

const shouldDebug = NODE_ENV === 'development';

const permissions = shield(
  {
    Query: {
      '*': allow,
    },
    Mutation: {
      '*': allow,
    },
  },
  {
    allowExternalErrors: shouldDebug,
    debug: shouldDebug,
  },
);

export default permissions;
