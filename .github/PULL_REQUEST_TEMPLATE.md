<!--
Thanks for contributing! Fill in the summary, then complete the checklist
sections that apply to your change. Delete the sections that don't.
See CONTRIBUTING.md for the contribution paths and the release procedure.
-->

## Summary

<!-- What does this change and why. Link the issue it closes, e.g. "Closes #123". -->

## Checklist

- [ ] `npm test` passes locally (markdown lint, example validation, link types, hazard codes).
- [ ] Markdown style nits auto-fixed (`npx remark . -r .github/remark.yaml -o` / `npx remark docs -r .github/remark-docs.yaml -o`).
- [ ] `CHANGELOG.md` updated under `[Unreleased]` (unless this is docs-only / trivial).

### Adding or updating a source

<!-- Delete this section if not applicable. -->

- [ ] Registered / updated in `docs/model/sources/sources.yml`.
- [ ] Source doc at `docs/model/sources/<ID>/README.md`, wired into `mkdocs.yml` nav.
- [ ] Example collections under `examples/<source>-<type>/` validate.
- [ ] `python scripts/gen_sources_index.py` re-run and the generated indexes committed (`--check` passes in CI).

### Changing the schema

<!-- Delete this section if not applicable. -->

- [ ] `json-schema/schema.json` and the matching field descriptions in `README.md` are verbatim-identical.
- [ ] SemVer impact noted (additive → minor, breaking → major); a version bump is a **separate** release PR — see CONTRIBUTING "Cutting a release".

### Changing the model or taxonomy

<!-- Delete this section if not applicable. -->

- [ ] Relevant page(s) under `docs/model/` updated; hazard/impact code changes reconcile with `docs/model/taxonomy.md`.
