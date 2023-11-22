import { graphql, HttpResponse } from 'msw';

export const handlers = [
  graphql.query('GetUser', () => {
    return HttpResponse.json(
      {
        data: {
          user: {
            id: 'top-gun-123',
            name: 'Maverick',
            email: 'talk-to-me-goose@aol.com',
          },
        },
      },
      {
        headers: {
          'x-custom-header': 'foo',
        },
      },
    );
  }),
];
