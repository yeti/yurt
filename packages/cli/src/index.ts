import chalk from 'chalk';
import path from 'path';
import { execSync } from 'child_process';
import { prompt } from 'enquirer';
import fse from 'fs-extra';
import untildify from './utils';

const REACT = 'react';
const REACT_APOLLO = 'react-apollo';
const BACKEND = 'backend';

const TEMPLATES = {
  [BACKEND]: 'backend',
  [REACT]: 'react',
  [REACT_APOLLO]: 'react-apollo',
};

const prompts = [
  {
    type: 'input',
    name: 'repoName',
    message: 'What should the repo be called?',
    required: true,
  },
  {
    type: 'input',
    name: 'readmeTitle',
    message: 'What should the readme title be? (i.e. project name)',
    required: true,
  },
  {
    type: 'input',
    name: 'repoLocation',
    message: 'Where should the repo be created? (absolute or relative path)',
    initial: '.',
    required: true,
  },
  {
    type: 'select',
    name: 'appType',
    message: 'What type of app is this?',
    choices: [
      { name: 'Standalone React/Vite App', value: REACT },
      { name: 'React/Vite App + Apollo GraphQL server', value: REACT_APOLLO },
    ],
    result(_value: string): string {
      // This makes it so that the choice value is returned for appType,
      // instead of the choice name which is the default behavior
      //@ts-ignore
      return this.focused.value;
    },
  },
];

interface PromptInputs {
  repoName: string;
  readmeTitle: string;
  repoLocation: string;
  appType: 'react' | 'react-apollo';
}

const main = async () => {
  const response: PromptInputs = await prompt(prompts);

  const startTime = performance.now();

  const { repoName, readmeTitle, repoLocation, appType } = response;

  const repoLocationAbsolutePath = untildify(repoLocation);
  const repoAbsolutePath = `${repoLocationAbsolutePath}/${repoName}`;

  await fse.mkdirp(repoLocationAbsolutePath);

  const excludedRootDirectories = [
    'packages',
    'node_modules',
    'postgres',
    'README.md',
  ];

  if (appType === REACT) {
    excludedRootDirectories.push('docker-compose.yaml');
  }

  console.log(chalk.green('🍳 Creating repo 🍳'));
  // Copy monorepo root files
  fse.cpSync(path.resolve(__dirname, '../../../'), repoAbsolutePath, {
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
    stdio: 'pipe',
  });

  // Create root readme
  await fse.appendFile(
    `${repoAbsolutePath}/README.md`,
    `# ${readmeTitle}

> A monorepo managed through [lerna](https://github.com/lerna/lerna) that houses packages related to the ${readmeTitle} project.

## Getting Started

### Install node

\`\`\`bash
nvm install 18.18.2
\`\`\`

The \`.nvmrc\` file in the root of this project should default to node 18.12 if you run \`nvm use\`.
Confirm that this is the case by running \`node --version\` on the command line.

### Install pnpm

Follow the [pnpm installation instructions](https://pnpm.io/installation).

### Install dependencies

We use [pnpm workspaces](https://pnpm.io/workspaces), which allows for dependency sharing between packages. This allows us to just do a single install at the root folder.

\`\`\`bash
pnpm install
\`\`\`

## Deployments

We use Render to handle deployments.

### Staging Deploy

Staging deploys are started automatically when a commit is merged into the \`develop\` branch.

### Production Deploy

Production deploys are started automatically when a commit is merged into the \`main\` branch. Merge with caution!`,
  );

  // Create application packages
  switch (appType) {
    case REACT: {
      createReactApp(repoAbsolutePath);
      break;
    }
    case REACT_APOLLO: {
      createReactApolloApp(repoAbsolutePath);
      createGraphQLServer(repoAbsolutePath);
      break;
    }
  }

  console.log(chalk.green('📝 Creating initial commit 📝'));
  execSync(
    `
    cd ${repoAbsolutePath} && 
    git add --all && 
    git commit --message "Initial commit" && 
    git branch -M main && 
    git branch develop`,
    { stdio: 'pipe' },
  );

  const endTime = performance.now();

  console.log(
    chalk.green(
      `✨ Successfully created ${repoName} in ${(
        (endTime - startTime) /
        1000
      ).toFixed(2)}s! ✨`,
    ),
  );

  process.exit(0);
};

main().catch((error) => {
  console.error(chalk.red(error));

  process.exit(1);
});

const createReactApolloApp = (repoAbsolutePath: string) => {
  const excludedFrontendDirectories = ['node_modules'];

  fse.copySync(
    path.resolve(__dirname, '../../', TEMPLATES[REACT_APOLLO]),
    `${repoAbsolutePath}/packages/frontend`,
    {
      filter: (src) => {
        if (excludedFrontendDirectories.some((item) => src.includes(item))) {
          return false;
        }

        return true;
      },
    },
  );

  console.log(chalk.blue('📦 Installing frontend dependencies 📦'));
  installDependencies(repoAbsolutePath);
};

const createGraphQLServer = (repoAbsolutePath: string) => {
  const excludedBackendDirectories = ['node_modules'];

  fse.cpSync(
    path.resolve(__dirname, '../../', TEMPLATES[BACKEND]),
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
    },
  );

  // Copy .env.example to .env
  fse.cpSync(
    path.resolve(__dirname, '../../', `${TEMPLATES[BACKEND]}/.env.example`),
    `${repoAbsolutePath}/packages/backend/.env`,
  );

  console.log(chalk.blue('📦 Installing backend dependencies 📦'));
  installDependencies(repoAbsolutePath);

  console.log(
    chalk.blue(
      '🔨 Generating Prisma schema, GraphQL schema, and GraphQL types 🔨',
    ),
  );
  execSync(`cd ${repoAbsolutePath}/packages/backend && pnpm generate`, {
    stdio: 'pipe',
  });
  console.log(
    chalk.green(
      '✅ Prisma schema, GraphQL schema, and GraphQL types generated ✅',
    ),
  );
};

const createReactApp = (repoAbsolutePath: string) => {
  const excludedFrontendDirectories = ['node_modules'];

  fse.cpSync(
    path.resolve(__dirname, '../../', TEMPLATES[REACT]),
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
    },
  );

  console.log(chalk.blue('📦 Installing frontend dependencies 📦'));
  installDependencies(repoAbsolutePath);
};

const installDependencies = (repoAbsolutePath: string) => {
  execSync(`cd ${repoAbsolutePath} &&  pnpm install`, {
    stdio: 'pipe',
  });
  console.log(chalk.green('✅ Dependencies installed ✅'));
};
