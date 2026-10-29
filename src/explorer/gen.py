import os; HERE = os.path.dirname(os.path.abspath(__file__))
import json, html, re, yaml
import iwf
DATA = os.path.join(HERE, '..', '..', 'data')
Y = lambda n: yaml.safe_load(open(os.path.join(DATA, n + '.yml')))
SITE = Y('site')
SCENARIOS = Y('examples')
for _s in SCENARIOS:                       # steps as (step, answer, note) tuples, as the renderer expects
    for _t in _s['tools']: _t['steps'] = [(x['step'], x['answer'], x['note']) for x in _t['steps']]
from tiers import tiers_html, TIER_CSS

T = Y('tools')

E = lambda s: html.escape(str(s), quote=True)

# ---------- toolkit tables -> accordion html
def tool_html(key, title, cols):
    rows = T[key]; hdr = rows[0]; body = rows[1:]
    out = [f'<h3>{E(title)}</h3>']
    # group by step
    groups = []; cur = None
    for r in body:
        changed = r[-1] == '__CHANGED__'; cells = r[:-1] if changed else r[:]
        while len(cells) < len(hdr): cells.append('')
        single = sum(1 for c in cells if c) == 1 and cells[0]
        step = cells[0]
        if single:
            groups.append({'kind':'note','text':cells[0],'changed':changed}); cur=None; continue
        if step and (cur is None or cur['step'] != step or cur.get('q') != cells[1] and cells[1]):
            cur = {'kind':'step','step':step,'q':cells[1],'rows':[],'changed':False}; groups.append(cur)
        if cur is None:
            cur = {'kind':'step','step':step or '?','q':cells[1],'rows':[],'changed':False}; groups.append(cur)
        if not cur.get('q') and cells[1]: cur['q'] = cells[1]
        cur['rows'].append((cells, changed)); cur['changed'] = cur['changed'] or changed
    for g in groups:
        if g['kind']=='note':
            out.append(f'<div class="note">{E(g["text"])}</div>'); continue
        cls = 'step'
        q = g['q'] or (g['rows'][0][0][1] if g['rows'] else '')
        out.append(f'<details class="{cls}"><summary><span class="stepno">{E(g["step"])}</span><span class="stepq">{E(q)}</span></summary>')
        out.append('<table><thead><tr>' + ''.join(f'<th>{E(h)}</th>' for h in hdr[2:]) + '</tr></thead><tbody>')
        for cells, changed in g['rows']:
            out.append(f'<tr>' + ''.join(f'<td>{E(c)}</td>' for c in cells[2:]) + '</tr>')
        out.append('</tbody></table></details>')
    return '\n'.join(out)

tools = [
 ('T6','Tool 1 — Neurodata Governance Decision Tool','Assigns a provisional functional-exposure tier (5, 4, 3, 2, 1) to the particular object or artefact and identifies the baseline safeguards. It opens with an applicability checkpoint on statutory access regimes and impact assessments. The highest applicable tier governs; an Unknown answer takes the more protective tier; a tier is confirmed only when all applicable steps and required reviews are complete.'),
 ('T7','Tool 2 — Neurodata Transfer and Access Decision Tool, Neuro-TADT','Asks whether the proposed pathway can carry the tier’s safeguards. Step 3 splits the tool into a controlled-access pathway (Steps 4A–12A) and a public-release pathway (Steps 4B–12B); both share the jurisdiction, lawful-basis and statutory-authorisation checks (Steps 6, 7 and 7A) and the implementation check (Step 13). Four outcomes.'),
 ('T8','Tool 3 — Derivative and Embedding Governance Decision Tool','Reassesses features, embeddings, synthetic data, predictions and trained models for identification, inference, computational persistence and leakage, then checks provenance, release conditions and lifecycle controls. Five outcomes: retain the tier, refer for Tier 4, confirm Tier 5, specialist review, or do not proceed.'),
 ('T9','Tool 4 — MDTAA Clause Selection Tool','Maps the recorded tier, pathway conditions and transformation findings to the modules of the Modular Neurodata Transfer and Access Agreement; Step 1A covers public releases governed by repository terms or a public licence rather than an MDTAA.'),
]
tool_tabs = ''.join(f'<button class="sub" data-sub="toolkit" data-id="t{i+1}">Tool {i+1}</button>' for i in range(4))
PDFS={'T6': 'Tool1_Neurodata_Governance_Decision_Tool.pdf', 'T7': 'Tool2_Neurodata_Transfer_and_Access_Decision_Tool.pdf', 'T8': 'Tool3_Derivative_and_Embedding_Governance_Decision_Tool.pdf', 'T9': 'Tool4_MDTAA_Clause_Selection_Tool.pdf'}
tool_panels = ''.join(f'<section class="subpanel" id="toolkit-t{i+1}"><p class="lead">{E(d)}</p>{tool_html(k,t,None)}</section>' for i,(k,t,d) in enumerate(tools))

