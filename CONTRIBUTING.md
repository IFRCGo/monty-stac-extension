# Contributing

Thank you for your interest in contributing to the Monty STAC Extension. This
repository holds three related things — the [extension spec](README.md), the
[Monty model](docs/model/) and the [source analyses](docs/model/sources/) that
map real-world disaster data sources onto it — see the README's
[three pillars](README.md#the-three-pillars) section for how they fit
together.

All contributions are subject to the
[STAC Specification Code of Conduct](https://github.com/radiantearth/stac-spec/blob/master/CODE_OF_CONDUCT.md).
General contribution etiquette follows the
[STAC specification contributing guide](https://github.com/radiantearth/stac-spec/blob/master/CONTRIBUTING.md).

> A dedicated `CODE_OF_CONDUCT.md`, issue/PR templates and a documented
> release procedure are tracked in
> [#68](https://github.com/IFRCGo/monty-stac-extension/issues/68); this file
> will grow to cover them.

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
