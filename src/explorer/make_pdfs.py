import os; HERE = os.path.dirname(os.path.abspath(__file__)); PDF = os.path.join(HERE,'..','..','_build','pdf')   # intermediate HTML; the PDFs themselves go to toolkit/pdf (see topdf.js)
import json, html, subprocess, os
import yaml
T = yaml.safe_load(open(os.path.join(HERE, '..', '..', 'data', 'tools.yml')))
E = lambda s: html.escape(str(s))
TOOLS = [
 ('T6','Tool 1','Neurodata Governance Decision Tool','Supplementary Table 6','Scientist-facing decision tool for assigning a provisional functional-exposure tier (5, 4, 3, 2, 1) to the particular neurodata object or artefact under assessment and identifying the corresponding baseline safeguards. The assessment considers technical form together with identifiability, traceability, inferential capacity, reconstruction potential and computational persistence. Model incorporation triggers further assessment but does not automatically determine Tier 5. A tier is confirmed only when all applicable steps and required reviews are complete; an Unknown answer produces a provisional tier; a Tool 3 referral identifies a candidate tier.'),
 ('T7','Tool 2','Neurodata Transfer and Access Decision Tool (Neuro-TADT)','Supplementary Table 7','Assesses whether the safeguards associated with the tier assigned under Tool 1 can be maintained across a proposed sharing, repository, remote-access, cloud or cross-border pathway. Step 3 separates a controlled-access pathway (Steps 4A–12A) from a public-release pathway (Steps 4B–12B). Four outcomes: proceed subject to applicable approvals; proceed after supplementary safeguards; redesign the pathway; do not proceed and obtain specialist review.'),
 ('T8','Tool 3','Derivative and Embedding Governance Decision Tool','Supplementary Table 8','Assesses whether technical transformation (features, embeddings, synthetic data, predictions, trained models) has materially changed functional exposure and whether the tier or safeguards require reassessment. Five outcomes: retain the existing tier; refer for Tier 4; confirm Tier 5; specialist review required; do not proceed in the current form.'),
 ('T9','Tool 4','MDTAA Clause Selection Tool','Supplementary Table 9','Maps the outcomes of Tools 1–3 to the modules of the Modular Neurodata Transfer and Access Agreement. Module selection does not establish lawfulness or enforceability.'),
]

CSS = '''
@page{size:A4 landscape;margin:14mm 12mm 16mm 12mm}
body{font-family:"Helvetica Neue",Arial,sans-serif;font-size:9pt;color:#1d2230;margin:0}
h1{font-size:16pt;margin:0 0 2pt} .sub{color:#555;font-size:10pt;margin:0 0 6pt}
p.desc{font-size:9pt;max-width:95%;margin:0 0 8pt}
.note{background:#e4eef2;border-left:3px solid #1f6f8b;padding:5pt 8pt;margin:0 0 8pt;font-size:8.5pt}
table{border-collapse:collapse;width:100%;table-layout:fixed}
th,td{border:1px solid #b9c0c8;padding:4pt 5pt;vertical-align:top;font-size:8pt;line-height:1.3;word-wrap:break-word}
th{background:#d9e2f3;font-weight:700;text-align:left}
thead{display:table-header-group} tr{page-break-inside:avoid}
td.band{background:#ededed;font-style:italic}
.legend{font-size:8pt;color:#555;margin:0 0 6pt} .legend i{display:inline-block;width:14pt;height:8pt;border:1px solid #b38600;background:#fff3c4;vertical-align:middle;margin-right:3pt}
footer{font-size:7.5pt;color:#666;margin-top:8pt}
'''
def table_html(key):
    rows=T[key]; hdr=rows[0]; n=len(hdr)
    widths={5:['6%','34%','12%','12%','36%'],4:['6%','36%','15%','43%']}[n]
    out=['<table><colgroup>'+''.join(f'<col style="width:{w}">' for w in widths)+'</colgroup><thead><tr>'+''.join(f'<th>{E(h)}</th>' for h in hdr)+'</tr></thead><tbody>']
    for r in rows[1:]:
        chg=r[-1]=='__CHANGED__'; c=r[:-1] if chg else r[:]
        while len(c)<n: c.append('')
        if sum(1 for x in c if x)==1 and c[0]:
            out.append(f'<tr><td colspan="{n}" class="band{" chg" if chg else ""}">{E(c[0])}</td></tr>'); continue
        out.append(f'<tr class="{"chg" if chg else ""}">'+''.join(f'<td>{E(x)}</td>' for x in c)+'</tr>')
    out.append('</tbody></table>'); return ''.join(out)

def doc(parts, title):
    body=''.join(parts)
    return f'<!doctype html><html><head><meta charset="utf-8"><title>{E(title)}</title><style>{CSS}</style></head><body>{body}<footer>Neurodata Governance Toolkit, version 1.0 (October 2026). Governance decision support only; not legal advice.</footer></body></html>'

