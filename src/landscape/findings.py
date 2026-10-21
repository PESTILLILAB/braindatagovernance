"""Generates content/findings.html (the Legal landscape page) from matrix.json and geo.json.
Run: python3 src/landscape/findings.py   then   python3 src/build.py
"""
import os, json, yaml
HERE = os.path.dirname(os.path.abspath(__file__))
SITE = yaml.safe_load(open(os.path.join(HERE, '..', '..', 'data', 'site.yml')))
D = json.load(open(os.path.join(HERE,'matrix.json')))

BODY = '''
<h1 style="font-size:2rem;font-weight:600;margin:1.2rem 0 .4rem">The legal landscape behind the Toolkit</h1>
<p class="lead">How 93 countries in Africa, Europe, and Latin America and the Caribbean treat the transfer of brain data, and what that means for a collaboration between any two of them. Legal experts in each region reviewed 477 laws and regulations across six layers of governance, and every one of the 8,556 country-to-country pathways is rated for the conditions it imposes in practice. Hover for detail, click to pin.</p>


<h2 id="fig1">Six layers of governance</h2>
<p>We look at each jurisdiction through six layers, from how it recognises neural data to what its contracts must carry. The layers build on each other: what a jurisdiction recognises (layer 1) determines which lawful bases are available (layer 2), which determines whether and how transfer can occur (layer 3), and only then does the question become whether protection remains effective in practice (layers 4–6). Click a layer.</p>
<div class="figwrap"><div class="layers" id="layers"></div><aside class="figside" id="layerside"><b>Select a layer</b><p>Each layer shows what it examines, the question the coders answered, and which tool in the toolkit it informed.</p></aside></div>

<h2 id="fig3a">The compatibility matrix: every pathway between every pair</h2>
<p>Rows are exporting jurisdictions, columns receiving jurisdictions; each cell is the class assigned to that direction. A1 (dark green) is a unified legal space, A2 (light green) highly convergent architectures, B (yellow) pathways supported by standard transfer instruments, C (orange) operationally conditional pathways, D (red) pathways restricted in practice and E (grey) insufficient legal certainty. Hover a cell for its class; click a cell to pin the pair and read both directions and both countries; click the diagonal for a single country's profile. The classes are structured indicators of practical navigability, not findings of legal adequacy.</p>
<div class="controls"><label>Highlight region <select id="regsel"><option value="">all</option><option>Europe</option><option>Africa</option><option>Latin America &amp; Caribbean</option></select></label><label>Find jurisdiction <input type="search" id="jsearch" placeholder="e.g. Kenya"></label><span class="legend" id="classlegend"></span></div>
<div class="figwrap"><div class="scroll"><canvas id="matrix" width="930" height="930" style="max-width:100%;height:auto;display:block"></canvas></div><aside class="figside" id="matside"><b>Hover or click a cell</b><p>The profile shows the jurisdiction’s outgoing and incoming class distribution, its modal class for imports from the European reference set, and the entropy of its incoming conditions.</p></aside></div>

<h2 id="fig3b">Where sharing is enabled</h2>
<p>The network keeps only pathways of class A1, A2 or B (weighted 3, 2, 1). Node size is the sum of weighted in- and out-strength; the European cluster is dense because every EU pair is A1 and the UK and Switzerland are A2 with all of them. Click a node to show its enabled pathways; the thin lines are B, the thick ones A1/A2.</p>
<div class="figwrap"><div class="scroll"><svg id="net" viewBox="0 0 900 620" role="img" aria-label="Network of enabled transfer pathways among 93 jurisdictions, grouped by region" style="width:100%;max-width:900px;height:auto;display:block"></svg></div><aside class="figside" id="netside"><b>Click a node</b><p>Shows the jurisdiction’s enabled pathways and its weighted strength.</p></aside></div>

<h2 id="fig3c">On the map: receiving data from Europe, or from anywhere</h2>
<p>Each jurisdiction is shaded by the modal class of the pathways that originate in the sampled European jurisdictions (24 origins; 23 for European destinations). Outside Europe the dominant condition is C: transfers are possible, but practical governance depends on supplementary contractual, institutional or repository controls. The map is interactive: hover a country for its value, click it to pin its profile, or change the origin to see the conditions any sampled jurisdiction faces when exporting to the rest of the sample. The United States and Canada are shown in dark grey because they were analysed as governance units rather than at country level.</p>
<div class="controls"><label>Origin <select id="orig"><option value="EU">European reference set (modal class)</option></select></label><label>Direction <select id="dir"><option value="out">exports from origin → destinations</option><option value="in">imports into origin ← sources</option></select></label><span class="legend" id="maplegend"></span></div>
<div class="figwrap"><div class="scroll"><svg id="map3c" class="map" role="img" aria-label="Map of the sampled jurisdictions shaded by the compatibility class of imports from Europe"></svg></div><aside class="figside" id="map3cside"><b>Hover or click a country</b><p>Shows the class of the pathway from the selected origin, and on click the jurisdiction’s full profile.</p></aside></div>

<h2 id="fig3d">On the map: how varied the conditions are</h2>
<p>Jurisdictions are shaded by the Shannon entropy (bits) of their incoming compatibility profile across the six classes. High entropy means a researcher there faces very different conditions depending on where data come from; low entropy means uniform conditions, whether uniformly enabled or uniformly restricted, so entropy is read together with the classes themselves. European jurisdictions score highest because they receive A1 from EU members, A2 from the UK and Switzerland, and B or C from the other regions.</p>
<div class="controls"><span class="legend" id="entlegend"></span></div>
<div class="figwrap"><div class="scroll"><svg id="map3d" class="map" role="img" aria-label="Map of the sampled jurisdictions shaded by the entropy of incoming transfer conditions"></svg></div><aside class="figside" id="map3dside"><b>Hover or click a country</b><p>Shows the entropy and the incoming class distribution it summarises.</p></aside></div>

<h2 id="corridors">Region to region</h2>
<p>A summary derived from the matrix: the share of each class for every origin-region to destination-region corridor. Europe to Latin America is predominantly C (80.8%) while the reverse direction clusters in B (76.9%), an asymmetry worth knowing before you plan a collaboration; Europe to Africa is C for 65.1% of pathways.</p>
<div id="corr" class="corr"></div>

<h2 id="fig4">From the landscape to a decision</h2>
<p>The Toolkit turns this landscape into a decision for your collaboration: classify the data, look up the pathway, reassess derivatives and models, select the agreement modules. <a href="/toolkit/#workflow">See the workflow</a> or <a href="/toolkit/">open the Toolkit</a>.</p>
<h2 id="data">Data, code and citation</h2>
<p>The matrix and the code behind these figures are open: <a href="https://github.com/francopestilli/data-governance-access-matrix">github.com/francopestilli/data-governance-access-matrix</a>. Legal content reflects instruments in force at __LEGAL_DATE__. If you use the data, please cite the study: Botes M, Mendes A, Huffman B, et al. <i>A decision support toolkit for AI-ready neuroscience data governance</i> (2026); full citations are on the <a href="/about/#citation">About</a> page. The regional distributions of governance attributes for each layer will be published with the legal landscape handbook.</p>
<script>window.MATRIX=__DATA__;window.GEO=__GEO__;</script>
'''.replace('__LEGAL_DATE__', SITE['legal_content_date']).replace('__DATA__', json.dumps(D, ensure_ascii=False)).replace('__GEO__', open(os.path.join(HERE,'geo.json')).read())

