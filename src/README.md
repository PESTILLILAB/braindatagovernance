# src/ — the generators

Nothing in here holds content. Content is in `content/` (pages) and `data/` (lists and the Toolkit's
examples, tools and tiers). These scripts turn it into HTML.

| File | What it does | Reads | Writes |
|---|---|---|---|
| `build.py` | Assembles every page: Markdown + front matter → HTML in the site template; `::directives` render the data files; checks links | `content/`, `data/`, `templates/` | `_site/` |
| `landscape/findings.py` | Generates the Legal landscape page (matrix, network, maps) | `landscape/matrix.json`, `landscape/geo.json`, `data/site.yml` | `content/findings.html` |
| `landscape/mkgeo.py` | One-off: projects world geometry into `geo.json`. Needs the `world-atlas` npm package (`countries-50m.json`) as its argument | world-atlas | `landscape/geo.json` |
| `explorer/gen.py` | Generates the Toolkit explorer page | `data/examples.yml`, `data/tools.yml`, `data/tiers.yml`, `data/site.yml`, `explorer/iwf.py` | `toolkit/index.html` |
| `explorer/tiers.py` | Renders the tier framework (used by `gen.py` and `make_pdfs.py`) | `data/tiers.yml` | — |
| `explorer/iwf.py` | The interactive workflow diagram: its nodes, edges, panel texts, CSS and JS | — | — |
| `explorer/make_pdfs.py` | Lays out each tool and the tier figure as print HTML | `data/tools.yml`, `data/tiers.yml` | `_build/pdf/*.html` |
| `explorer/topdf.js`, `explorer/tierfig.js` | Print that HTML to PDF/PNG with a headless browser (Playwright) | `_build/pdf/` | `toolkit/pdf/` |

`../build.sh` runs them in the right order; `../build.sh pdf` also regenerates the PDFs.
The GitHub Action runs everything except the PDFs, which are committed in `toolkit/pdf/`.

The explorer keeps its own stylesheet inside `gen.py` rather than using `assets/site.css`, because it
is a self-contained application page with its own tabs and components. Colours are the same
variables; change both places if you re-theme.
