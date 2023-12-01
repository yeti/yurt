import { gql } from '@apollo/client';

export const GET_USER = gql`
  query GetUser($userId: Int!) {
    user(userId: $userId) {
      id
      email
      name
    }
  }
`;