# ---------- scenarios
def abstract(s):
    t=s["setting"]; 
    if len(t)<=190: return t
    cut=t[:190]; cut=cut[:cut.rfind(' ')]
    return cut+'…'

def strip_html(s):
    parts=[]
    for t in s['tools']:
        chips=''.join(f'<span class="chip"><b>{E(st)}</b> {E(a)}</span>' for st,a,_ in t['steps'])
        parts.append(f'<div class="lane"><div class="lanehead">{E(t["tool"])}</div><div class="chips">{chips}<span class="chip res">{E(t["result"])}</span></div></div>')
    return '<div class="strip">'+''.join(parts)+'</div>'

def scen_html(s):
    steps=''
    for t in s['tools']:
        rows=''.join(f'<tr><td class="k">{E(st)}</td><td>{E(a)}</td><td class="m">{E(n)}</td></tr>' for st,a,n in t['steps'])
        steps+=f'<details class="step" open><summary><span class="stepno">{E(t["tool"])}</span><span class="stepq">{E(t["result"])}</span></summary><table><thead><tr><th>Step</th><th>Answer</th><th>Note</th></tr></thead><tbody>{rows}</tbody></table></details>'
    legal=''.join(f'<li>{E(x)}</li>' for x in s['legal'])
    counsel=''.join(f'<li>{E(x)}</li>' for x in s['counsel'])
    return f'''<section class="subpanel" id="examples-{s["id"]}">
<h3>{E(s["title"])}</h3>
<p class="lead">{E(s["setting"])}</p>
<div class="facts"><b>Data provider</b><span>{E(s["exporter"])}</span><b>Recipient</b><span>{E(s["importer"])}</span><b>Data</b><span>{E(s["datadesc"])}</span><b>Origin regime</b><span>{E(s["origin"])}</span><b>Destination</b><span>{E(s["dest"])}</span><b>Access mode</b><span>{E(s["access"])}</span><b>Determination</b><span class="{"negtxt" if s["verdict_new"].lower().startswith("do not") else "postxt"}">{E(s["verdict_new"])}</span></div>
<h4>Path through the tools</h4>
{steps}
<div class="two"><div><h4>Legal points that decide the case</h4><ul>{legal}</ul></div><div><h4>Questions to put to counsel</h4><ul>{counsel}</ul></div></div>
</section>'''

ex_tabs=''.join(f'<button class="excard{" neg" if s["verdict_new"].lower().startswith("do not") else ""}" data-sub="examples" data-id="{s["id"]}" title="{E(s["verdict_new"])}"><span class="exname">{E(s["short"])}</span><span class="exmeta">{E(s["region"])}</span></button>' for s in SCENARIOS)
ex_panels=''.join(scen_html(s) for s in SCENARIOS)

page = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Neurodata Governance Toolkit Explorer</title>
<meta name="description" content="Interactive explorer for the decision-support toolkit for cross-border neurodata sharing: tools, workflow and ten worked examples.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500&display=swap">
<style>
:root{{--bg:#f7f8f6;--fg:#1d2230;--muted:#5a6273;--line:#c9cfd6;--panel:#fff;--accent:#005981;--accent2:#00405e;--new:#fff;--newline:#c9cfd6;--tier:#e6f0f5;--old:#a9262c;--good:#005981;--loop:#a9262c;--font:"IBM Plex Sans",system-ui,sans-serif;--mono:"IBM Plex Mono",ui-monospace,monospace}}
@media (prefers-color-scheme:dark){{:root{{--bg:#15181f;--fg:#e8eaf0;--muted:#a3abba;--line:#3a4150;--panel:#1d2129;--accent:#5fb0d6;--accent2:#002b40;--new:#1d2129;--newline:#3a4150;--tier:#1e3340;--old:#e0666b;--good:#5fb0d6;--loop:#e0666b;color-scheme:dark}}}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--bg);color:var(--fg);font-family:var(--font);font-size:15px;line-height:1.55}}
header{{background:var(--accent2);color:#fff;padding:22px max(16px,env(safe-area-inset-left)) 0}}
.wrap{{max-width:1240px;margin:0 auto;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px))}}
header h1{{margin:0;font-size:1.55rem;font-weight:600}}
.stripe{{height:6px;background:linear-gradient(90deg,#005981 0 25%,#a9262c 25% 50%,#e57536 50% 75%,#f9c926 75% 100%)}}
.sitebar{{background:#002b40;color:#fff;font-size:.9rem}} .sitebar .wrap{{display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px;padding:8px 0}} .sitebar .sbrand{{color:#fff;text-decoration:none;font-weight:600}} .sitebar nav{{display:flex;gap:2px;flex-wrap:wrap}} .sitebar nav a{{color:#fff;opacity:.8;text-decoration:none;padding:5px 10px;border-radius:6px}} .sitebar nav a:hover,.sitebar nav a.active{{opacity:1;background:rgba(255,255,255,.14)}} a.parent{{color:#fff;opacity:.8;text-decoration:none;font-size:.85rem;display:inline-block;margin-bottom:6px}} a.parent:hover{{opacity:1;text-decoration:underline}}
header p{{margin:4px 0 14px;opacity:.85;max-width:80ch}}
nav.tabs{{display:flex;flex-wrap:wrap;gap:4px}}
nav.tabs button{{background:transparent;border:0;color:#fff;opacity:.75;padding:10px 14px;font:inherit;font-weight:500;border-radius:6px 6px 0 0;cursor:pointer}}
nav.tabs button.active{{background:var(--bg);color:var(--fg);opacity:1}}
nav.tabs a.tablink{{color:#fff;opacity:.85;padding:10px 14px;font-weight:500;text-decoration:none;border-radius:6px 6px 0 0;margin-left:auto;border:1px solid rgba(255,255,255,.35)}} nav.tabs a.tablink:hover{{opacity:1;background:rgba(255,255,255,.12)}}
nav.tabs button:focus-visible{{outline:2px solid #fff}}
main{{padding-block:22px 60px}}
.panel{{display:none}} .panel.active{{display:block}}
.subtabs{{display:flex;flex-wrap:wrap;gap:6px;margin:0 0 16px}}
.subtabs button{{background:var(--panel);border:1px solid var(--line);color:var(--fg);padding:6px 11px;border-radius:999px;font:inherit;font-size:.9rem;cursor:pointer}}
.subtabs button.active{{background:var(--accent);border-color:var(--accent);color:#fff}}
.subpanel{{display:none}} .subpanel.active{{display:block}}
h2{{font-size:1.35rem;font-weight:600;margin:0 0 .4rem}} h3{{font-size:1.15rem;font-weight:600;margin:1.2rem 0 .5rem}} h4{{font-size:1rem;margin:1.2rem 0 .4rem}}
p,li{{max-width:78ch}} .lead{{color:var(--muted)}}
.card{{background:var(--panel);border:1px solid var(--line);border-radius:8px;padding:16px 18px;margin:0 0 14px}}
.fourtools{{list-style:none;margin:0 0 18px;padding:0;max-width:78ch}} .fourtools li{{margin:0 0 10px;padding-left:2.2em;text-indent:-2.2em}} .fourtools b{{font-family:var(--mono);color:var(--accent);font-weight:500;margin-right:.6em}}
details.step{{border-top:1px solid var(--line);margin:0}} details.step:last-of-type{{border-bottom:1px solid var(--line)}} details.step[open]{{padding-bottom:10px}}
details.step.chg{{border-color:var(--newline);background:color-mix(in srgb,var(--new) 45%,var(--panel))}}
details.step summary{{cursor:pointer;padding:10px 4px;display:flex;gap:12px;align-items:baseline;list-style:none}} details.step summary:hover .stepq{{color:var(--accent)}} details.step table{{margin:4px 0 0 0}}
details.step summary::-webkit-details-marker{{display:none}}
details.step summary::before{{content:"▸";color:var(--accent);flex:0 0 auto}} details.step[open] summary::before{{content:"▾"}}
.stepno{{font-family:var(--mono);font-weight:500;color:var(--accent);flex:0 0 auto;min-width:3.2em}} .stepq{{flex:1 1 auto;min-width:0}}
.tag{{font-size:.72rem;letter-spacing:.06em;text-transform:uppercase;background:var(--newline);color:#fff;padding:2px 7px;border-radius:4px;flex:0 0 auto}}
table{{border-collapse:collapse;width:100%;font-size:.9rem}} th,td{{text-align:left;vertical-align:top;padding:8px 10px;border-top:1px solid var(--line)}} th{{color:var(--muted);font-weight:600;font-size:.8rem;text-transform:uppercase;letter-spacing:.05em}}
tr.chg td{{background:var(--new)}}
td.k{{font-family:var(--mono);white-space:nowrap}} td.m{{color:var(--muted)}}
.tablewrap{{overflow-x:auto}}
.note{{background:var(--tier);border-left:3px solid var(--accent);padding:8px 12px;margin:0 0 8px;font-size:.9rem;color:var(--muted)}} .note.chg{{background:var(--new);border-left-color:var(--newline);color:var(--fg)}}
.controls{{display:flex;gap:14px;flex-wrap:wrap;align-items:center;margin:0 0 12px;font-size:.9rem}} .controls button.sub{{background:none;border:0;padding:0;color:var(--accent);font:inherit;font-size:.9rem;cursor:pointer;text-decoration:underline}}
.controls input[type=search]{{font:inherit;padding:6px 10px;border:1px solid var(--line);border-radius:6px;background:var(--panel);color:var(--fg);min-width:240px}}
.facts{{display:grid;grid-template-columns:max-content 1fr;gap:6px 18px;margin:14px 0 6px;font-size:.92rem;max-width:90ch}} .facts b{{font-size:.72rem;text-transform:uppercase;letter-spacing:.06em;color:var(--muted);padding-top:3px;font-weight:600}} .facts span{{display:block}} @media (max-width:560px){{.facts{{grid-template-columns:1fr;gap:2px}} .facts span{{margin-bottom:8px}}}}
.verdicts{{display:flex;gap:10px;flex-wrap:wrap;margin:8px 0 4px}} .v{{padding:5px 10px;border-radius:999px;font-size:.85rem;border:1.5px solid}} .v.old{{border-color:var(--old);color:var(--old)}} .v.new{{border-color:var(--good);color:var(--good)}}
.strip{{display:flex;flex-direction:column;gap:8px;margin:6px 0 10px}}
.lane{{display:grid;grid-template-columns:150px 1fr;gap:10px;align-items:start}} .lanehead{{font-weight:600;font-size:.9rem;padding-top:6px}}
.chips{{display:flex;flex-wrap:wrap;gap:6px}} .chip{{background:var(--panel);border:1px solid var(--line);border-radius:6px;padding:4px 8px;font-size:.82rem}} .chip b{{font-family:var(--mono);color:var(--accent);font-weight:500;margin-right:4px}} .chip.res{{background:var(--tier);border-color:var(--accent);font-weight:600}}
.callout{{border-left:3px solid var(--old);background:var(--panel);padding:10px 14px;margin:14px 0;font-size:.95rem}}
.two{{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:20px}}
figure{{margin:0 0 18px;padding:0}} .iwf-legend button.sub{{background:none;border:0;padding:0;color:var(--accent);font:inherit;font-size:.85rem;cursor:pointer;text-decoration:underline}} figcaption{{color:var(--muted);font-size:.9rem;margin-top:8px}}
.scroll{{overflow-x:auto}} #wf{{min-width:1200px;width:100%;height:auto;display:block}}
.legend{{display:flex;flex-wrap:wrap;gap:12px 20px;font-size:.85rem;color:var(--muted);margin:0 0 10px}} .legend span{{display:inline-flex;align-items:center;gap:6px}} .sw{{width:20px;height:13px;border:1.5px solid var(--line);border-radius:3px;background:var(--panel)}} .sw.new{{background:var(--new);border-color:var(--newline)}} .sw.tier{{background:var(--tier);border-color:var(--accent)}} .sw.loop{{border:0;height:2px;background:var(--loop);width:24px}}
.tierlist{{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:10px}} .tierlist div{{background:var(--panel);border:1px solid var(--line);border-left:4px solid var(--accent);border-radius:6px;padding:8px 12px;font-size:.92rem}} .tierlist div.new{{border-left-color:var(--newline)}} .tierlist b{{display:block}}
td.old{{color:var(--old)}} td.new{{color:var(--good)}}
.excards{{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:2px 32px;margin:0 0 28px;max-width:960px}}
@media (max-width:640px){{.excards{{grid-template-columns:1fr}}}}
.exdet.neg,.negtxt{{color:var(--old)}} .postxt{{color:var(--good);font-weight:600}}

.excard{{text-align:left;background:none;border:0;border-bottom:1px solid var(--line);padding:7px 4px 7px 18px;position:relative;font:inherit;color:var(--fg);cursor:pointer;display:block;width:100%}}
.excard:hover .exname{{color:var(--accent)}} .excard.active .exname{{color:var(--accent);text-decoration:underline;text-underline-offset:3px}}
.excard:focus-visible{{outline:2px solid var(--accent);outline-offset:2px}}
.excard::before{{content:"";position:absolute;left:2px;top:14px;width:8px;height:8px;border-radius:50%;background:var(--good)}} .excard.neg::before{{background:var(--old)}} .exname{{font-weight:500;font-size:.92rem;line-height:1.3}} .exmeta{{display:block;font-size:.7rem;color:var(--muted);text-transform:uppercase;letter-spacing:.04em;margin-top:1px}} .exabs{{font-size:.88rem;color:var(--muted);line-height:1.45}} .exdet{{font-size:.78rem;color:var(--good);font-weight:600;margin-top:2px}}

footer{{color:var(--muted);font-size:.85rem;border-top:1px solid var(--line);padding-top:14px;margin-top:30px}}
a{{color:var(--accent)}}
.dls{{font-size:.9rem;color:var(--muted);margin:0 0 18px;max-width:none}} .dls a{{white-space:nowrap}} a.dl{{font-weight:500;text-decoration:none;border-bottom:1px solid currentColor}} a.dl:hover{{color:var(--accent2)}} .links a.dl{{margin-right:14px}}
@media (max-width:600px){{.lane{{grid-template-columns:1fr}}}}
{TIER_CSS}
{iwf.CSS}
</style>
</head>
<body>
<div class="sitebar"><div class="wrap"><a class="sbrand" href="/"><svg viewBox="0 0 120 120" width="24" height="24" style="vertical-align:-6px;margin-right:8px" aria-hidden="true">  <circle cx="60" cy="60" r="58" fill="#ffffff"/>  <polygon points="85.5,34.5 53.6,53.6 60,60 66.4,66.4" fill="#1d2230"/><polygon points="34.5,34.5 53.6,66.4 60,60 66.4,53.6" fill="#1d2230"/><polygon points="34.5,85.5 66.4,66.4 60,60 53.6,53.6" fill="#1d2230"/><polygon points="85.5,85.5 66.4,53.6 60,60 53.6,66.4" fill="#1d2230"/>  <polygon points="60.0,4.0 44.0,60.0 60,60 76.0,60.0" fill="#f9c926"/><polygon points="116.0,60.0 60.0,44.0 60,60 60.0,76.0" fill="#e57536"/><polygon points="60.0,116.0 76.0,60.0 60,60 44.0,60.0" fill="#a9262c"/><polygon points="4.0,60.0 60.0,76.0 60,60 60.0,44.0" fill="#005981"/>  <circle cx="60" cy="60" r="7" fill="#ffffff" stroke="#1d2230" stroke-width="4"/></svg>Global Brain Governance</a><nav><a href="/about/">About</a><a class="active" href="/toolkit/">Toolkit</a></nav></div></div>
<div class="stripe"></div>
<header><div class="wrap">
<h1>Neurodata Governance Toolkit</h1>
<p>Decision support for sharing neural data across borders. Version {SITE['toolkit_version']}, {SITE['toolkit_date']}.</p>
<nav class="tabs" role="tablist">
<button data-tab="intro" class="active">Introduction</button><button data-tab="toolkit">Toolkit</button><button data-tab="workflow">Workflow</button><button data-tab="examples">Examples</button><button data-tab="about">Sources &amp; status</button><a class="tablink" href="/toolkit/legal-landscape/">Legal landscape ↗</a>
</nav></div></header>
<main class="wrap">

<section class="panel active" id="panel-intro">
<p class="lead" style="font-size:1.2rem;max-width:60ch">Four tools that take a collaboration from “what are these data?” to the clauses its agreement needs.</p>
<ul class="fourtools">
<li><b>Tool 1</b><strong>Classify.</strong> What can the data reveal or enable, for this recipient? Tool 1 assigns a tier by functional exposure.</li>
<li><b>Tool 2</b><strong>Test the pathway.</strong> Can the proposed transfer, access or public release carry the safeguards that tier requires? Tool 2 decides: proceed, proceed after safeguards, redesign, or do not proceed.</li>
<li><b>Tool 3</b><strong>Reassess derivatives and models.</strong> Features, embeddings, synthetic data and model weights are reassessed for identification, inference, persistence and leakage before they circulate. Tool 3 retains the tier, refers to Tier 4 or 5, or stops.</li>
<li><b>Tool 4</b><strong>Select the clauses.</strong> Tool 4 maps the results to the modules of the Modular Neurodata Transfer and Access Agreement (MDTAA).</li>
</ul>
<p>Built from the law of 93 countries in Africa, Europe, and Latin America and the Caribbean. The tools structure the questions and record the answers. They do not establish that a transfer is lawful, and they do not replace ethics, repository, institutional or legal review.</p>
<h3>Tiered Neurodata Risk Classification Framework based on functional exposure</h3>
<p class="lead">Classifying neurodata by the capacity to enable inference, reconstruction, profiling or harm. Download the figure as <a class="dl" href="pdf/Figure_Tiers.png" download>PNG</a> or <a class="dl" href="pdf/Figure_Tiers.pdf" download>PDF</a>.</p>
{tiers_html()}
</section>

<section class="panel" id="panel-toolkit">
<h2>The four tools</h2>
<p class="lead">Each tool is a sequence of questions. Click a step to see its answer rows and required actions.</p>
<div class="controls"><input type="search" id="toolsearch" placeholder="Filter steps (e.g. public release, Tier 4, EHDS)"><button class="sub" id="expandall">Expand all</button><button class="sub" id="collapseall">Collapse all</button></div>
<p class="dls">Print-ready PDFs (A4 landscape): <a class="dl" href="pdf/Toolkit_Tools_1-4.pdf" download>all four tools (48 pp.)</a> · <a class="dl" href="pdf/Tool1_Neurodata_Governance_Decision_Tool.pdf" download>Tool 1</a> · <a class="dl" href="pdf/Tool2_Neurodata_Transfer_and_Access_Decision_Tool.pdf" download>Tool 2</a> · <a class="dl" href="pdf/Tool3_Derivative_and_Embedding_Governance_Decision_Tool.pdf" download>Tool 3</a> · <a class="dl" href="pdf/Tool4_MDTAA_Clause_Selection_Tool.pdf" download>Tool 4</a> · workflow figure (<a class="dl" href="pdf/Figure_Workflow_Toolkit.png" download>PNG</a>, <a class="dl" href="pdf/Figure_Workflow_Toolkit.svg" download>SVG</a>) · tier figure (<a class="dl" href="pdf/Figure_Tiers.png" download>PNG</a>, <a class="dl" href="pdf/Figure_Tiers.pdf" download>PDF</a>)</p>
<div class="subtabs" data-group="toolkit">{tool_tabs}</div>
{tool_panels}
</section>

<section class="panel" id="panel-workflow">
<h2>Workflow</h2>
<p class="lead">The four tools are used in sequence: classify the object, assess the pathway (controlled access or public release), reassess any transformation, then select the contract modules. Linkage, AI use and material changes loop back to earlier tools.</p>
<p class="dls">Download the figure as <a class="dl" href="pdf/Figure_Workflow_Toolkit.png" download>PNG</a> or <a class="dl" href="pdf/Figure_Workflow_Toolkit.svg" download>SVG</a>.</p>
{iwf.html()}
</section>

<section class="panel" id="panel-examples">
<h2>Sixteen worked examples</h2>
<p class="lead">Realistic arrangements drawn from current practice in the sampled regions; a red dot marks the cases that end in “do not proceed”. Click one to open it below the list.</p>
<div class="excards" data-group="examples">{ex_tabs}</div>
{ex_panels}
</section>

<section class="panel" id="panel-about">
<h2>Sources and status</h2>
<p>The four tools are published in the study <i>A decision support toolkit for AI-ready neuroscience data governance</i> (Botes et al., 2026), where they appear as Supplementary Tables 6–9; this is version {SITE['toolkit_version']}. The study’s compatibility matrix, network and maps are interactive in the <a href="/toolkit/legal-landscape/">Legal landscape</a>. Legal statements reflect the law in force at {SITE['legal_content_date']}; items marked [verify] in the examples await confirmation by the regional co-authors. Nothing on this site is legal advice.</p>
<h3>Principal legal sources used in the examples</h3>
<ul>
<li>European Commission adequacy decisions (Argentina, Uruguay, UK renewal 19 Dec 2025, Brazil C(2026) 373 of 26 Jan 2026); EU SCCs, Decision (EU) 2021/914; EDPB Opinion 28/2024; CJEU C-413/23 P (4 Sept 2025); Regulation (EU) 2025/327 (EHDS); AI Act as amended by the Digital Omnibus (June 2026).</li>
<li>Lei 13.709/2018 (LGPD) arts 5, 11, 13, 33, 35; Resolução CD/ANPD 19/2024.</li>
<li>POPIA ss. 26, 34, 57, 72; NHREC Guidelines (2024); SA DTA 1.1.</li>
<li>Nigeria Data Protection Act 2023 ss. 30, 41–43; NDPC GAID 2025.</li>
<li>Kenya Data Protection (General) Regulations 2021 regs 26, 40–48; Rwanda Law 058/2021 arts 48–50; Botswana Act 18 of 2024.</li>
<li>Québec Act respecting the protection of personal information in the private sector ss. 17, 21; PIPEDA; PHIPA.</li>
<li>28 CFR Part 202 (DOJ Data Security Program); 45 CFR 164.514; 45 CFR 46; OFAC 31 CFR 515; Colorado HB24-1058; California SB 1223.</li>
<li>Chile Law 21.719 (in force 1 Dec 2026), Law 21.383, Corte Suprema Rol 105.065-2023; Mexico LFPDPPP (20 March 2025); Peru DS 016-2024-JUS; Finland Act 552/2019.</li>
</ul>
<footer>Part of <a href="/">{SITE['name']}</a> · © {SITE.get('copyright_year')} {SITE['maintainer']}. All rights reserved for the site name and design. Content is licensed <a href="https://creativecommons.org/licenses/by/4.0/">CC BY 4.0</a> unless stated otherwise; code under the MIT licence. Nothing on this site is legal advice.</footer>
</section>
</main>
<script>
{iwf.JS}
const TABLES={json.dumps({k:len(v) for k,v in T.items()})};
(function(){{
const tabs=[...document.querySelectorAll('nav.tabs button')],panels={{}};tabs.forEach(b=>panels[b.dataset.tab]=document.getElementById('panel-'+b.dataset.tab));
const subState={{toolkit:'t1',examples:'s1'}};
function showTab(t){{tabs.forEach(b=>b.classList.toggle('active',b.dataset.tab===t));for(const k in panels)panels[k].classList.toggle('active',k===t);window.scrollTo({{top:0}});}}
function showSub(g,id){{subState[g]=id;document.querySelectorAll(`[data-group="${{g}}"] button`).forEach(b=>b.classList.toggle('active',b.dataset.id===id));document.querySelectorAll(`#panel-${{g}} .subpanel`).forEach(p=>p.classList.toggle('active',p.id===g+'-'+id));if(g==='examples'&&window.__userClick){{const p=document.getElementById(g+'-'+id);if(p)p.scrollIntoView({{behavior:'smooth',block:'start'}});window.__userClick=false;}}}}
function route(){{const h=(location.hash||'#intro').slice(1).split('/');const t=panels[h[0]]?h[0]:'intro';showTab(t);if(h[1]&&(t==='toolkit'||t==='examples'))showSub(t,h[1]);else if(t==='toolkit'||t==='examples')showSub(t,subState[t]);}}
tabs.forEach(b=>b.addEventListener('click',()=>{{location.hash='#'+b.dataset.tab+((b.dataset.tab==='toolkit'||b.dataset.tab==='examples')?'/'+subState[b.dataset.tab]:'');}}));
document.querySelectorAll('.subtabs button,.excards button').forEach(b=>b.addEventListener('click',()=>{{window.__userClick=true;location.hash='#'+b.dataset.sub+'/'+b.dataset.id;}}));
window.addEventListener('hashchange',route);route();
// toolkit filters
const search=document.getElementById('toolsearch');
function filter(){{const q=search.value.trim().toLowerCase();document.querySelectorAll('#panel-toolkit details.step').forEach(d=>{{const ok=(!q||d.textContent.toLowerCase().includes(q));d.style.display=ok?'':'none';if(q)d.open=true;}});}}
search.addEventListener('input',filter);
document.getElementById('expandall').addEventListener('click',()=>document.querySelectorAll('#panel-toolkit .subpanel.active details').forEach(d=>d.open=true));
document.getElementById('collapseall').addEventListener('click',()=>document.querySelectorAll('#panel-toolkit .subpanel.active details').forEach(d=>d.open=false));
}})();
</script>
</body>
</html>'''
open(os.path.join(HERE,'..','..','toolkit','index.html'),'w',encoding='utf-8').write(page)
print(len(page))
