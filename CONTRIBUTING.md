# Contributing

Thank you for helping keep these resources accurate and useful. The site is built from Markdown and YAML files; **MAINTAINING.md** explains which file holds what and how pages are written.

## Ways to contribute

- **Report an error in legal content** (a tool step, a worked example, the compatibility matrix, a date). Open an issue with the *Legal content correction* template, citing the instrument.
- **Propose a worked example** from a real collaboration (anonymised as needed): the *Worked example* template.
- **Report a pilot** of the toolkit: what worked, what did not, where the questions were unclear.
- **Fix text, links or layout**: open a pull request directly.

## How changes are reviewed

- Text, design and site changes: one maintainer approves.
- **Legal content** (`data/tools.yml`, `data/examples.yml`, `data/tiers.yml`, `src/landscape/matrix.json`, country-specific statements anywhere): a regional co-author for the jurisdictions concerned approves before merge. `CODEOWNERS` requests that review automatically.
- Every pull request is built by the Action; a build or link-check failure must be fixed before merge.

## Conventions

- Dates of legal content are stated, not implied: when you change a legal statement, update the date it reflects (see MAINTAINING.md, section 9).
- Mark anything not yet confirmed by a regional co-author with `[verify]`.
- Keep the menu at four items; new pages are linked from About, Products or Get involved.
- Content is CC BY 4.0 and code is MIT; by contributing you agree your contribution is released under the same terms.
