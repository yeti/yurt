import os from 'node:os';

const homeDirectory = os.homedir();

export default function untildify(path: string) {
  return homeDirectory ? path.replace(/^~(?=$|\/|\\)/, homeDirectory) : path;
}
