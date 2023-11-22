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

  const repoLocationAbsolutePath = untildify(repoLocation);
  const repoAbsolutePath = `${repoLocationAbsolutePath}/${repoName}`;

  await fse.mkdirp(repoLocationAbsolutePath);

  const excludedRootDirectories = ['packages', 'node_modules', 'postgres'];

  console.log(chalk.green('📦 Creating repo 📦'));
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

  if (needsFrontend) {
    const excludedFrontendDirectories = ['node_modules'];

    fse.copySync(
      path.resolve(__dirname, '../../', 'frontend'),
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
  }

  if (needsBackend) {
    const excludedBackendDirectories = ['node_modules'];

    fse.copySync(
      path.resolve(__dirname, '../../', 'backend'),
      `${repoAbsolutePath}/packages/backend`,
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

  console.log(chalk.green('📦 Installing dependencies 📦'));
  execSync(`cd ${repoAbsolutePath} &&  pnpm install`, {
    stdio: 'pipe',
  });

  if (needsBackend) {
    console.log(
      chalk.green(
        '🔨 Generating Prisma schema, GraphQL schema, and GraphQL types 🔨',
      ),
    );
    execSync(`cd ${repoAbsolutePath}/packages/backend && pnpm generate`, {
      stdio: 'pipe',
    });
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
