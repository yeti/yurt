import chalk from 'chalk';
import path from 'path';
import { execSync } from 'child_process';
import { prompt } from 'enquirer';
import fse from 'fs-extra';
import untildify from './utils';

interface PromptInputs {
  repoName: string;
  readmeTitle: string;
  repoLocation: string;
  appType: 'react' | 'react-apollo';
}

const REACT = 'react';
const REACT_APOLLO = 'react-apollo';
const BACKEND = 'backend';

const TEMPLATES = {
  [BACKEND]: 'backend',
  [REACT]: 'react-frontend',
  [REACT_APOLLO]: 'apollo-react-frontend',
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
      { name: 'React/Vite App', value: REACT },
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

  execSync(`cd ${repoAbsolutePath} && rm -rf .git && git init .`, {
    stdio: 'pipe',
  });

  //TODO: add README template
  // Create root readme
  execSync(`echo "# ${readmeTitle}" >> ${repoAbsolutePath}/README.md`, {
    stdio: 'pipe',
  });

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
    `cd ${repoAbsolutePath} && git add --all && git commit --message "Initial commit"`,
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