CSS = '''
.figwrap{display:grid;grid-template-columns:minmax(0,1fr) 300px;gap:16px;align-items:start;margin:12px 0 8px}
@media (max-width:900px){.figwrap{grid-template-columns:1fr}}
.figside{background:var(--panel);border:1px solid var(--line);border-radius:8px;padding:12px 14px;font-size:.9rem;position:sticky;top:10px}
.figside b{display:block;margin-bottom:4px} .figside p{margin:.3rem 0;max-width:none} .figside .k{font-family:var(--mono);color:var(--accent);font-size:.8rem}
.layers{display:flex;flex-direction:column;gap:8px}
.layer{display:grid;grid-template-columns:54px 1fr;gap:12px;align-items:center;background:var(--panel);border:1.5px solid var(--line);border-radius:10px;padding:10px 14px;cursor:pointer;text-align:left;font:inherit;color:var(--fg)}
.layer:hover,.layer.on{border-color:var(--accent);background:var(--tier)}
.layer .n{font-size:1.4rem;font-weight:700;color:var(--accent);font-family:var(--mono)} .layer b{display:block} .layer span{font-size:.85rem;color:var(--muted)}
.controls{display:flex;gap:16px;flex-wrap:wrap;align-items:center;font-size:.9rem;margin:8px 0}
.controls select,.controls input{font:inherit;padding:5px 8px;border:1px solid var(--line);border-radius:6px;background:var(--panel);color:var(--fg)}
.legend{display:inline-flex;gap:10px;flex-wrap:wrap;color:var(--muted)} .legend i{display:inline-block;width:14px;height:12px;border-radius:2px;vertical-align:middle;margin-right:4px}
.scroll{overflow-x:auto}
.bars{display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:4px 16px;font-size:.82rem;margin:8px 0 16px}
.bars div{display:grid;grid-template-columns:120px 1fr;align-items:center;gap:8px} .bars div span{white-space:nowrap;overflow:hidden;text-overflow:ellipsis} .bars div i{display:block;height:12px;border-radius:2px}
.corr{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:10px;margin:8px 0 16px}
.corr div{background:var(--panel);border:1px solid var(--line);border-radius:8px;padding:10px 12px;font-size:.85rem} .corr b{display:block;margin-bottom:6px}
.corr .bar{display:flex;height:16px;border-radius:3px;overflow:hidden;margin:4px 0} .corr .bar i{display:block;height:100%}
svg.map{width:100%;max-width:980px;height:auto;display:block;background:#f4f7f9;border-radius:8px}
svg.map .bg{fill:#d9dee3;stroke:#fff;stroke-width:.5} svg.map .na{fill:#555b63} svg.map .j{stroke:#fff;stroke-width:.6;cursor:pointer} svg.map .j:hover,svg.map .j.pin{stroke:#111;stroke-width:1.6}
svg.map .isl{stroke:#fff;stroke-width:1;cursor:pointer} svg.map .isl:hover,svg.map .isl.pin{stroke:#111;stroke-width:1.6}
.legend .grad{display:inline-block;width:120px;height:12px;vertical-align:middle;border-radius:2px;margin:0 4px}
#net .node{cursor:pointer} #net.focus .node:not(.on){opacity:.25} #net .edge{opacity:.15} #net .edge.on{opacity:.9}
'''

