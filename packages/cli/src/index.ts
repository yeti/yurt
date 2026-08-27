import { execSync } from "node:child_process";
import path from "node:path";
import chalk from "chalk";
import { prompt } from "enquirer";
import fse from "fs-extra";
import {
  buildSubstitutions,
  substituteInTree,
  type TerraformSubstitutionInputs,
  validateTerraformInputs,
} from "./substitute";
import untildify from "./utils";

const REACT = "react";
const REACT_YOGA = "react-yoga";
const BACKEND = "backend";
const INFRA = "infra";

const TEMPLATES = {
  [BACKEND]: "backend",
  [INFRA]: "infra",
  [REACT]: "react",
  [REACT_YOGA]: "react-yoga",
};

const prompts = [
  {
    type: "input",
    name: "repoName",
    message: "What should the repo be called?",
    required: true,
  },
  {
    type: "input",
    name: "readmeTitle",
    message: "What should the readme title be? (i.e. project name)",
    initial: "README",
    required: true,
  },
  {
    type: "input",
    name: "repoLocation",
    message: "Where should the repo be created? (absolute or relative path)",
    initial: "~",
    required: true,
  },
  {
    type: "select",
    name: "appType",
    message: "What type of app is this?",
    choices: [
      { name: "Standalone React/Vite App", value: REACT },
      { name: "React/Vite App + Yoga GraphQL server", value: REACT_YOGA },
    ],
    result(_value: string): string {
      // This makes it so that the choice value is returned for appType,
      // instead of the choice name which is the default behavior
      //@ts-expect-error
      return this.focused.value;
    },
  },
];

interface PromptInputs {
  appType: "react" | "react-yoga";
  readmeTitle: string;
  repoLocation: string;
  repoName: string;
}

type TerraformInputs = Pick<
  TerraformSubstitutionInputs,
  "githubOwner" | "hcpOrgName"
>;

const promptForTerraform = async (): Promise<TerraformInputs | undefined> => {
  const { includeTerraform } = await prompt<{ includeTerraform: boolean }>({
    type: "confirm",
    name: "includeTerraform",
    message:
      "Include Terraform infra for Render + Auth0? (HCP Terraform state backend)",
    initial: false,
  });

  if (!includeTerraform) {
    return;
  }

  return await prompt<TerraformInputs>([
    {
      type: "input",
      name: "hcpOrgName",
      message: "HCP Terraform organization name?",
      initial: "yeti-co",
      required: true,
    },
    {
      type: "input",
      name: "githubOwner",
      message: "GitHub owner/org for this repo?",
      initial: "yeti",
      required: true,
    },
  ]);
};

