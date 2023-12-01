import os from 'node:os';

const homeDirectory = os.homedir();

/**
 * Converts a tilde path (UNIX home) to an absolute path.
 */
export default function untildify(path: string) {
  return homeDirectory ? path.replace(/^~(?=$|\/|\\)/, homeDirectory) : path;
}
