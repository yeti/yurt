import { gql } from '@apollo/client';

export const USER_QUERY = gql`
  query User($userId: Int!) {
    user(userId: $userId) {
      id
      email
      name
    }
  }
`;
