#!/usr/bin/env python3
"""Builds the site into _site/ from Markdown pages in content/, data in data/*.yml and templates/.

    python3 src/build.py          # build
    python3 src/build.py --check  # build, then verify every internal link

Pages: content/<name>.md → /<name>/ (written as <name>/index.html). Each starts with a YAML front matter block:
    ---
    title: About                 (required; browser tab and <h1>)
    description: one sentence    (required; search engines)
    nav: /about/              (optional; top-menu item to highlight if not the page itself)
    subnav: toolkit              (optional; key of a sub-menu in data/nav.yml)
    layout: home                 (optional; "home" renders the home page from front matter)
    url: /toolkit/legal-landscape/   (optional; the page's address, default /<name>/)
    ---
Then ordinary Markdown. Lines that start with "::" insert a component rendered from data/:
    ::people LIST        cards for the people under LIST in data/people.yml (e.g. ::people leadership)
    ::partners           tiles for data/partners.yml
    ::products           cards for products with status available/next (data/products.yml)
    ::roadmap            table of all products
    ::news / ::events / ::publications   lists from data/news.yml
    ::citations          the citation blocks from data/citations.yml
    ::toc                "On this page" list of the ## headings
    ::cards              the Markdown list that follows becomes a row of cards (**Title** then text); '::cards wide' for fewer, wider cards
    ::timeline           the list that follows becomes a timeline (**date** then text)
    ::callout            the paragraph that follows becomes a highlighted box
    ::buttons            the list that follows becomes buttons ([label](href); first one filled)
"""
import os, re, sys, html, shutil, datetime
import yaml, markdown

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = lambda *a: os.path.join(ROOT, *a)
OUT = P('_site')
D = {n: yaml.safe_load(open(P('data', n + '.yml'))) for n in ('nav', 'news', 'products', 'people', 'partners', 'citations', 'site')}

def validate():
    """Fail early with a readable message when a data file is missing a required field."""
    req = {'news': ('kind', 'date', 'title', 'text'), 'products': ('id', 'status', 'status_label', 'title', 'roadmap')}
    for name, fields in req.items():
        for i, row in enumerate(D[name]):
            for f in fields:
                if f not in row: raise SystemExit(f'data/{name}.yml: entry {i + 1} ({row.get("title", "?")}) is missing "{f}"')
    for n in D['news']:
        if n['kind'] not in ('news', 'event', 'publication'): raise SystemExit(f'data/news.yml: "{n["title"]}" has unknown kind {n["kind"]}')
    for p in D['products']:
        if p['status'] not in ('available', 'next', 'planned'): raise SystemExit(f'data/products.yml: "{p["title"]}" has unknown status {p["status"]}')
    for key in D['nav']['menu'] + sum((v['items'] for v in D['nav']['submenus'].values()), []):
        if 'href' not in key or 'label' not in key: raise SystemExit(f'data/nav.yml: every item needs href and label: {key}')
validate()
D['site']['year'] = D['site'].get('copyright_year') or datetime.date.today().year

def site_vars(text):
    text = re.sub(r'\{\{site\.(\w+)\}\}', lambda m: E(str(D['site'].get(m.group(1), m.group(0)))), text)
    base = D['site'].get('base_url', '/').rstrip('/')
    if base:   # serving from a sub-path (e.g. https://user.github.io/repo/): prefix root-relative links
        text = re.sub(r'((?:href|src)=")/(?!/)', lambda m: m.group(1) + base + '/', text)
    return text
MD = lambda t: markdown.markdown(t, extensions=['tables', 'attr_list', 'md_in_html', 'sane_lists'])
E = html.escape

# ------------------------------------------------------------------ components
def people(key):
    rows = D['people'].get(key, [])
    return '<div class="people">' + ''.join(f'<div><b>{E(p["name"])}</b>{E(p["role"])}</div>' for p in rows) + '</div>'

def partners():
    return '<div class="partners">' + ''.join(f'<span>{E(x)}</span>' for x in D['partners']) + '</div>'

PILL = {'available': 'live', 'next': 'next', 'planned': 'plan'}
def products():
    out = []
    for p in D['products']:
        if p['status'] == 'planned': continue
        links = ''.join(f'<a{" class=\"btn accent\"" if l.get("primary") else ""} href="{l["href"]}">{E(l["label"])}</a>' for l in p.get('links', []))
        out.append(f'<div class="card" id="{p["id"]}"><span class="pill {PILL[p["status"]]}">{E(p["status_label"])}</span><h3>{E(p["title"])}</h3><p>{p.get("text","")}</p><div class="foot">{links}</div></div>')
    return '<div class="grid">' + ''.join(out) + '</div>'

