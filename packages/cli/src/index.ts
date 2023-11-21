import chalk from 'chalk';
import path from 'path';
import { execSync } from 'child_process';
import { prompt } from 'enquirer';
import fs from 'fs-extra';
import untildify from './utils';

interface PromptInputs {
  repoName: string;
  readmeTitle: string;
  repoLocation: string;
  needsFrontend: boolean;
  needsBackend: boolean;
}

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
    type: 'confirm',
    name: 'needsFrontend',
    message: 'Does the repo need a frontend?',
    required: true,
  },
  {
    type: 'confirm',
    name: 'needsBackend',
    message: 'Does the repo need a backend?',
    required: true,
  },
];

const main = async () => {
  const response: PromptInputs = await prompt(prompts);

  const startTime = performance.now();

  const { repoName, readmeTitle, repoLocation, needsFrontend, needsBackend } =
    response;

  if (!needsFrontend && !needsBackend) {
    console.error(
      chalk.red('You must select at least one of frontend or backend'),
    );

    process.exit(1);
  }

  const absolutePath = untildify(repoLocation);

  await fs.mkdirp(absolutePath);

  const excludedRootDirectories = [
    'packages',
    'node_modules',
    'postgres',
    '.git',
  ];

  fs.copySync(
    //TODO: resolve this path properly when command is invoked
    path.resolve(__dirname, '../../../'),
    `${repoLocation}/${repoName}/`,
    {
      filter: (src) => {
        if (excludedRootDirectories.some((item) => src.includes(item))) {
          return false;
        }

        return true;
      },
    },
  );

  execSync(`cd ${repoLocation}/${repoName} && git init `, {
    stdio: 'pipe',
  });

  // Create root readme
  execSync(`echo "# ${readmeTitle}" >> ${repoLocation}/${repoName}/README.md`, {
    stdio: 'pipe',
  });

  if (needsFrontend) {
    const excludedFrontendDirectories = ['node_modules'];

    fs.copySync(
      path.resolve(__dirname, '../../', 'frontend'),
      `${repoLocation}/${repoName}/packages/frontend`,
      {
        filter: (src) => {
          if (excludedFrontendDirectories.some((item) => src.includes(item))) {
            return false;
          }

          return true;
        },
      },
    );
  }

  if (needsBackend) {
    const excludedBackendDirectories = ['node_modules'];

    fs.copySync(
      path.resolve(__dirname, '../../', 'backend'),
      `${repoLocation}/${repoName}/packages/backend`,
      {
        filter: (src) => {
          if (excludedBackendDirectories.some((item) => src.includes(item))) {
            return false;
          }

          return true;
        },
      },
    );
  }

  execSync(
    `cd ${repoLocation}/${repoName} && git add --all && git commit --message "Initial commit"`,
    { stdio: 'pipe' },
  );

  console.log(chalk.green('📦 Installing dependencies...'));
  execSync(`cd ${repoLocation}/${repoName} &&  pnpm install`, {
    stdio: 'pipe',
  });

  console.log(chalk.green('🔨 Generating GraphQL schema and types...'));
  execSync(`cd ${repoLocation}/${repoName}/packages/backend && pnpm generate`, {
    stdio: 'pipe',
  });

  const endTime = performance.now();

  console.log(
    chalk.green(
      `🚀 Successfully created ${repoName} in ${(
        (endTime - startTime) /
        1000
      ).toFixed(2)}s!`,
    ),
  );

  console.log(chalk.green('✨ Done! ✨'));
  process.exit(0);
};

main().catch((err) => {
  console.error(chalk.red(err));

  process.exit(1);
});
