# Risk model options — slide deck

Slidev deck that summarises [docs/model/risk-model-options.md](../../docs/model/risk-model-options.md)
for the core-partner review ([discussion #110](https://github.com/IFRCGo/monty-stac-extension/discussions/110)).
The theme is a copy of the Development Seed slidev template.

## Run

Run all commands in this folder (`slides/2026-10-risk-model-options/`), not in `slides/`.

```sh
cd slides/2026-10-risk-model-options
pnpm install --frozen-lockfile
pnpm dev      # http://localhost:3030
pnpm build    # static site in dist/
pnpm export   # PDF (needs playwright-chromium)
```

## Note

The root `npm test` runs `stac-node-validator .` on the whole repository. It also reads the JSON files in
this folder's `node_modules/`, and reports them as invalid. Remove `node_modules/` before you run the root
tests. CI is not affected, because `node_modules/` is not committed.