const main = async () => {
  const response: PromptInputs = await prompt(prompts);

  const { repoName, readmeTitle, repoLocation, appType } = response;

  const terraform =
    appType === REACT_YOGA ? await promptForTerraform() : undefined;

  // Fail on values that would break the generated Terraform/envrc files
  // before anything is written to disk.
  if (terraform) {
    validateTerraformInputs({ ...terraform, readmeTitle, repoName });
  }

  const startTime = performance.now();

  const repoLocationAbsolutePath = untildify(repoLocation);
  const repoAbsolutePath = `${repoLocationAbsolutePath}/${repoName}`;

  await fse.mkdirp(repoLocationAbsolutePath);

  const excludedRootDirectories = [
    "packages",
    "node_modules",
    "postgres",
    "README.md",
  ];

  if (appType === REACT) {
    excludedRootDirectories.push("docker-compose.yaml");
    excludedRootDirectories.push("docker-compose.jest.yml");
    excludedRootDirectories.push("pnpm-workspace.yaml");
  }

  console.log(chalk.green("🍳 Creating repo 🍳"));
  // Copy monorepo root files
  fse.cpSync(path.resolve(__dirname, "../../../"), repoAbsolutePath, {
    filter: (src) => {
      if (excludedRootDirectories.some((item) => src.includes(item))) {
        return false;
      }

      return true;
    },
    dereference: true,
    recursive: true,
  });

  // Initialize git repo
  execSync(`cd ${repoAbsolutePath} && rm -rf .git && git init .`, {
    stdio: "pipe",
  });

  const deploymentsIntro = terraform
    ? "We use Render to handle deployments, provisioned via Terraform (HCP Terraform state backend). See [`infra/README.md`](infra/README.md) for the full runbook — start with Phase 1 (accounts and bootstrap) before anything can deploy."
    : "We use Render to handle deployments.";

  // Create root readme
  await fse.appendFile(
    `${repoAbsolutePath}/README.md`,
    `# ${readmeTitle}

> A monorepo managed through [lerna](https://github.com/lerna/lerna) that houses packages related to the ${readmeTitle} project.

## Getting Started

### Install node

\`\`\`bash
nvm install 20.11
\`\`\`

The \`.nvmrc\` file in the root of this project should default to node 20.11 if you run \`nvm use\`.
Confirm that this is the case by running \`node --version\` on the command line.

### Install pnpm

Follow the [pnpm installation instructions](https://pnpm.io/installation).

### Install dependencies

We use [pnpm workspaces](https://pnpm.io/workspaces), which allows for dependency sharing between packages. This allows us to just do a single install at the root folder.

\`\`\`bash
pnpm install
\`\`\`

## Deployments

${deploymentsIntro}

### Staging Deploy

Staging deploys are started automatically when a commit is merged into the \`develop\` branch.

### Production Deploy

Production deploys are started automatically when a commit is merged into the \`main\` branch. Merge with caution!`
  );

  // Create application packages
  switch (appType) {
    case REACT: {
      createReactApp(repoAbsolutePath);
      fse.writeFileSync(
        `${repoAbsolutePath}/pnpm-workspace.yaml`,
        "packages:\n  - packages/*\n"
      );
      break;
    }
    case REACT_YOGA: {
      createReactYogaApp(repoAbsolutePath);
      createGraphQLServer(repoAbsolutePath);
      if (terraform) {
        console.log(chalk.blue("🏗️  Adding Terraform infra (Render + Auth0) 🏗️"));
        createInfra(
          repoAbsolutePath,
          buildSubstitutions({ ...terraform, readmeTitle, repoName })
        );
      }
      break;
    }
    default: {
      throw new Error(`Unknown app type: ${appType}`);
    }
  }

  // Install dependencies after all packages are created
  console.log(chalk.blue("📦 Installing dependencies 📦"));
  installDependencies(repoAbsolutePath);

  // Generate Prisma and GraphQL schemas for backend if it exists
  if (appType === REACT_YOGA) {
    console.log(
      chalk.blue(
        "🔨 Generating Prisma schema, GraphQL schema, and GraphQL types 🔨"
      )
    );
    execSync(`cd ${repoAbsolutePath}/packages/backend && pnpm generate`, {
      stdio: "inherit",
    });
    console.log(
      chalk.green(
        "✅ Prisma schema, GraphQL schema, and GraphQL types generated ✅"
      )
    );
  }

  console.log(chalk.green("📝 Creating initial commit 📝"));
  execSync(
    `
    cd ${repoAbsolutePath} &&
    git add --all &&
    git commit --message "Initial commit" &&
    git branch -M main &&
    git branch develop`,
    { stdio: "pipe" }
  );

  const endTime = performance.now();

  console.log(
    chalk.green(
      `✨ Successfully created ${repoName} in ${(
        (endTime - startTime) / 1000
      ).toFixed(2)}s! ✨`
    )
  );

  if (terraform) {
    console.log(
      chalk.cyan(`
Next steps (Terraform infra):
  1. Read ${repoName}/infra/README.md — Phase 1 bootstrap: Render account +
     API key, HCP Terraform org "${terraform.hcpOrgName}" + 5 workspaces,
     two Auth0 tenants + "Terraform IaC" M2M apps, GitHub Environments + secrets.
  2. Push this repo to https://github.com/${terraform.githubOwner}/${repoName}
     so Render and CI can see it.
  3. Follow Phase 3 in the runbook to apply (render/project first).`)
    );
  }

  process.exit(0);
};

main().catch((error) => {
  console.error(chalk.red(error));

  process.exit(1);
});

