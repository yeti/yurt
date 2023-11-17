import chalk from 'chalk';
import path from 'path';
import { execSync } from 'child_process';
import { prompt } from 'enquirer';
import fs from 'fs-extra';

interface PromptInputs {
  repoName: string;
  readmeTitle: string;
  repoLocation: string;
  needsFrontend: boolean;
  needsBackend: boolean;
}

const main = async () => {
  const response: PromptInputs = await prompt([
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
      message: 'Where should the repo be created? (relative path)',
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
  ]);

  const { repoName, readmeTitle, repoLocation, needsFrontend, needsBackend } =
    response;

  if (!needsFrontend && !needsBackend) {
    console.error(
      chalk.red('You must select at least one of frontend or backend'),
    );

    process.exit(1);
  }

  await fs.mkdirp(`${repoLocation}/${repoName}`);

  fs.copySync(
    path.resolve(__dirname, '../../../'),
    `${repoLocation}/${repoName}/`,
    {
      filter: (src, _dest) => {
        if (src.includes('packages')) {
          return false;
        }

        return true;
      },
    },
  );

  execSync(`cd ${repoLocation}/${repoName} && rm -r ./.git && git init `, {
    stdio: 'pipe',
  });
  execSync(`echo "#${readmeTitle}" >> ${repoLocation}/${repoName}/README.md`, {
    stdio: 'pipe',
  });

  if (needsFrontend) {
    fs.copySync(
      path.resolve(__dirname, '../../', 'frontend'),
      `${repoLocation}/${repoName}/packages/frontend`,
    );
  }

  if (needsBackend) {
    //TODO: Add backend files
  }

  execSync(`cd ${repoLocation}/${repoName}`, { stdio: 'pipe' });
  execSync(`git add .`, { stdio: 'pipe' });
  execSync(`git commit -m "Initial commit"`, { stdio: 'pipe' });

  console.log(chalk.green('✨ Done! ✨'));
  process.exit(0);
};

main().catch((err) => {
  console.error(chalk.red(err));

  process.exit(1);
});
