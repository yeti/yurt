import { graphql, HttpResponse } from 'msw';

export const handlers = [
  graphql.query('GetUser', () => {
    return HttpResponse.json(
      {
        data: {
          user: {
            id: 'abc-123',
            firstName: 'John',
            lastName: 'Maverick',
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