def tool_part(key,short,name,sub,desc):
    extra = ''
    return f'<h1>{E(short)} — {E(name)}</h1><p class="sub">{E(sub)}</p><p class="desc">{E(desc)}</p>{extra}{table_html(key)}'

os.makedirs(PDF,exist_ok=True)
files=[]
for key,short,name,sub,desc in TOOLS:
    fn=PDF+f'/{short.replace(" ","")}_{name.split("(")[0].strip().replace(" ","_")}.html'
    open(fn,'w').write(doc([tool_part(key,short,name,sub,desc)],f'{short} — {name}')); files.append(fn)
allfn=PDF+'/Toolkit_Tools_1-4.html'
open(allfn,'w').write(doc([tool_part(*t)+'<div style="page-break-after:always"></div>' for t in TOOLS],'Neurodata Governance Toolkit — Tools 1–4')); files.append(allfn)
json.dump(files,open(PDF+'/_files.json','w'))
print('\n'.join(files))


# ---- standalone tier figure (rendered to PNG/PDF by tierfig.js)
from tiers import tiers_html
TIER_HEAD = """<!doctype html><html><head><meta charset="utf-8"><title>Tiered Neurodata Risk Classification Framework</title>
<style>body{margin:0;background:#fff;padding:28px 32px;font-family:"Helvetica Neue",Arial,sans-serif;color:#1d2230} h1{font-size:24px;margin:0 0 4px;color:#1b3f5c} .sub{font-style:italic;color:#5a6273;margin:0 0 16px;font-size:15px} 
.tierfig{--line:#c9cfd6;font-family:"IBM Plex Sans",system-ui,sans-serif;color:#1d2230;max-width:1240px}
.tierhead{display:grid;grid-template-columns:200px 1fr 1fr;gap:12px;font-size:.78rem;letter-spacing:.06em;text-transform:uppercase;color:#5a6273;font-weight:600;margin:0 0 8px}
.tiergrid{display:grid;grid-template-columns:200px 1fr;grid-template-rows:auto auto;gap:12px}
.tcat{background:#fff;border:1px solid #c9cfd6;border-radius:10px;padding:14px 14px;font-size:.85rem;color:#5a6273}
.tcat b{display:block;color:#1d2230;font-size:.95rem;margin-bottom:2px} .tcat span{display:block;font-size:.78rem;letter-spacing:.04em;text-transform:uppercase;margin-bottom:6px;color:#1f6f8b} .tcat p{margin:0}
.tcat1{grid-row:1;grid-column:1} .tcat2{grid-row:2;grid-column:1}
.tiers{grid-column:2;grid-row:1 / span 2;display:flex;flex-direction:column;gap:8px}
.tier{display:grid;grid-template-columns:64px 1fr 1fr;gap:0;background:var(--tbg);color:var(--tfg);border:1px solid #b9c0c8;border-radius:10px;overflow:hidden}
.tnum{display:flex;align-items:center;justify-content:center;font-size:1.5rem;font-weight:700;background:rgba(255,255,255,.35);border-right:1px solid rgba(0,0,0,.08)}
.tbody{padding:12px 14px} .ttitle{font-weight:700;font-size:.95rem;text-transform:uppercase;letter-spacing:.02em;margin-bottom:4px} .tdesc{font-size:.86rem;line-height:1.4}
.tex{margin:0;padding:12px 14px 12px 30px;background:rgba(255,255,255,.75);color:#1d2230;font-size:.86rem;line-height:1.5;border-left:1px solid rgba(0,0,0,.08)}
.tkey{margin-top:12px;background:#fff;border:1px solid #c9cfd6;border-radius:10px;padding:10px 14px;font-size:.9rem} .tkey b{color:#1f6f8b;margin-right:8px;text-transform:uppercase;font-size:.8rem;letter-spacing:.06em}
@media (prefers-color-scheme:dark){.tierfig{color:#e8eaf0}.tcat,.tkey{background:#1d2129;border-color:#3a4150;color:#a3abba}.tcat b,.tkey{color:#e8eaf0}.tierhead{color:#a3abba}.tex{background:rgba(255,255,255,.85)}}
@media (max-width:760px){.tiergrid,.tierhead{grid-template-columns:1fr}.tiers{grid-column:1;grid-row:auto}.tcat1,.tcat2{grid-column:1;grid-row:auto}.tier{grid-template-columns:48px 1fr}.tex{grid-column:1 / span 2;border-left:0;border-top:1px solid rgba(0,0,0,.08)}.tierhead div:nth-child(3){display:none}}
 @page{size:A4 landscape;margin:10mm}</style></head>
"""
open(PDF+'/_tiers_fig.html','w').write(TIER_HEAD+"""<body><div id="fig"><h1>Tiered Neurodata Risk Classification Framework based on functional exposure</h1><p class="sub">Classifying neurodata by the capacity to enable inference, reconstruction, profiling or harm.</p>"""+tiers_html(standalone=True)+'</div></body></html>')
print('wrote', PDF+'/_tiers_fig.html')
