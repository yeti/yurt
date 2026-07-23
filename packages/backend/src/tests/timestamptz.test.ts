import { readdirSync, readFileSync } from "node:fs";
import path from "node:path";

/**
 * Enforces the convention that every Prisma `DateTime` column is stored as
 * `timestamptz` (via `@db.Timestamptz`) rather than Prisma's default `timestamp
 * without time zone`.
 */

const SCHEMA_DIR = path.resolve(import.meta.dirname, "../../prisma");
const MIGRATIONS_SEGMENT = `${path.sep}migrations${path.sep}`;
const BLOCK_OPEN = /^(?:model|type)\s+\w+\s*\{/;
const TYPE_MODIFIER = /(?:\?|\[])$/;
const TIMESTAMPTZ = /@db\.Timestamptz/;
const WHITESPACE = /\s+/;

interface DateTimeColumn {
  field: string;
  file: string;
  isTimestamptz: boolean;
  line: number;
}

function findPrismaSchemaFiles(dir: string): string[] {
  return readdirSync(dir, { recursive: true, withFileTypes: true })
    .filter((entry) => entry.isFile() && entry.name.endsWith(".prisma"))
    .map((entry) => path.join(entry.parentPath, entry.name))
    .filter((file) => !file.includes(MIGRATIONS_SEGMENT));
}

function stripComment(line: string): string {
  const commentStart = line.indexOf("//");
  return commentStart === -1 ? line : line.slice(0, commentStart);
}

function collectDateTimeColumns(): DateTimeColumn[] {
  const columns: DateTimeColumn[] = [];

  for (const file of findPrismaSchemaFiles(SCHEMA_DIR)) {
    const lines = readFileSync(file, "utf8").split("\n");
    let insideModel = false;

    for (const [index, rawLine] of lines.entries()) {
      const line = stripComment(rawLine).trim();
      if (line === "") {
        continue;
      }

      // Only `model`/`type` bodies hold typed fields; skip datasource,
      // generator, and enum blocks so their contents can never match.
      if (BLOCK_OPEN.test(line)) {
        insideModel = true;
        continue;
      }

      if (line === "}") {
        insideModel = false;
        continue;
      }

      if (!insideModel) {
        continue;
      }

      const tokens = line.split(WHITESPACE);
      if (tokens.length < 2) {
        continue;
      }

      // A field's type is its second token; strip any `?`/`[]` modifier.
      const [field, rawType] = tokens;
      if (rawType.replace(TYPE_MODIFIER, "") !== "DateTime") {
        continue;
      }

      columns.push({
        field,
        file: path.relative(SCHEMA_DIR, file),
        isTimestamptz: TIMESTAMPTZ.test(line),
        line: index + 1,
      });
    }
  }

  return columns;
}

describe("Prisma DateTime columns", () => {
  it("reads the prisma schema (sanity guard)", () => {
    // Guards against a broken path.
    expect(findPrismaSchemaFiles(SCHEMA_DIR).length).toBeGreaterThan(0);
  });

  it("uses @db.Timestamptz for every DateTime column", () => {
    const offenders = collectDateTimeColumns()
      .filter((column) => !column.isTimestamptz)
      .map((column) => `${column.file}:${column.line} ${column.field}`);

    expect(
      offenders,
      `DateTime columns must be timestamptz. Add \`@db.Timestamptz(3)\` to:\n${offenders.join(
        "\n"
      )}`
    ).toEqual([]);
  });
});
