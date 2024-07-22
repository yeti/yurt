import { createTestContext, TestContext } from '~/tests/__helpers';
import { GRAPHQL_PATH } from '~/config';
import prisma from '~/prismaClient';

describe('user', () => {
  let ctx: TestContext;

  beforeAll(async () => {
    ctx = await createTestContext();
  });

  // Clean up and close the server
  afterAll(async () => {
    await ctx.stopServer();
  });

  it("should return the user's email for a given userId", async () => {
    const uniqueEmail = `alice${Date.now()}@test.com`;
    const user = await prisma.user.create({
      data: {
        email: uniqueEmail,
        name: 'Alice',
      },
    });

    const queryData = {
      query: `
      query User($userId: Int!) {
        user(userId: $userId) {
          email
        }
      }
    `,
      variables: { userId: user.id },
    };

    const response = await ctx.request.post(GRAPHQL_PATH).send(queryData);

    expect(response.status).toBe(200);
    expect(response.body.data.user).toBeDefined();
    expect(response.body.data.user.email).toBe(user.email);
    await prisma.user.delete({ where: { id: user.id } });
    await prisma.$disconnect();
  });

  it('should handle non-existing userId gracefully', async () => {
    const queryData = {
      query: `
      query User($userId: Int!) {
        user(userId: $userId) {
          email
        }
      }
    `,
      variables: { userId: 999 },
    };

    const response = await ctx.request.post(GRAPHQL_PATH).send(queryData);

    expect(response.status).toBe(200);
    expect(response.body.data.user).toBeNull();
  });
});
