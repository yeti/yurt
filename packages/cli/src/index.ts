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
      message: 'Where should the repo be created?',
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

  await fs.mkdirp(`${process.cwd()}/${repoLocation}/${repoName}`);
  execSync(`cd ${repoLocation}/${repoName} && git init `, { stdio: 'pipe' });
  execSync(`echo "#${readmeTitle}" >> README.md`, { stdio: 'pipe' });
  // && echo "# ${readmeTitle}" >> README.md && git add . && git commit -m "Initial commit"

  if (needsFrontend) {
    fs.copySync(
      path.resolve(__dirname, '../../', 'frontend'),
      `${repoLocation}/${repoName}/packages/frontend`,
    );
    // await Promise.all([
    //   fs.mkdirp(`${repoLocation}/${repoName}/packages/frontend/public`),
    //   fs.mkdirp(`${repoLocation}/${repoName}/packages/frontend/src/apollo`),
    //   fs.mkdirp(`${repoLocation}/${repoName}/packages/frontend/src/assets`),
    //   fs.mkdirp(`${repoLocation}/${repoName}/packages/frontend/src/modules`),
    //   fs.mkdirp(`${repoLocation}/${repoName}/packages/frontend/src/services`),
    //   fs.mkdirp(
    //     `${repoLocation}/${repoName}/packages/frontend/src/shared/components`,
    //   ),
    //   fs.mkdirp(
    //     `${repoLocation}/${repoName}/packages/frontend/src/shared/types`,
    //   ),
    //   fs.mkdirp(
    //     `${repoLocation}/${repoName}/packages/frontend/src/shared/hooks`,
    //   ),
    //   fs.mkdirp(
    //     `${repoLocation}/${repoName}/packages/frontend/src/shared/mutations`,
    //   ),
    //   fs.mkdirp(
    //     `${repoLocation}/${repoName}/packages/frontend/src/shared/queries`,
    //   ),
    //   fs.mkdirp(
    //     `${repoLocation}/${repoName}/packages/frontend/src/shared/styles`,
    //   ),
    //   fs.mkdirp(
    //     `${repoLocation}/${repoName}/packages/frontend/src/shared/types`,
    //   ),
    //   fs.mkdirp(
    //     `${repoLocation}/${repoName}/packages/frontend/src/static/icons`,
    //   ),
    //   fs.mkdirp(`${repoLocation}/${repoName}/packages/frontend/src/stores`),
    //   fs.mkdirp(`${repoLocation}/${repoName}/packages/frontend/src/tests`),
    // ]);

    //TODO: Add frontend files
  }

  if (needsBackend) {
    //TODO: Add backend files
  }
};

main().catch((err) => {
  console.error(chalk.red(err));

  process.exit(1);
});