def roadmap():
    rows = ''.join(f'<tr><td>{E(p["title"])}</td><td>{E(p["roadmap"]["what"])}</td><td>{E(p["roadmap"]["builds"])}</td><td><span class="pill {PILL[p["status"]]}">{p["status"]}</span></td></tr>' for p in D['products'])
    return f'<div class="tablewrap"><table><thead><tr><th>Product</th><th>What it is</th><th>Builds on</th><th>Status</th></tr></thead><tbody>{rows}</tbody></table></div>'

LABEL = {'event': 'Event', 'news': 'News', 'publication': 'Publication'}
def news(kinds, limit=None):
    items = sorted([n for n in D['news'] if n['kind'] in kinds], key=lambda n: str(n['date']), reverse=True)
    if limit: items = items[:limit]
    def card(n):
        t = f'<a href="{n["link"]}">{E(n["title"])}</a>' if n.get('link') else E(n['title'])
        return f'<div><span class="d">{LABEL[n["kind"]]} · {E(str(n["date"]))}</span><b>{t}</b>{n.get("text","")}</div>'
    return '<div class="newslist">' + ''.join(card(n) for n in items) + '</div>'

def citations():
    return ''.join(f'<div class="cite">{c}</div>' for c in D['citations'])

def toc(md_text):
    items = re.findall(r'^## (.+?)\s*(?:\{#([\w-]+)\})?\s*$', md_text, re.M)
    lis = ''.join(f'<li><a href="#{i or slug(t)}">{E(t)}</a></li>' for t, i in items)
    return f'<div class="toc"><b>On this page</b><ol>{lis}</ol></div>'

def slug(t): return re.sub(r'[^a-z0-9]+', '-', t.lower()).strip('-')

def list_items(block):
    """Markdown list block → list of item texts (bullets or numbers)."""
    return [re.sub(r'^\s*(?:[-*]|\d+\.)\s+', '', l) for l in block.strip().splitlines() if re.match(r'^\s*(?:[-*]|\d+\.)\s+', l)]

def inline(t): return MD(t)[3:-4] if MD(t).startswith('<p>') else MD(t)   # strip the outer <p>

def cards(block, arg=None):
    out = []
    for it in list_items(block):
        idm = re.search(r'\{#([\w-]+)\}', it); it = re.sub(r'\s*\{#[\w-]+\}', '', it)
        m = re.match(r'\*\*(.+?)\*\*\s*[—–:-]?\s*(.*)', it, re.S)
        title, text = (m.group(1), m.group(2)) if m else ('', it)
        out.append(f'<div{" id=\"" + idm.group(1) + "\"" if idm else ""}><h3>{E(title)}</h3><p>{inline(text)}</p></div>')
    minw = {'wide': '300px', 'narrow': '200px'}.get(arg, '200px' if len(out) >= 5 else '260px')
    style = f' style="grid-template-columns:repeat(auto-fit,minmax({minw},1fr))"'
    return f'<div class="how"{style}>' + ''.join(out) + '</div>'

def timeline(block):
    out = []
    for it in list_items(block):
        m = re.match(r'\*\*(.+?)\*\*\s*[—–:-]?\s*(.*)', it, re.S)
        out.append(f'<li><span class="d">{E(m.group(1))}</span><span>{inline(m.group(2))}</span></li>' if m else f'<li><span class="d"></span><span>{inline(it)}</span></li>')
    return '<ul class="timeline">' + ''.join(out) + '</ul>'

def buttons(block):
    out = []
    for k, it in enumerate(list_items(block)):
        m = re.match(r'\[(.+?)\]\((.+?)\)', it)
        if m: out.append(f'<a class="btn {"accent" if k == 0 else "ghost2"}" href="{m.group(2)}">{E(m.group(1))}</a>')
    return '<p class="cta">' + ' '.join(out) + '</p>'

def callout(block): return f'<div class="callout">{MD(block)}</div>'