JS = r'''
(function(){
const D=window.MATRIX;if(!D)return;const N=D.names,R=D.region;const CL=['A1','A2','B','C','D','E'];
const COL={A1:'#1b7f4a',A2:'#8fcf8a',B:'#f1c232',C:'#e8842c',D:'#c0392b',E:'#6b7280'};
const LAB={A1:'A1 unified legal space',A2:'A2 convergent architectures',B:'B standard instruments',C:'C operationally conditional',D:'D restricted in practice',E:'E insufficient certainty'};
const cls=(i,j)=>{const c=D.matrix[i][j];return c==='.'?null:CL[+c];};
document.getElementById('classlegend').innerHTML=CL.map(c=>`<span><i style="background:${COL[c]}"></i>${LAB[c]}</span>`).join('');
// ---- Figure 1 layers
const LAY=[['1','Definitions and scope','How neurodata are legally recognised and classified: as health, biometric, genetic or sensitive data, or explicitly as neural data.','Is neurodata a distinct legal object? Which categories capture it? Does protection depend on identifiability?','Informed the Neurodata Governance Decision Tool (Tool 1) and the tier framework.'],
['2','Lawful bases and processing contexts','Which legal justifications permit processing in research, clinical, public-interest and commercial settings; the role of consent and research exemptions.','What is the principal processing pathway? Consent in 42 of 43 African and 24 of 26 Latin American jurisdictions; research provisions in all 24 European jurisdictions.','Informed Tool 1 and the lawful-basis questions of Tool 2 Step 7.'],
['3','Cross-border transfer and access pathways','Adequacy, standard instruments, consent-based transfer, regulator authorisation, localisation and repository-led governance.','Transfer is formally permissible almost everywhere but navigable only through jurisdiction-specific interpretation.','Informed the Transfer and Access Decision Tool (Tool 2) and the compatibility matrix used at Step 6A.'],
['4','Safeguards and oversight','Data-protection authorities, research ethics committees, repository access controls and technical safeguards.','Oversight exists on paper everywhere, but proactive supervisory capacity and resources vary widely.','Informed Tool 2 Step 8 (receiving-environment capacity) and the Enhanced Audit module of Tool 4.'],
['5','Enforcement and remedies','Compliance monitoring, regulatory enforcement, individual complaints and court access.','Remedies are oriented to conventional data-protection violations rather than neurotechnology-specific harms; participant rights are operationally fragile where redress is weak.','Informed Tool 2 and the Redress article of the MDTAA.'],
['6','Contractual governance','Data transfer and use agreements, standard clauses, onward-transfer and AI-related conditions.','Contracts carry the weight of continuity of protection, which burdens institutions with limited legal resources.','Informed the MDTAA Clause Selection Tool (Tool 4) and the Modular Agreement itself.']];
const lw=document.getElementById('layers'),ls=document.getElementById('layerside');
LAY.forEach(([n,t,s,q,tool],i)=>{const b=document.createElement('button');b.className='layer';b.innerHTML=`<span class="n">${n}</span><div><b>${t}</b><span>${s}</span></div>`;b.addEventListener('click',()=>{[...lw.children].forEach(x=>x.classList.remove('on'));b.classList.add('on');ls.innerHTML=`<div class="k">Layer ${n}</div><b>${t}</b><p>${s}</p><p><b style="display:inline">Coding question and finding.</b> ${q}</p><p><b style="display:inline">In the toolkit.</b> ${tool}</p>`;});lw.appendChild(b);});
// ---- Figure 3a matrix
const cv=document.getElementById('matrix'),ctx=cv.getContext('2d');const n=N.length,PAD=0,S=10;cv.width=n*S;cv.height=n*S;
let hl='',pinned=null,pinj=null;
function draw(){ctx.clearRect(0,0,cv.width,cv.height);for(let i=0;i<n;i++)for(let j=0;j<n;j++){const c=cls(i,j);if(!c){ctx.fillStyle='#ffffff';ctx.fillRect(j*S,i*S,S,S);continue;}ctx.fillStyle=COL[c];ctx.globalAlpha=(hl&&R[N[i]]!==hl&&R[N[j]]!==hl)?0.18:1;ctx.fillRect(j*S,i*S,S-1,S-1);}ctx.globalAlpha=1;
 if(pinned!=null){ctx.strokeStyle='#111';ctx.lineWidth=2;ctx.strokeRect(0,pinned*S-1,n*S,S+1);if(pinj!=null){ctx.strokeRect(pinj*S-1,0,S+1,n*S);ctx.lineWidth=3;ctx.strokeRect(pinj*S-1.5,pinned*S-1.5,S+2,S+2);}else{ctx.strokeRect(pinned*S-1,0,S+1,n*S);}}
 // region separators
 ctx.strokeStyle='rgba(0,0,0,.6)';ctx.lineWidth=1.5;[24,67].forEach(k=>{ctx.beginPath();ctx.moveTo(k*S,0);ctx.lineTo(k*S,n*S);ctx.moveTo(0,k*S);ctx.lineTo(n*S,k*S);ctx.stroke();});}
draw();
const side=document.getElementById('matside');
function profile(i){const out={},inn={};for(let j=0;j<n;j++){if(j===i)continue;const a=cls(i,j),b=cls(j,i);if(a)out[a]=(out[a]||0)+1;if(b)inn[b]=(inn[b]||0)+1;}
 const bar=o=>{const t=Object.values(o).reduce((a,b)=>a+b,0);return `<div class="bar" style="display:flex;height:14px;border-radius:3px;overflow:hidden">${CL.filter(c=>o[c]).map(c=>`<i title="${c}: ${o[c]}" style="display:block;width:${100*o[c]/t}%;background:${COL[c]}"></i>`).join('')}</div><div style="font-size:.78rem;color:var(--muted)">${CL.filter(c=>o[c]).map(c=>c+' '+o[c]).join(' · ')}</div>`;};
 return `<div class="k">${R[N[i]]}</div><b>${N[i]}</b><p>Outgoing (as exporter)</p>${bar(out)}<p>Incoming (as destination)</p>${bar(inn)}<p>Modal class for imports from the European reference set: <b style="display:inline">${D.importEU[N[i]]}</b><br>Entropy of incoming conditions: <b style="display:inline">${D.entropy[N[i]].toFixed(2)} bits</b></p>`;}
const DESC0={A1:'Same legal space: no transfer mechanism required.',A2:'Adequacy-type recognition: record the decision relied on.',B:'Standard transfer instrument under origin law.',C:'Standard instrument plus supplementary safeguards and a transfer-risk assessment.',D:'Restricted in practice: default to redesign (remote or federated access).',E:'Insufficient legal certainty: default to do not proceed unless counsel documents a mechanism.'};
function mini(i){const out={},inn={};for(let j=0;j<n;j++){if(j===i)continue;const a=cls(i,j),b=cls(j,i);if(a)out[a]=(out[a]||0)+1;if(b)inn[b]=(inn[b]||0)+1;}const f=o=>CL.filter(c=>o[c]).map(c=>`<span style="color:${COL[c]};font-weight:600">${c}</span> ${o[c]}`).join(' · ');return `<p style="font-size:.8rem;color:var(--muted);margin:.1rem 0">exports ${f(out)}<br>imports ${f(inn)}<br>from Europe: ${D.importEU[N[i]]} · entropy ${D.entropy[N[i]].toFixed(2)}</p>`;}
function pair(i,j){const c=cls(i,j),b=cls(j,i);return `<div class="k">pathway</div><b>${N[i]} → ${N[j]}</b><p style="margin:.2rem 0 .6rem"><b style="display:inline;color:${COL[c]}">Class ${c}</b> · ${LAB[c].replace(/^\w+\s/,'')}<br>${DESC0[c]}</p><p style="margin:.2rem 0 .8rem;font-size:.9rem"><b style="display:inline">Reverse</b> ${N[j]} → ${N[i]}: <b style="display:inline;color:${COL[b]}">Class ${b}</b>${b===c?'':' (not symmetric)'}</p><div class="k">${R[N[i]]}</div><b>${N[i]}</b>${mini(i)}<div class="k">${R[N[j]]}</div><b>${N[j]}</b>${mini(j)}`;}
cv.addEventListener('mousemove',e=>{if(pinned!=null)return;const r=cv.getBoundingClientRect();const j=Math.floor((e.clientX-r.left)/r.width*n),i=Math.floor((e.clientY-r.top)/r.height*n);if(i<0||j<0||i>=n||j>=n)return;const c=cls(i,j);side.innerHTML=`<div class="k">${c?LAB[c]:'self'}</div><b>${N[i]} → ${N[j]}</b><p>${c?('Class '+c+'. '+({A1:'Same legal space: no transfer mechanism required.',A2:'Adequacy-type recognition: record the decision relied on.',B:'Standard transfer instrument under origin law.',C:'Standard instrument plus supplementary safeguards and a transfer-risk assessment.',D:'Restricted in practice: default to redesign (remote or federated access).',E:'Insufficient legal certainty: default to do not proceed unless counsel documents a mechanism.'})[c]):'Diagonal (same jurisdiction) is not assessed.'}</p>`;});
cv.addEventListener('click',e=>{const r=cv.getBoundingClientRect();const j=Math.floor((e.clientX-r.left)/r.width*n),i=Math.floor((e.clientY-r.top)/r.height*n);if(i<0||j<0||i>=n||j>=n)return;if(pinned===i&&pinj===j){pinned=null;pinj=null;draw();return;}if(i===j){pinned=i;pinj=null;draw();side.innerHTML=profile(i)+'<p style="font-size:.78rem;color:var(--muted)">Click again to unpin.</p>';return;}pinned=i;pinj=j;draw();side.innerHTML=pair(i,j)+'<p style="font-size:.78rem;color:var(--muted)">Click the cell again to unpin; click the diagonal for a single country.</p>';});
document.getElementById('regsel').addEventListener('change',e=>{hl=e.target.value;draw();});
document.getElementById('jsearch').addEventListener('input',e=>{const q=e.target.value.trim().toLowerCase();if(!q)return;const i=N.findIndex(x=>x.toLowerCase().startsWith(q));if(i>=0){pinned=i;pinj=null;draw();side.innerHTML=profile(i);}});
// ---- Figure 3b network
const svg=document.getElementById('net');const NS='http://www.w3.org/2000/svg';const el=(t,a)=>{const e=document.createElementNS(NS,t);for(const k in a)e.setAttribute(k,a[k]);return e;};
const centers={'Europe':[250,300],'Africa':[640,220],'Latin America & Caribbean':[620,470]};const radius={'Europe':150,'Africa':170,'Latin America & Caribbean':120};
const groups={};N.forEach(x=>{(groups[R[x]]=groups[R[x]]||[]).push(x);});const pos={};
for(const g in groups){const arr=groups[g];arr.forEach((x,k)=>{const a=2*Math.PI*k/arr.length;pos[x]=[centers[g][0]+radius[g]*Math.cos(a),centers[g][1]+radius[g]*Math.sin(a)];});}
const edgesG=el('g',{});svg.appendChild(edgesG);
for(let i=0;i<n;i++)for(let j=0;j<n;j++){if(i===j)continue;const c=cls(i,j);if(c&&['A1','A2','B'].includes(c)){const [x1,y1]=pos[N[i]],[x2,y2]=pos[N[j]];edgesG.appendChild(el('line',{x1,y1,x2,y2,stroke:COL[c],'stroke-width':c==='B'?0.5:1.2,class:'edge','data-a':N[i],'data-b':N[j]}));}}
for(const g in groups){const [cx,cy]=centers[g];const t=el('text',{x:cx,y:cy-radius[g]-14,'text-anchor':'middle','font-size':'13','font-weight':'600',fill:'var(--fg)'});t.textContent=g;svg.appendChild(t);}
const maxS=Math.max(...N.map(x=>D.outStrength[x]+D.inStrength[x]));
N.forEach(x=>{const [cx,cy]=pos[x];const s=D.outStrength[x]+D.inStrength[x];const r=3+9*Math.sqrt(s/maxS);const g=el('g',{class:'node','data-id':x});g.appendChild(el('circle',{cx,cy,r,fill:{'Europe':'#005981','Africa':'#e57536','Latin America & Caribbean':'#a9262c'}[R[x]],stroke:'#fff','stroke-width':1}));const t=el('title',{});t.textContent=x+' · strength '+s;g.appendChild(t);svg.appendChild(g);
 g.addEventListener('click',()=>{svg.classList.add('focus');const nb=new Set([x]);svg.querySelectorAll('.edge').forEach(e=>{const on=e.dataset.a===x||e.dataset.b===x;e.classList.toggle('on',on);if(on){nb.add(e.dataset.a);nb.add(e.dataset.b);}});svg.querySelectorAll('.node').forEach(nd=>nd.classList.toggle('on',nb.has(nd.dataset.id)));
  let o={};for(let j=0;j<n;j++){const c=cls(N.indexOf(x),j);if(c&&['A1','A2','B'].includes(c))o[c]=(o[c]||0)+1;}
  document.getElementById('netside').innerHTML=`<div class="k">${R[x]}</div><b>${x}</b><p>Enabled outgoing pathways: ${CL.slice(0,3).map(c=>c+' '+(o[c]||0)).join(' · ')}</p><p>Weighted out-strength ${D.outStrength[x]}, in-strength ${D.inStrength[x]}.</p><p style="font-size:.78rem;color:var(--muted)">Click the background to clear.</p>`;});});
svg.addEventListener('click',e=>{if(e.target===svg){svg.classList.remove('focus');svg.querySelectorAll('.edge').forEach(x=>x.classList.remove('on'));}});
// ---- Figure 3c/3d maps
const G=window.GEO;
function viridis(t){const st=[[68,1,84],[59,82,139],[33,145,140],[94,201,98],[253,231,37]];t=Math.max(0,Math.min(1,t))*(st.length-1);const i=Math.min(Math.floor(t),st.length-2),f=t-i;const c=st[i].map((v,k)=>Math.round(v+(st[i+1][k]-v)*f));return `rgb(${c[0]},${c[1]},${c[2]})`;}
function buildMap(id){const sv=document.getElementById(id);sv.setAttribute('viewBox',`0 0 ${G.w} ${G.h}`);const bg=el('g',{}),fg=el('g',{}),isl=el('g',{});sv.appendChild(bg);sv.appendChild(fg);sv.appendChild(isl);const shapes={};
 G.f.forEach(f=>{if(!f.k){if(f.d)bg.appendChild(el('path',{d:f.d,class:f.na?'bg na':'bg'}));return;}
  let e;if(f.a<30){e=el('circle',{cx:f.c[0],cy:f.c[1],r:4.5,class:'isl','data-id':f.n});if(f.d)bg.appendChild(el('path',{d:f.d,class:'bg'}));}else{e=el('path',{d:f.d,class:'j','data-id':f.n});}
  const t=el('title',{});e.appendChild(t);shapes[f.n]={e,t};(f.a<30?isl:fg).appendChild(e);});
 return {sv,shapes};}
function wireMap(m,sideId,colorFn,hoverFn,clickFn){const side=document.getElementById(sideId);let pin=null;
 const paint=()=>{for(const x in m.shapes){const {e,t}=m.shapes[x];const c=colorFn(x);e.setAttribute('fill',c.fill);t.textContent=c.title;}};
 for(const x in m.shapes){const e=m.shapes[x].e;e.addEventListener('mouseenter',()=>{if(pin)return;side.innerHTML=hoverFn(x);});e.addEventListener('click',()=>{if(pin===x){pin=null;e.classList.remove('pin');side.innerHTML=hoverFn(x);return;}if(pin)m.shapes[pin].e.classList.remove('pin');pin=x;e.classList.add('pin');side.innerHTML=clickFn(x)+'<p style="font-size:.78rem;color:var(--muted)">Click again to unpin.</p>';});}
 return paint;}
const DESC={A1:'Same legal space: no transfer mechanism required.',A2:'Adequacy-type recognition: record the decision relied on.',B:'Standard transfer instrument under origin law.',C:'Standard instrument plus supplementary safeguards and a transfer-risk assessment.',D:'Restricted in practice: default to redesign (remote or federated access).',E:'Insufficient legal certainty: default to do not proceed unless counsel documents a mechanism.'};
// 3c
const osel=document.getElementById('orig');N.forEach(x=>{const o=document.createElement('option');o.value=x;o.textContent=x;osel.appendChild(o);});
const dsel=document.getElementById('dir');document.getElementById('maplegend').innerHTML=CL.map(c=>`<span><i style="background:${COL[c]}"></i>${c}</span>`).join('');
const m3c=buildMap('map3c');
function val3c(x){const o=osel.value;if(o==='EU')return {c:D.importEU[x],lab:'modal class of imports from the European reference set'};
 const i=N.indexOf(o),j=N.indexOf(x);if(i===j)return {c:null,lab:'origin'};const c=dsel.value==='out'?cls(i,j):cls(j,i);return {c,lab:dsel.value==='out'?`class of the pathway ${o} → ${x}`:`class of the pathway ${x} → ${o}`};}
const paint3c=wireMap(m3c,'map3cside',x=>{const v=val3c(x);return {fill:v.c?COL[v.c]:'#111827',title:x+(v.c?': '+v.c:' (origin)')};},
 x=>{const v=val3c(x);return `<div class="k">${R[x]}</div><b>${x}</b><p>${v.c?('Class <b style="display:inline">'+v.c+'</b>, '+v.lab+'.</p><p>'+DESC[v.c]):'Selected origin.'}</p>`;},
 x=>profile(N.indexOf(x)));
paint3c();osel.addEventListener('change',paint3c);dsel.addEventListener('change',paint3c);
// 3d
const m3d=buildMap('map3d');const EMAX=Math.max(...N.map(x=>D.entropy[x]));
document.getElementById('entlegend').innerHTML=`<span>0 bits <i class="grad" style="background:linear-gradient(90deg,${[0,.25,.5,.75,1].map(viridis).join(',')})"></i> ${EMAX.toFixed(2)} bits</span>`;
const paint3d=wireMap(m3d,'map3dside',x=>({fill:viridis(D.entropy[x]/EMAX),title:x+': '+D.entropy[x].toFixed(2)+' bits'}),
 x=>{const inn={};for(let j=0;j<n;j++){const c=cls(j,N.indexOf(x));if(c)inn[c]=(inn[c]||0)+1;}return `<div class="k">${R[x]}</div><b>${x}</b><p>Entropy of incoming conditions: <b style="display:inline">${D.entropy[x].toFixed(2)} bits</b></p><p>Incoming classes: ${CL.filter(c=>inn[c]).map(c=>c+' '+inn[c]).join(' · ')}</p>`;},
 x=>profile(N.indexOf(x)));
paint3d();
// ---- corridors
const cb=document.getElementById('corr');Object.entries(D.corridor).forEach(([k,o])=>{const t=Object.values(o).reduce((a,b)=>a+b,0);const d=document.createElement('div');d.innerHTML=`<b>${k.replace('→',' → ')}</b><div class="bar">${CL.filter(c=>o[c]).map(c=>`<i style="width:${100*o[c]/t}%;background:${COL[c]}" title="${c}: ${o[c]} (${(100*o[c]/t).toFixed(1)}%)"></i>`).join('')}</div>${CL.filter(c=>o[c]).map(c=>`${c} ${(100*o[c]/t).toFixed(1)}%`).join(' · ')}`;cb.appendChild(d);});
})();
'''

if __name__ == '__main__':
    out = os.path.join(HERE, '..', '..', 'content', 'findings.html')
    open(out, 'w').write('---\ntitle: Legal landscape\ndescription: "The legal landscape behind the Neurodata Governance Toolkit: the six-layer framework, the 93×93 directional compatibility matrix, the network of enabled pathways, and maps of import conditions and their heterogeneity, interactive."\nurl: /toolkit/legal-landscape/\ngenerated: edit src/landscape/findings.py, not this file\n---\n<style>' + CSS + '</style>\n<main class="wrap">\n' + BODY + '\n</main>\n<script>' + JS + '</script>\n')
    print('wrote', os.path.normpath(out))
