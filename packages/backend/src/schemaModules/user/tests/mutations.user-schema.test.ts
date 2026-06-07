import { GRAPHQL_PATH } from "~/config";
import prisma from "~/prisma-client";
import { createTestContext, type TestContext } from "~/tests/__helpers";

describe("createUser", () => {
  let ctx: TestContext;

  beforeAll(async () => {
    ctx = await createTestContext();
  });

  // Clean up and close the server
  afterAll(async () => {
    await ctx.stopServer();
  });

  it("should correctly create a new user with the provided email and name", async () => {
    const uniqueEmail = `john${Date.now()}@test.com`;
    const mutationData = {
      query: `
      mutation CreateUser($input: UserInput!) {
        createUser(input: $input) {
          email
          name
          id
        }
      }
    `,
      variables: {
        input: {
          email: uniqueEmail,
          name: "John",
        },
      },
    };

    const response = await ctx.request.post(GRAPHQL_PATH).send(mutationData);

    expect(response.status).toBe(200);
    expect(response.body.data.createUser).toBeDefined();
    expect(response.body.data.createUser.email).toBe(uniqueEmail);
    expect(response.body.data.createUser.name).toBe("John");

    await prisma.user.delete({
      where: { id: response.body.data.createUser.id },
    });
    await prisma.$disconnect();
  });

  it("should not create a user without an email", async () => {
    const mutationData = {
      query: `
      mutation CreateUser($input: UserInput!) {
        createUser(input: $input) {
          id
          email
          name
        }
      }
    `,
      variables: {
        input: {
          name: "Bob",
        },
      },
    };

    const response = await ctx.request.post(GRAPHQL_PATH).send(mutationData);

    expect(response.status).toBe(400);
    expect(response.body.errors).toBeDefined();
    expect(response.body.errors[0].message).toMatch(
      'Variable "$input" got invalid value { name: "Bob" }; Field "email" of required type "String!" was not provided.'
    );
  });
});
