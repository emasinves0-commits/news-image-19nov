// Copies the poster (entry.png, drawn by draw.py) into the output directory.
import { copyFileSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const src = join(dirname(fileURLToPath(import.meta.url)), "entry.png");
const outDir = process.env.MAKEFUN_OUTPUT_DIR || "/output";
const dest = join(outDir, "entry.png");

try {
  mkdirSync(outDir, { recursive: true });
  copyFileSync(src, dest);
} catch (err) {
  console.error(`error: could not copy ${src} to ${dest}: ${(err as Error).message}`);
  process.exit(1);
}
console.log(`wrote ${dest}`);
