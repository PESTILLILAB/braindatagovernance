# Maintaining braindatagovernance.org

Everything you will normally change is a Markdown file in `content/` or a YAML file in `data/`.
Edit on GitHub (open the file, pencil icon, edit, "Commit changes"); a GitHub Action rebuilds and
publishes the site within a couple of minutes. If a change breaks something (a missing colon in
YAML, a link to a page that does not exist) the Action fails and the old site stays up; the
Actions tab shows the error and its line.

## Addresses

Every page has a clean address: `braindatagovernance.org/about/`, `/why/`, `/products/`,
`/get-involved/`, `/toolkit/` (the Toolkit explorer), `/toolkit/legal-landscape/`. A page
`content/<name>.md` is published at `/<name>/`; set `url: /some/path/` in its front matter to
choose a different address. Each product gets its own folder at the root and therefore its own
address: `/toolkit/` now, `/ezgov/` when it ships. Links inside the site are written with a
leading slash (`[About](/about/)`, `href: /products/#ezgov`) so they work from any page.

| Change | File |
|---|---|
| News, event, publication | `data/news.yml` |
| Add, release or retire a product; roadmap | `data/products.yml` |
| People | `data/people.yml` |
| Partner institutions | `data/partners.yml` |
| How to cite | `data/citations.yml` |
| Menu and sub-menus | `data/nav.yml` |
| Home page text, numbers | `content/index.md` (its front matter; see section 4) |
| Support the work page | `content/support.md` |
| Text of any other page | `content/<page>.md` |
| A new page | new `content/<name>.md` |
| Header, footer | `templates/base.html` |
| Colours, fonts | `assets/site.css` |
| Worked examples | `data/examples.yml` |
| Tool steps (the four tools) | `data/tools.yml` |
| Tier framework | `data/tiers.yml` |
| Site-wide settings: contact, GitHub, version, legal-content date | `data/site.yml` |
| Compatibility matrix | `src/landscape/matrix.json` (then the Action regenerates) |

## 0. Published and unpublished pages

Only pages directly in `content/` are built. `content/_drafts/` holds pages written but not yet
published (Why it matters, Products, Get involved, Support the work, the summit page); to publish
one, move it up into `content/`, add it to `data/nav.yml` if it belongs in the menu, and check its
links. The site currently publishes the home page, About, the Toolkit and the Legal landscape.

## 1. News, events, publications — `data/news.yml`

An event or news item that deserves a page of its own gets one in `content/` and a `link` in
its news entry. `content/summit-2026.md` is the model: it is published at
`braindatagovernance.org/summit-2026/`, and the entry in `data/news.yml` points to it with
`link: /summit-2026/`. Name such pages `<event>-<year>` (`marrakesh-2025`, `summit-2027`).

Add a block anywhere (they are sorted by date, newest first):

```yaml
- kind: news            # news | event | publication
  date: "2027-03"       # "2027-03", "2027-03-15" or "2027"
  title: ezGov public beta
  text: ezGov is open for testing with real collaborations. Feedback through GitHub issues.
  link: /products/#ezgov        # optional
```

The three newest items appear on the home page; events are listed under *Events* on Get
involved, news and publications under *News and publications*.

## 2. Products — `data/products.yml`

Products are listed in display order. A planned product needs only:

```yaml
- id: handbook
  status: planned             # available | next | planned
  status_label: Planned
  title: Legal landscape handbook
  roadmap: {what: Country profiles for the sampled jurisdictions, builds: Supplementary Data 1–3}
```

To release it, change `status` to `next` (a card appears) or `available`, set `status_label`
to the version and date, and add `text` and `links`:

```yaml
  text: Country profiles across the six governance layers, with the coded instruments and dates.
  links:
    - {label: Open the handbook, href: /handbook/, primary: true}
    - {label: PDF, href: /handbook/handbook.pdf}
```

The product's own files go in a folder of their own at the repository root, next to
`toolkit/`; add that folder name to the `for d in ('assets', 'toolkit')` line in `src/build.py`
so it is copied into the site. Add a news entry. Only products belong here: the MDTAA and the
legal landscape are parts of the Toolkit.

## 3. People and partners — `data/people.yml`, `data/partners.yml`

People are in named groups; a page shows a group with a line `::people team`. Add a
person as `- {name: …, role: …}` under the group, or add a new group and a new `::people`
line on the page. Partners are a plain list, shown wherever a page says `::partners`.

## 4. Text on a page — `content/<page>.md`

Pages are Markdown: `## Heading`, paragraphs, `**bold**`, `*italic*`, `[link](page.html)`,
lists. Each file starts with a front matter block:

```yaml
---
title: About                       # required: browser tab and page heading
description: One sentence.         # required: for search engines
nav: /about/                       # optional: top-menu item to highlight (if not the page itself)
url: /some/path/                   # optional: the page's address (default /<name>/)
subnav: products                   # optional: sub-menu bar to show (a key in data/nav.yml)
---
```

Give a heading a stable id with `## History {#history}` so links like `/about/#history`
keep working. A paragraph followed by `{: .lead}` is shown as the larger intro text.

Lines starting with `::` insert a component rendered from the data files:

| Line | Shows |
|---|---|
| `::toc` | "On this page" list of the `##` headings |
| `::people team` | the people in that group |
| `::partners` | the partner tiles |
| `::products` | product cards (available and in development) |
| `::roadmap` | the roadmap table |
| `::news`, `::events`, `::publications` | the lists from `data/news.yml` |
| `::citations` | the citation blocks |
| `::cards` + a list | the list that follows becomes a row of cards; each item is `**Title** — text`, optionally with `{#id}`. `::cards wide` makes fewer, wider cards |
| `::timeline` + a list | the list becomes a timeline; each item is `**2024** — text` |
| `::callout` + a paragraph | a highlighted box |
| `::buttons` + a list of links | buttons; the first is filled, the others outlined |

