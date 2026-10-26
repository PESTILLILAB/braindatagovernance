import os, yaml
_T = yaml.safe_load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'data', 'tiers.yml')))
TIERS = [(x['id'], x['name'], x['description'], x['examples'], x['background'], x['text_colour'], False) for x in _T]

def tiers_html(standalone=False):
    rows=''
    for n,t,d,ex,bg,fg,new in TIERS:
        exl=''.join(f'<li>{x}</li>' for x in ex)
        rows+=f'''<div class="tier{" new" if new else ""}" style="--tbg:{bg};--tfg:{fg}">
  <div class="tnum">{n}</div>
  <div class="tbody"><div class="ttitle">{t}</div><div class="tdesc">{d}</div></div>
  <ul class="tex">{exl}</ul>
</div>'''
    return f'''<div class="tierfig">
<div class="tierhead"><div>Risk category</div><div>Risk tier &amp; description</div><div>Illustrative artefacts requiring assessment</div></div>
<div class="tiergrid">
 <div class="tcat tcat1"><b>Conventional privacy-based risk</b><span>Tiers 1, 2 and 3</span><p>Risk linked primarily to aggregation, participant linkage, identifiability and traceability.</p></div>
 <div class="tcat tcat2"><b>Post-transformation functional-exposure tiers</b><span>Tiers 4 and 5</span><p>Risk driven by the capacity to support inference, profiling or harm, independent of identifiability.</p></div>
 <div class="tiers">{rows}</div>
</div>
<div class="tkey"><b>Key principle</b> Tier assignment is informed by functional exposure; legal status remains determined under applicable law. The highest applicable tier governs; safeguards are cumulative; an Unknown answer is governed under the more protective tier until resolved; incorporation into a model triggers assessment but does not by itself establish Tier 5.</div>
</div>'''

TIER_CSS = '''
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
'''
