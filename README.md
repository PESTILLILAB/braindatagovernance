# Global Brain Governance — braindatagovernance.org

Open instruments for sharing brain data across borders responsibly. Maintained by the Pestilli Laboratory, The University of Texas at Austin, with the BRIDGE community. Funded by Wellcome.

The site is written in Markdown and YAML and built into static HTML by a short Python script; GitHub Actions builds and deploys it on every push to `main`.

```
content/*.md        the pages (Markdown with a small front matter)  ← edit these
content/_drafts/    pages written but not yet published (not built)
data/*.yml          news, products, people, partners, citations, menu, site settings,
                    and the Toolkit's content (examples, tools, tiers)  ← and these
templates/          header/footer skeleton and the hero map
assets/             stylesheet, favicon and the logo files (assets/logo/)
toolkit/            the Toolkit explorer and its PDFs (generated from src/explorer/)
build.sh            builds everything (see src/README.md for the individual generators)
src/                the generators: pages, Legal landscape, Toolkit explorer, PDFs
.github/workflows/  build and deploy
```

Local preview: `pip install markdown pyyaml && ./build.sh && python3 -m http.server 8000 -d _site`, then open http://localhost:8000/.

Published pages: `/` (home), `/about/`, `/media/`, `/toolkit/`, `/toolkit/legal-landscape/`. Pages in `content/_drafts/` (why, products, get-involved, support, summit) are written but not built; move one into `content/` to publish it.

## Putting it online

1. Create a public repository under github.com/pestillilab (for example `braindatagovernance`), push this folder to its `main` branch.
2. Repository **Settings → Pages → Source: GitHub Actions**. The workflow in `.github/workflows/build.yml` then builds and deploys on every push to `main` (about a minute; progress under the Actions tab).
3. Same screen, **Custom domain**: `braindatagovernance.org` (matches the `CNAME` file). At the DNS provider add A records for the apex to 185.199.108.153, 185.199.109.153, 185.199.110.153 and 185.199.111.153, and a CNAME for `www` to `pestillilab.github.io`. When DNS has propagated, tick **Enforce HTTPS**.
4. Until the domain is live the site is at `pestillilab.github.io/<repo-name>/`; for that address set `base_url: /<repo-name>/` in `data/site.yml`, and set it back to `/` for the domain.

After that, publishing is editing a file in `content/` or `data/` and pushing (or saving in the GitHub web editor); the site rebuilds itself.

See **MAINTAINING.md** for how to add news, products, people, pages, menu items and worked examples; **CONTRIBUTING.md** for how changes are reviewed; **CHANGELOG.md** for what changed when.
