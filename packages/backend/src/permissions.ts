import { rule, shield } from 'graphql-shield';
import { NODE_ENV } from './config';

const isAuthenticated = rule({ cache: 'contextual' })(async (
  _parent,
  _args,
  { user },
) => {
  return Boolean(user);
});

const isAdmin = rule({ cache: 'contextual' })(async (
  _parent,
  _args,
  { user, isAdmin },
) => {
  if (user !== null) {
    return isAdmin;
  }
});

const shouldDebug = NODE_ENV === 'development';

const permissions = shield(
  {
    Query: {},
    Mutation: {},
  },
  {
    fallbackRule: isAuthenticated,
    allowExternalErrors: shouldDebug,
    debug: shouldDebug,
  },
);

export default permissions;