// Local-only artifacts a yurt maintainer may have created while testing the
// template (all gitignored there, but still on disk) — never ship them.
const excludedInfraFiles = [
  ".terraform",
  ".terraform.tfstate.lock.info",
  ".envrc",
  "terraform.tfstate",
  "terraform.tfstate.backup",
  "plan_output.txt",
  ".DS_Store",
];

const infraCopyFilter = (src: string): boolean => {
  const basename = path.basename(src);
  // Exact-match basenames so .envrc is excluded but .envrc.example survives,
  // and .terraform/ is excluded but .terraform-version and lock files survive.
  return !(
    excludedInfraFiles.includes(basename) || basename.endsWith(".tfplan")
  );
};

const createInfra = (
  repoAbsolutePath: string,
  tokens: ReturnType<typeof buildSubstitutions>
) => {
  const templateRoot = path.resolve(__dirname, "../../", TEMPLATES[INFRA]);

  // The template root nests an infra/ dir (hence packages/infra/infra) so its
  // contents mirror their destination path in the generated repo, while
  // workflows/ can sit alongside it for its own destination below.
  fse.cpSync(path.join(templateRoot, "infra"), `${repoAbsolutePath}/infra`, {
    dereference: true,
    filter: infraCopyFilter,
    recursive: true,
  });

  // The workflows live outside a .github/ path in the template so they never
  // run in the yurt repo itself; the generated repo gets them in place.
  fse.cpSync(
    path.join(templateRoot, "workflows"),
    `${repoAbsolutePath}/.github/workflows`,
    { dereference: true, filter: infraCopyFilter, recursive: true }
  );

  // Covers everything this function wrote: .github/workflows includes ci.yml
  // from the root copy, which is token-free and left untouched.
  substituteInTree(`${repoAbsolutePath}/infra`, tokens);
  substituteInTree(`${repoAbsolutePath}/.github/workflows`, tokens);
};

const createReactYogaApp = (repoAbsolutePath: string) => {
  const excludedFrontendDirectories = ["node_modules"];

  fse.copySync(
    path.resolve(__dirname, "../../", TEMPLATES[REACT_YOGA]),
    `${repoAbsolutePath}/packages/frontend`,
    {
      filter: (src) => {
        if (excludedFrontendDirectories.some((item) => src.includes(item))) {
          return false;
        }

        return true;
      },
    }
  );

  // Copy .env.example to .env
  fse.cpSync(
    path.resolve(__dirname, "../../", `${TEMPLATES[REACT_YOGA]}/.env.example`),
    `${repoAbsolutePath}/packages/frontend/.env`
  );
};

const createGraphQLServer = (repoAbsolutePath: string) => {
  const excludedBackendDirectories = ["node_modules"];

  fse.cpSync(
    path.resolve(__dirname, "../../", TEMPLATES[BACKEND]),
    `${repoAbsolutePath}/packages/backend`,
    {
      filter: (src) => {
        if (excludedBackendDirectories.some((item) => src.includes(item))) {
          return false;
        }

        return true;
      },
      dereference: true,
      recursive: true,
    }
  );

  // Copy .env.example to .env
  fse.cpSync(
    path.resolve(__dirname, "../../", `${TEMPLATES[BACKEND]}/.env.example`),
    `${repoAbsolutePath}/packages/backend/.env`
  );
};

const createReactApp = (repoAbsolutePath: string) => {
  const excludedFrontendDirectories = ["node_modules"];

  fse.cpSync(
    path.resolve(__dirname, "../../", TEMPLATES[REACT]),
    `${repoAbsolutePath}/packages/frontend`,
    {
      filter: (src) => {
        if (excludedFrontendDirectories.some((item) => src.includes(item))) {
          return false;
        }

        return true;
      },
      recursive: true,
      dereference: true,
    }
  );

  // Copy .env.example to .env
  fse.cpSync(
    path.resolve(__dirname, "../../", `${TEMPLATES[REACT]}/.env.example`),
    `${repoAbsolutePath}/packages/frontend/.env`
  );
};

const installDependencies = (repoAbsolutePath: string) => {
  execSync(`cd ${repoAbsolutePath} &&  pnpm install`, {
    stdio: "inherit",
  });
  console.log(chalk.green("✅ Dependencies installed ✅"));
};
