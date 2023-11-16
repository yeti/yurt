import { exec, execSync } from 'child_process';
import { prompt } from 'enquirer';
// import ProgressBar from "progress";
import fs from 'fs-extra';

interface PromptInputs {
  repoName: string;
  repoLocation: string;
  needsFrontend: boolean;
  needsBackend: boolean;
}

const main = async () => {
  // const bar = new ProgressBar(":bar", { total: 100 });

  const response: PromptInputs = await prompt([
    {
      type: 'input',
      name: 'repoName',
      message: 'What should the repo be called?',
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

  console.log(response);

  const { repoName, repoLocation, needsFrontend, needsBackend } = response;

  await fs.mkdirp(`${repoLocation}/${repoName}`);

  execSync(
    `cd ${repoLocation}/${repoName} && git init && echo "# ${repoName}" >> README.md && git add . && git commit -m "Initial commit"`,
    { stdio: 'pipe' },
  );

  // setInterval(() => {
  //   bar.tick();
  //   if (bar.complete) {
  //     console.log("\ncomplete\n");
  //     process.exit();
  //   }
  // }, 100);
};

main();
