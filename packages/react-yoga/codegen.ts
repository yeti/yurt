import type { CodegenConfig } from "@graphql-codegen/cli";

const config: CodegenConfig = {
  schema: "../backend/schema.graphql",
  documents: ["src/graphql/**/*.ts"],
  generates: {
    "./src/graphql/gen/graphql.ts": {
      plugins: [
        "typescript",
        "typescript-operations",
        "typescript-react-apollo",
      ],
      config: {
        withHooks: true,
        scalars: {
          DateTime: "string",
        },
        maybeValue: "T | null",
      },
    },
  },
};

export default config;