The home page (`content/index.md`) has no body: everything is in its front matter. The `hero`
is required; every other block is optional and appears only if its key is present: `why` (three
claim/consequence statements), `vision` (one sentence, with `vision_title`), `build` (cards,
with `build_title` and `build_buttons`), `regions` (with `global_title`, `global_text` and the
partner tiles), `impact` (numbers, with `title` and `note`), `band` (the call to action) and
`news: 3` (latest items). A block has a heading only if it carries a title, so the page can be
as sparse or as full as you like; the current page is deliberately lean: hero, three cards,
three numbers, one band.

## 5. A new page — worked example: "Partner organisations"

1. Create `content/partners.md`:

   ```markdown
   ---
   title: Partner organisations
   description: The institutions and initiatives that build Global Brain Governance with us.
   nav: /about/
   ---

   One sentence on what this page is.
   {: .lead}

   ## Institutions

   ::partners

   ## Initiatives

   Text about the initiatives, with [links](https://bridge.incf.org/).
   ```

2. Link to it: either from another page (`[Partner organisations](/partners/)`); it is published at `/partners/`, or in the
   menu, `data/nav.yml`:

   ```yaml
   menu:
     - {href: /about/, label: About}
     - {href: /partners/, label: Partners}      # new
     ...
   ```

   The menu is deliberately four items; a fifth fits, a sixth wraps on small screens. For a
   sub-menu instead, add to `submenus:`

   ```yaml
     about:
       label: About
       parent: /about/
       items:
         - {href: /about/, label: Overview}
         - {href: /partners/, label: Partner organisations}
   ```

   and write `subnav: about` in the front matter of every page that should show that bar.

3. Commit. The Action builds, checks every internal link, and publishes.

## 6. The Toolkit explorer and the Legal landscape (generated)

The Toolkit explorer (`toolkit/index.html`) is generated from three data files:

- `data/examples.yml` — the worked examples. To add one, copy an existing block, give it a new
  `id` (`s17`), and fill in the story (`setting`), the parties, the data, the answers at each
  step of each tool, the determination (`verdict_new`; begin with "Do not" for a negative
  outcome), the legal points and the questions for counsel. Put it where it should appear in the
  4×4 grid.
- `data/tools.yml` — the four tools, step by step (T6 = Tool 1 … T9 = Tool 4), copied from
  Supplementary Tables 6–9 of the study. Each row is step, question, answer, tier, required action
  (Tool 4: step, question, if yes, if no). Rows of one step repeat the step label and question so
  that every row stands alone; a single-cell row is a note shown as a band. The step labels are
  also used by the worked examples and by the workflow diagram, so a renumbering in the study means
  updating `data/examples.yml` and `src/explorer/iwf.py` as well.
- `data/tiers.yml` — the tier framework.

The Legal landscape (`content/findings.html`) is generated from `src/landscape/matrix.json`
and `geo.json`. The Action regenerates both pages on every push; never edit the generated
files. The explorer's workflow diagram (nodes and edges) is code in `src/explorer/iwf.py`.
The PDFs in `toolkit/pdf/` need a browser and are made locally:

```sh
npm i playwright && npx playwright install chromium   # once
./build.sh pdf
```

Commit the updated files in `toolkit/pdf/`. The intermediate HTML goes to `_build/`, which git
ignores.

## 7. Local preview

```sh
pip install markdown pyyaml
./build.sh                               # builds _site/ and checks links
python3 -m http.server 8000 -d _site     # then open http://localhost:8000/
```

The site uses root-relative links (`/about/`), so preview it through the small web server
above rather than by double-clicking a file.

## 7b. Serving from a sub-path

If the site is served at `https://<user>.github.io/<repo>/` rather than at the domain root, set
`base_url: /<repo>/` in `data/site.yml`; the build prefixes every internal link. Set it back to
`/` once the domain is attached.

## 8. Publishing

Settings → Pages → Source: **GitHub Actions**. `CNAME` holds the domain; DNS for
`braindatagovernance.org` points at GitHub Pages (`A` records to GitHub's Pages addresses or a
`CNAME` to `pestillilab.github.io`). Protect `main`; legal content changes go through a pull
request reviewed by a regional co-author.

## 9. When legal content changes

Update `toolkit_version`, `toolkit_date` and `legal_content_date` in `data/site.yml`: they feed
the explorer header and its Sources tab, the Legal landscape page and the products page. Update
the `status_label` of the product in `data/products.yml`, regenerate the PDFs, add a line to
`CHANGELOG.md` and a news entry.

## 10. Review and roles

`CONTRIBUTING.md` states the rules for outside contributors. `.github/CODEOWNERS` makes GitHub
request a review from the legal reviewers team whenever `data/tools.yml`, `data/examples.yml`,
`data/tiers.yml` or the matrix change, and from the site maintainers for everything else:
create those two teams in the GitHub organisation (or replace the placeholders with user names)
and protect `main` so that an approved review is required. Issue templates guide reporters of
legal corrections, worked examples and pilot reports.

## 11. Logo and media

The logo is a compass rose. Files are in `assets/logo/` (mark, mark on dark, mono, lockups, as SVG
and PNG); `assets/favicon.svg` is the mark with a heavier ring. The header uses the mark inline in
`templates/base.html`; the Toolkit's top bar uses it in `src/explorer/gen.py`. The public Media
page (`content/media.md`) lists the files, the colours and the usage terms.