# ------------------------------------------------------------------ page assembly
def render_body(md_text):
    """Replace ::directives with HTML, convert the rest with Markdown."""
    parts, pos = [], 0
    for m in re.finditer(r'^::(\w+)(?:[ \t]+(\S+))?[ \t]*\n', md_text, re.M):
        parts.append(md_text[pos:m.start()])
        name, arg = m.group(1), m.group(2)
        rest = md_text[m.end():]
        consume = 0
        if name in ('cards', 'timeline', 'buttons', 'callout'):
            blk = re.match(r'(.*?)(?:\n\s*\n|\Z)', rest, re.S); consume = blk.end(); block = blk.group(1)
            out = cards(block, arg) if name == 'cards' else {'timeline': timeline, 'buttons': buttons, 'callout': callout}[name](block)
        elif name == 'people': out = people(arg)
        elif name == 'partners': out = partners()
        elif name == 'products': out = products()
        elif name == 'roadmap': out = roadmap()
        elif name == 'news': out = news(('news',))
        elif name == 'events': out = news(('event',))
        elif name == 'publications': out = news(('publication',))
        elif name == 'latest': out = news(('news', 'event', 'publication'), limit=int(arg or 3))
        elif name == 'citations': out = citations()
        elif name == 'toc': out = toc(md_text)
        else: raise SystemExit(f'unknown directive ::{name}')
        parts.append('\n\n' + out + '\n\n'); pos = m.end() + consume
    parts.append(md_text[pos:])
    return MD(''.join(parts))

def front_matter(text):
    m = re.match(r'---\s*\n(.*?)\n---\s*\n', text, re.S)
    if not m: raise SystemExit('missing front matter')
    return yaml.safe_load(m.group(1)) or {}, text[m.end():]

def menu(active):
    return ''.join(f'<a href="{i["href"]}"{" class=\"active\"" if i["href"] == active else ""}>{E(i["label"])}</a>' for i in D['nav']['menu'])

def submenu(key, page):
    if not key: return ''
    sm = D['nav']['submenus'][key]
    items = ''.join(f'<a href="{i["href"]}"{" class=\"active\"" if i["href"] == page else ""}>{E(i["label"])}</a>' for i in sm['items'])
    return f'<div class="subnav"><div class="wrap"><span>{E(sm["label"])}</span>{items}</div></div>'

def home(meta):
    """The home page is rendered from its front matter (see content/index.md)."""
    h = meta['hero']
    btns = ''.join(f'<a class="btn{"" if k == 0 else " ghost"}" href="{b["href"]}">{E(b["label"])}</a>' for k, b in enumerate(h['buttons']))
    hero_svg = open(P('templates', 'hero-map.svg')).read()
    hero = f'<section class="hero big"><div class="wrap"><p class="tag">{E(h["tagline"])}</p><h1>{h["headline"]}</h1><p>{E(h["lead"])}</p><div class="cta">{btns}</div></div>{hero_svg}</section>'
    why = '<div class="why">' + ''.join(f'<div><b>{E(w["claim"])}</b><span>{E(w["consequence"])}</span></div>' for w in meta['why']) + '</div>'
    build = '<div class="how" style="grid-template-columns:repeat(auto-fit,minmax(280px,1fr))">' + ''.join(f'<div><span class="n">{E(c["kind"])}</span><h3>{E(c["title"])}</h3><p>{E(c["text"])}</p></div>' for c in meta['build']) + '</div>'
    regions = '<div class="regions">' + ''.join(f'<span>{E(r)}</span>' for r in meta['regions']) + '</div>'
    band = meta['band']
    bbtn = ''.join(f'<a class="btn{"" if k == 0 else " ghost"}" href="{b["href"]}">{E(b["label"])}</a>' for k, b in enumerate(band['buttons']))
    imp = ''
    if meta.get('impact'):
        imp = '<div class="impact">' + ''.join(f'<div><b>{E(str(x["value"]))}</b><span>{E(x["label"])}</span></div>' for x in meta['impact']['items']) + '</div>'
        imp = f'<h2>{E(meta["impact"]["title"])}</h2>{imp}' + (f'<p class="note">{E(meta["impact"]["note"])}</p>' if meta['impact'].get('note') else '')
    body = f'''{why}
<h2>{E(meta["vision_title"])}</h2><p class="big">{E(meta["vision"])}</p>
<h2>{E(meta["build_title"])}</h2>{build}
<p>{''.join(f'<a class="btn {"accent" if k == 0 else "ghost2"}" href="{x["href"]}">{E(x["label"])}</a> ' for k, x in enumerate(meta.get('build_buttons', [])))}</p>
<h2>{E(meta["global_title"])}</h2>{regions}<p>{E(meta["global_text"])}</p>{partners()}
<p><a class="btn accent" href="{meta.get('global_link', {}).get('href', '/about/#people')}">{E(meta.get('global_link', {}).get('label', 'Meet the people'))}</a></p>
{imp}
<div class="band"><h2>{E(band["title"])}</h2><p>{E(band["text"])}</p><div class="cta">{bbtn}</div></div>
<h2>News and events</h2>{news(("news","event","publication"), 3)}'''
    return hero + '\n<main class="wrap">\n' + body + '\n</main>'

