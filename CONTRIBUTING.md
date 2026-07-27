# Contributing

Thank you for your interest in contributing to the Monty STAC Extension. This
repository holds three related things — the [extension spec](README.md), the
[Monty model](docs/model/) and the [source analyses](docs/model/sources/) that
map real-world disaster data sources onto it — see the README's
[three pillars](README.md#the-three-pillars) section for how they fit
together.

All contributions are subject to our [Code of Conduct](CODE_OF_CONDUCT.md).
General contribution etiquette follows the
[STAC specification contributing guide](https://github.com/radiantearth/stac-spec/blob/master/CONTRIBUTING.md).

## Opening an issue or pull request

Issues use structured forms — pick **New source**, **Model / schema change**,
or **Bug report** when you
[open one](https://github.com/IFRCGo/monty-stac-extension/issues/new/choose).
Pull requests are pre-filled from
[`.github/PULL_REQUEST_TEMPLATE.md`](.github/PULL_REQUEST_TEMPLATE.md); fill in
the checklist that matches your change.

Every PR is reviewed by a maintainer before merge. There is no `CODEOWNERS`
file, so review is not auto-assigned — tag a member of the
[Montandon Core Team](https://github.com/orgs/IFRCGo/teams/montandon-core-team)
if a PR goes quiet.

## Ways to contribute

- **Add or update a source analysis** — follow the
  [Source Analysis Process](https://ifrcgo.org/monty-stac-extension/model/sources/#source-analysis-process)
  and register the source in
  [`docs/model/sources/sources.yml`](docs/model/sources/sources.yml), then run
  `python scripts/gen_sources_index.py` to regenerate the derived indexes
  (`docs/model/sources/README.md`, `examples/index.md`, `docs/sources.json`).
- **Change the model** — edit the relevant page under
  [`docs/model/`](docs/model/), most often
  [`taxonomy.md`](docs/model/taxonomy.md) for hazard/impact codes.
- **Change the schema** — [`json-schema/schema.json`](json-schema/schema.json)
  and the field descriptions in [`README.md`](README.md) must stay
  verbatim-identical, so a schema field change means editing both.

Markdown style nits across the repository are auto-fixable — run
`npx remark . -r .github/remark.yaml -o` for the root files linted by
`check-markdown`, or `npx remark docs -r .github/remark-docs.yaml -o` for
`docs/`.

## Cutting a release

> **Interim.** Adopting [`release-please`](https://github.com/googleapis/release-please)
> to automate the version bump is tracked in
> [#72](https://github.com/IFRCGo/monty-stac-extension/issues/72); until then,
> the bump is manual and is documented here so it isn't tribal knowledge.

The published schema is versioned per release at
`https://ifrcgo.org/monty-stac-extension/v<X.Y.Z>/schema.json`. Publishing a new
version has two halves: a **version bump** (a PR) and a **GitHub Release** (which
triggers the deploy).

Pick the version with [SemVer](https://semver.org/): a backward-compatible,
additive schema change (a new optional field, a new enum value) is a **minor**
bump; a breaking change (a required field, a removed/renamed field) is a
**major** bump.

### 1. Version bump (in a PR)

The version string lives in **four canonical files** — keep them identical:

1. [`package.json`](package.json) — the `version` field **and** the pinned
   schema URL in the `check-examples` / `format-examples` `schemaMap` args.
2. [`pyproject.toml`](pyproject.toml) — the `version` field.
3. [`json-schema/schema.json`](json-schema/schema.json) — the `$id` **and** the
   `const` schema URL that examples pin to.
4. [`README.md`](README.md) — the `Identifier:` URL.

The same pinned URL (`v<old>/schema.json`) is then propagated across every
example and source doc that references it. From a clean tree, bumping `1.3.0` to
`1.4.0` is:

```bash
git grep -l 'v1.3.0/schema.json' -- '*.json' '*.md' '*.toml' \
  | xargs sed -i'' -e 's#v1.3.0/schema.json#v1.4.0/schema.json#g'
# then bump the bare `version` in package.json and pyproject.toml by hand
npm test   # every example must still validate against the bumped URL
```

### 2. Changelog

In [`CHANGELOG.md`](CHANGELOG.md), rename the `[Unreleased]` section to
`[<X.Y.Z>] - <YYYY-MM-DD>`, add a fresh empty `[Unreleased]` section above it,
and add the version's link definition at the bottom.

### 3. Release

Once the bump PR is merged to `main`, create the GitHub Release (tag
`v<X.Y.Z>`). That publishes the JSON Schema:
[`publish.yaml`](.github/workflows/publish.yaml) copies `json-schema/` to the
`v<X.Y.Z>/` directory on the `gh-pages` branch, making
`https://ifrcgo.org/monty-stac-extension/v<X.Y.Z>/schema.json` resolve. Earlier
`v*.*.*/` directories are preserved, so historical items keep validating.

## Running tests locally

The same checks that run on PRs are part of the repository and can be run
locally to verify that changes are valid. You'll need `npm`, which is a
standard part of any [node.js installation](https://nodejs.org/en/download/).

Install dependencies once from the root of the repository:

```bash
npm install
```

Then, to lint the markdown and validate the examples against the JSON
schema:

```bash
npm test
```

If the tests reveal formatting problems with the examples, fix them with:

```bash
npm run format-examples
```

`docs/` is linted separately (`npm run check-docs`) under a relaxed profile
(`.github/remark-docs.yaml`) that keeps link validation and code-fence checks
but disables cosmetic rules that would otherwise fire across most of `docs/`.

## Building the documentation site locally

The published site at <https://ifrcgo.org/monty-stac-extension/> is built
from `docs/` with [MkDocs](https://www.mkdocs.org/) and the
[Material](https://squidfunk.github.io/mkdocs-material/) theme.

1. Create a Python virtual environment and install the doc dependencies:

   ```bash
   ./scripts/setup.sh
   ```

2. Serve it locally with live reload:

   ```bash
   source .venv/bin/activate
   mkdocs serve
   ```

   The site is then available at <http://127.0.0.1:8000/>.

CI builds it with `mkdocs build --strict`, which fails if a page under
`docs/` isn't reachable from the `nav` in `mkdocs.yml`, and
`python scripts/gen_sources_index.py --check`, which fails if the generated
source indexes have drifted from `sources.yml`.
