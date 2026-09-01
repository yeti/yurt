import path from "node:path";
import fse from "fs-extra";

export interface TerraformSubstitutionInputs {
  githubOwner: string;
  hcpOrgName: string;
  readmeTitle: string;
  repoName: string;
}

const TOKENS = [
  "__YURT_API_IDENTIFIER__",
  "__YURT_HCP_ORG__",
  "__YURT_PROJECT_NAME__",
  "__YURT_PROJECT_SLUG__",
  "__YURT_PROJECT_SLUG_UNDERSCORE__",
  "__YURT_REPO_URL__",
] as const;

export type SubstitutionTokens = Record<(typeof TOKENS)[number], string>;

const TOKEN_PATTERN = /__YURT_[A-Z0-9_]+__/;
const SAFE_TITLE_PATTERN = /^[A-Za-z0-9 ._-]+$/;
const SAFE_IDENTIFIER_PATTERN = /^[A-Za-z0-9_-]+$/;

const deriveSlug = (repoName: string): string =>
  repoName
    .toLowerCase()
    .replace(/[^a-z0-9-]+/g, "-")
    .replace(/^-+|-+$/g, "");

// The substituted values land inside HCL string literals, shell single-quotes
// (the op:// paths in .envrc.example), and cloud resource names, so reject
// anything that would break that quoting rather than trying to escape it.
export const validateTerraformInputs = (
  inputs: TerraformSubstitutionInputs
): void => {
  if (deriveSlug(inputs.repoName).length === 0) {
    throw new Error(
      `Repo name "${inputs.repoName}" contains no usable characters (a-z, 0-9, -) — the Terraform workspace and database names derived from it would be empty.`
    );
  }

  if (!SAFE_TITLE_PATTERN.test(inputs.readmeTitle)) {
    throw new Error(
      `Readme title "${inputs.readmeTitle}" can only contain letters, numbers, spaces, and ._- when Terraform infra is included — it is used in Terraform strings, resource names, and 1Password paths.`
    );
  }

  for (const [label, value] of [
    ["HCP organization", inputs.hcpOrgName],
    ["GitHub owner", inputs.githubOwner],
  ] as const) {
    if (!SAFE_IDENTIFIER_PATTERN.test(value)) {
      throw new Error(
        `${label} "${value}" can only contain letters, numbers, hyphens, and underscores.`
      );
    }
  }
};

// Derives every template token from the prompt answers. The API identifier is
// substituted as a single token so the value in the auth0 root modules always
// matches the claim namespace hardcoded in post-login-action.js (the tenant
// module's lifecycle precondition enforces that they agree).
export const buildSubstitutions = (
  inputs: TerraformSubstitutionInputs
): SubstitutionTokens => {
  validateTerraformInputs(inputs);
  const slug = deriveSlug(inputs.repoName);

  return {
    __YURT_API_IDENTIFIER__: `https://${slug}-api`,
    __YURT_HCP_ORG__: inputs.hcpOrgName,
    __YURT_PROJECT_NAME__: inputs.readmeTitle,
    __YURT_PROJECT_SLUG__: slug,
    __YURT_PROJECT_SLUG_UNDERSCORE__: slug.replace(/-/g, "_"),
    __YURT_REPO_URL__: `https://github.com/${inputs.githubOwner}/${inputs.repoName}`,
  };
};

const walkFiles = (dir: string): string[] => {
  const entries = fse.readdirSync(dir, { withFileTypes: true });

  return entries.flatMap((entry) => {
    const fullPath = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      return walkFiles(fullPath);
    }

    return entry.isFile() ? [fullPath] : [];
  });
};

// Replaces every token in every file under rootDir (all template files are
// text), asserting that no token remains — a template typo (or a token missing
// from the map) fails generation loudly, before the broken file is written.
export const substituteInTree = (
  rootDir: string,
  tokens: SubstitutionTokens
): void => {
  for (const filePath of walkFiles(rootDir)) {
    const original = fse.readFileSync(filePath, "utf8");
    let updated = original;

    for (const [token, value] of Object.entries(tokens)) {
      updated = updated.split(token).join(value);
    }

    const leftover = updated.match(TOKEN_PATTERN);
    if (leftover) {
      throw new Error(
        `Unsubstituted template token ${leftover[0]} in ${filePath}`
      );
    }

    if (updated !== original) {
      fse.writeFileSync(filePath, updated);
    }
  }
};
