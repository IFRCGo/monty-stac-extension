#!/usr/bin/env node
// Asserts that `related` / `derived_from` links whose target is a STAC Item
// use `application/geo+json` rather than `application/json`.
// The STAC JSON Schema does not constrain link `type`, so stac-node-validator
// won't catch this class of error — see
// https://github.com/IFRCGo/monty-stac-extension/issues/55.

import { readFileSync, readdirSync, statSync } from "node:fs";
import { join, dirname, resolve } from "node:path";

const EXAMPLES_DIR = resolve(import.meta.dirname, "..", "examples");
const ITEM_TARGETING_RELS = new Set(["related", "derived_from"]);

function walk(dir) {
  const files = [];
  for (const entry of readdirSync(dir)) {
    const full = join(dir, entry);
    if (statSync(full).isDirectory()) {
      files.push(...walk(full));
    } else if (entry.endsWith(".json")) {
      files.push(full);
    }
  }
  return files;
}

function loadJson(path) {
  try {
    return JSON.parse(readFileSync(path, "utf8"));
  } catch {
    return null;
  }
}

const files = walk(EXAMPLES_DIR);
const cache = new Map();
function load(path) {
  if (!cache.has(path)) cache.set(path, loadJson(path));
  return cache.get(path);
}

const errors = [];

for (const file of files) {
  const data = load(file);
  if (!data || data.type !== "Feature") continue;

  for (const link of data.links ?? []) {
    if (!ITEM_TARGETING_RELS.has(link.rel)) continue;
    if (!link.href || /^https?:\/\//.test(link.href)) continue;
    if (link.type !== "application/json") continue;

    const targetPath = resolve(dirname(file), link.href);
    const target = load(targetPath);
    if (target?.type === "Feature") {
      errors.push(
        `${file}: rel="${link.rel}" href="${link.href}" has type "application/json" but targets a STAC Item — should be "application/geo+json"`,
      );
    }
  }
}

if (errors.length > 0) {
  console.error(`Found ${errors.length} link(s) with incorrect media type:\n`);
  for (const e of errors) console.error(`  ${e}`);
  process.exit(1);
} else {
  console.log("All item-targeting related/derived_from links use application/geo+json.");
}
