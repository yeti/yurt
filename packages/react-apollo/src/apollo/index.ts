import { ApolloClient, InMemoryCache, HttpLink, from } from '@apollo/client';
import { GRAPHQL_URL } from '~/shared/config';

const httpLink = new HttpLink({
  uri: GRAPHQL_URL,
});

const client = new ApolloClient({
  link: from([httpLink]),
  cache: new InMemoryCache(),
});

export default client;