def build():
    if os.path.exists(OUT): shutil.rmtree(OUT)
    os.makedirs(OUT)
    for d in ('assets', 'toolkit'):
        shutil.copytree(P(d), os.path.join(OUT, d))
    for f in ('CNAME', '.nojekyll'):
        if os.path.exists(P(f)): shutil.copy(P(f), OUT)
    tpl = open(P('templates', 'base.html')).read()
    footer_nav = ' · '.join(f'<a href="{i["href"]}">{E(i["label"])}</a>' for i in D['nav']['menu'])
    pages = [f for f in os.listdir(P('content')) if f.endswith(('.md', '.html'))]; built = []   # content/_drafts/ is not built
    for fn in sorted(pages):
        text = open(P('content', fn)).read()
        meta, body = front_matter(text)
        stem = os.path.splitext(fn)[0]
        url = meta.get('url') or ('/' if stem == 'index' else f'/{stem}/')      # clean URL: /about/, /toolkit/legal-landscape/
        out_name = url
        if meta.get('layout') == 'home':
            content = home(meta)
        elif fn.endswith('.html'):          # generated page: already HTML
            content = body
        else:
            h1 = f'<h1 style="font-size:2rem;font-weight:600;margin:1.2rem 0 .4rem">{E(meta["title"])}</h1>\n'
            content = '<main class="wrap">\n' + h1 + render_body(body) + '\n</main>'
        top = meta.get('nav') or (D['nav']['submenus'][meta['subnav']]['parent'] if meta.get('subnav') else out_name)
        page = (tpl.replace('{{title}}', E(meta['title'])).replace('{{description}}', E(meta['description']))
                   .replace('{{nav}}', menu(top)).replace('{{footer_nav}}', footer_nav)
                   .replace('{{subnav}}', submenu(meta.get('subnav'), out_name)).replace('{{content}}', content))
        out_path = os.path.join(OUT, url.strip('/'), 'index.html')
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        open(out_path, 'w').write(site_vars(page)); built.append(url)
        print('built', url)
    # 404 page and sitemap
    nf = tpl.replace('{{title}}', 'Page not found').replace('{{description}}', 'Page not found').replace('{{nav}}', menu('')).replace('{{footer_nav}}', footer_nav).replace('{{subnav}}', '').replace('{{content}}', '<main class="wrap"><h1 style="font-size:2rem;font-weight:600;margin:1.2rem 0 .4rem">Page not found</h1><p class="lead">The page may have moved. Try the menu above, or start from the <a href="/">home page</a>.</p></main>')
    open(os.path.join(OUT, '404.html'), 'w').write(site_vars(nf))
    base = 'https://' + D['site']['domain'] + '/'
    urls = sorted({base.rstrip('/') + u for u in built} | {base + 'toolkit/'})
    open(os.path.join(OUT, 'sitemap.xml'), 'w').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + ''.join(f'<url><loc>{u}</loc></url>' for u in urls) + '</urlset>\n')
    open(os.path.join(OUT, 'robots.txt'), 'w').write(f'User-agent: *\nAllow: /\nSitemap: {base}sitemap.xml\n')

def check():
    bad = 0
    for dirpath, _, files in os.walk(OUT):
        for fn in files:
            if not fn.endswith('.html'): continue
            page = os.path.join(dirpath, fn)
            for href in re.findall(r'(?:href|src)="([^"#]+)', open(page).read()):
                if href.startswith(('http', 'mailto', 'data:')): continue
                target = os.path.join(OUT, href.lstrip('/')) if href.startswith('/') else os.path.join(dirpath, href)
                if not (os.path.exists(target) or os.path.exists(os.path.join(target, 'index.html'))):
                    print(f'BROKEN in {os.path.relpath(page, OUT)}: {href}'); bad += 1
    print('links ok' if not bad else f'{bad} broken links'); sys.exit(1 if bad else 0)

if __name__ == '__main__':
    build()
    if '--check' in sys.argv: check()
