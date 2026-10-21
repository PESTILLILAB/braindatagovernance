# Interactive workflow: data + renderer for the Workflow tab.
import json

PANELS = [
 {"id":"t1","title":"1  Classify the object","sub":"Neurodata Governance Decision Tool","rec":"Schedule B",
  "out":{"id":"t1out","label":"Tier (highest governs)","lines":["Tier 5  model-associated","Tier 4  revealing derivative","Tier 3  directly identifiable","Tier 2  linkable by recipient","Tier 1b  participant-level, non-linkable","Tier 1  aggregate"]}},
 {"id":"t2","title":"2  Assess the pathway","sub":"Neurodata Transfer and Access Decision Tool","rec":"Schedule C",
  "out":{"id":"t2out","label":"Outcome","lines":["1  Proceed","2  Proceed after safeguards","3  Redesign the pathway","4  Do not proceed"]}},
 {"id":"t3","title":"3  Reassess the transformation","sub":"Derivative and Embedding Governance Decision Tool","rec":"Schedule D",
  "out":{"id":"t3out","label":"Outcome","lines":["1  Retain tier","2  Refer Tier 4","3  Confirm Tier 5","4  Specialist review","5  Do not proceed"]}},
 {"id":"t4","title":"4  Select contract modules","sub":"MDTAA Clause Selection Tool","rec":"Schedule A E.5 · module list",
  "out":{"id":"t4out","label":"Implementation","lines":["Compile and check consistency","Legal, ethics, repository review","Execute · implement · monitor"]}},
]

# nodes: id, panel, step label, short title, explanation (plain), yes/no effect, record
NODES = [
 # Tool 1
 {"id":"t1s0b","p":"t1","step":"0B","title":"Participant status","text":"Asks whether the data come from minors, adults who could not consent, deceased persons, Indigenous or community-governed groups, or people in a dependent relationship with the collecting institution (patients, employees, students).","effect":"Yes: the minimum tier available at the end is raised by one level and the community-governance module is flagged. No: continue. Unknown: treated as Yes until resolved.","why":"Ethics committees treat participant status as decisive; the tier alone does not capture it."},
 {"id":"t1s2a","p":"t1","step":"2A","title":"Is the object itself a model or persistent artefact?","text":"Checks whether the thing being classified is a trained model, model gradient, embedding store, synthetic-data generator or similar, rather than a dataset.","effect":"Yes: candidate Tier 5 and Tool 3 becomes mandatory for this object. No: continue to the dataset questions. A model trained on a dataset is a separate object with its own assessment.","why":"Models carry information from their training data and must be assessed on their own."},
 {"id":"t1s4","p":"t1","step":"4","title":"Derivative with excess inferential capacity?","text":"For derived objects only: can it support inferences outside the authorised purpose, identify a participant on its own (for example a connectome fingerprint), or reconstruct stimuli, speech or imagery? Standard summary derivatives that reveal no more than the source keep the source tier.","effect":"Yes: Tier 4 (controlled access, permitted-inference restrictions, Tool 3 before sharing). No: continue.","why":"Transformation can increase what data reveal even when it removes identifiers."},
 {"id":"t1s5","p":"t1","step":"5","title":"Direct identifiers or identifying anatomy?","text":"Names, identifying DICOM headers, non-defaced faces, voice or video, device identifiers and timestamps that allow tracing.","effect":"Yes: Tier 3 (secure environment, encryption, formal access approval, no downloads without review). No: continue to the linkage question.","why":"Directly identifiable neurodata are health data of the highest sensitivity in every sampled regime."},
 {"id":"t1s6","p":"t1","step":"6","title":"Linkage key available to the recipient?","text":"Can the intended recipient re-link records to individuals through a code, repository record or institutional key? The answer can differ by recipient: the lab that keeps the key answers Yes for itself and No for an external recipient that cannot obtain it.","effect":"Yes: Tier 2 (controlled access, data-use agreement, key kept separate). No: continue to the aggregate and disclosure-risk questions.","why":"Whether data are personal is assessed from the recipient's perspective (CJEU C-413/23 P; LGPD art. 12; POPIA)."},
 {"id":"t1s8","p":"t1","step":"8","title":"Disclosure risk for the intended recipient?","text":"Could an individual or small group still reasonably be identified by the intended recipient (for a public release, by anyone), through rare conditions, small cohorts, unique metadata, residual facial features or linkage with available data?","effect":"Yes: Tier 2 minimum; aggregate or suppress and reassess. No and aggregate-only: Tier 1. No and participant-level: Tier 1b, with the de-identification method, licence and re-identification prohibition recorded.","why":"This is the test that lets open-science releases be classified instead of stalling."},
 # Tool 2
 {"id":"t2s3","p":"t2","step":"3","title":"Who receives the data?","text":"Named institutions and providers; a public or unrestricted release (open repository, open licence, public model weights); or recipients that cannot be identified.","effect":"Named: continue. Public release: allowed only on a confirmed Tier 1 or 1b finding made for the public, or a documented model-anonymity assessment from Tool 3 Step 7; otherwise redesign to controlled or gated access. Unknown: stop until identified.","why":"Open releases need a gate, not a dead end; unknown recipients cannot be bound by any safeguard."},
 {"id":"t2s6a","p":"t2","step":"6A","title":"Compatibility class of the pathway","text":"Looks up the origin→destination pair (and hosting and remote-access jurisdictions) in the 93×93 compatibility matrix.","effect":"A1: no transfer mechanism needed. A2: adequacy-type recognition, check its scope. B: standard instrument under origin law. C: standard instrument plus supplementary safeguards and a transfer-risk assessment. D: redesign toward remote or federated access unless counsel documents a mechanism. E: do not proceed unless counsel documents a mechanism.","why":"This connects the comparative legal analysis to the decision."},
 {"id":"t2s6b","p":"t2","step":"6B","title":"Origin- and destination-side restrictions","text":"Checks the regime table for a statutory export prohibition, a localisation or serving-copy duty, regulator authorisation or registration, sanctions or export-control screening, a research export permit, and destination-side import conditions.","effect":"A prohibition forces redesign (analysis in place, results only) or stop. Any other restriction becomes a prerequisite that must be documented before Outcome 1.","why":"These rules (LGPD art. 13, Kenya reg. 26, POPIA s. 57, 28 CFR 202) are what most often stop a transfer in practice."},
 {"id":"t2s7","p":"t2","step":"7","title":"Exporter and importer legal checks","text":"7(i): the exporter's lawful basis, the transfer mechanism indicated at 6A, the required risk or impact assessment, the authorisations from 6B, and the exporter's authority under consent and ethics approvals. 7(ii): the importer's own lawful basis for sensitive data, registrations, hosting certifications and approvals. 7A: any statutory data permit or research permit.","effect":"All documented: continue. Anything missing: obtain the review; do not begin transfer; if no lawful pathway exists, Outcome 4.","why":"Transfer law binds the exporter; processing law binds the importer; both have to be satisfied."},
 {"id":"t2s9","p":"t2","step":"9 / 10","title":"Linkage or AI use planned?","text":"Will the recipient link the data with genomic, clinical, wearable or other datasets? Will the data or derivatives be used to train, fine-tune, validate or deploy a model?","effect":"Linkage: the linked dataset goes back to Tool 1 for re-tiering before linkage. AI use: Tool 3 must be completed before this pass can finish.","why":"Both change what the data can reveal, so the classification has to be redone."},
 {"id":"t2s11","p":"t2","step":"11–13","title":"Purpose, onward sharing, safeguards","text":"Is the use materially different from the approved purpose? May the recipient pass data on? Are all required safeguards implemented and verified?","effect":"A different purpose needs approvals (ethics amendment, re-consent or compatibility assessment). Onward sharing is permitted only within recorded conditions. Safeguards not yet implemented give Outcome 2; safeguards that cannot be implemented give Outcome 3 or 4.","why":"Purpose limitation and onward-transfer control are the obligations most contracts under-specify."},
 # Tool 3
 {"id":"t3s4","p":"t3","step":"4","title":"Can the artefact identify or re-link a participant?","text":"An embedding unique to a participant, a synthetic dataset that reproduces training records, or a model that memorises participant-level signals.","effect":"Yes: flagged for identification safeguards and Tier 3/2 treatment. No: continue; absence of identification does not establish absence of inference or persistence.","why":"Derived objects can carry identity even when they look nothing like the source."},
 {"id":"t3s5","p":"t3","step":"5 / 6","title":"Inference capability and computational persistence","text":"Step 5: can the artefact reveal, predict or profile cognitive, emotional or neurological states? Step 6: does neural information persist in a model, embedding store or generator in a way that supports continuing inference or extraction?","effect":"Step 5 Yes: candidate Tier 4. Step 6 Yes: candidate Tier 5. Model incorporation alone is not enough; the question is whether exposure persists.","why":"Tiers 4 and 5 are defined by what the artefact can do, not by its technical form."},
 {"id":"t3s7","p":"t3","step":"7","title":"Leakage and anonymity assessment","text":"Has the artefact been tested for memorisation, extraction, inversion and membership inference under the intended release conditions? For public release: likelihood of direct extraction, likelihood through queries, and documentation (the EDPB Opinion 28/2024 test).","effect":"Material exposure found: public release not supported. No material exposure under tested conditions: the public-release branch at Tool 2 Step 3 may be used. Not tested: specialist review.","why":"This is the only evidence that can justify releasing weights or synthetic data publicly."},
 {"id":"t3s8","p":"t3","step":"8–9A","title":"Provenance, deployment, release conditions","text":"Is the transformation history documented (source data, preprocessing, training, versions, vendors)? Do the proposed access or deployment conditions change exposure (downloads, APIs, fine-tuning, commercial deployment)? Have outputs been checked against release conditions?","effect":"Gaps in provenance block sharing of the affected artefact; changed deployment conditions trigger a Tool 2 pass for the artefact; release conditions must be approved before anything leaves.","why":"Permission to analyse is not permission to export; both must be recorded."},
 {"id":"t3s10","p":"t3","step":"10–11","title":"Lifecycle controls and manageability","text":"Are retention, deletion, decommissioning and (where feasible) unlearning procedures documented? Can the remaining exposure be managed with proportionate safeguards?","effect":"Yes: proceed to an outcome. Partly: record alternatives such as version retirement or output restrictions. No: Outcome 5, do not proceed in the current form.","why":"Deleting source data does not remove its influence from a model."},
 # Tool 4
 {"id":"t4s2","p":"t4","step":"2","title":"Cross-border and transfer-instrument module","text":"Activated for any international transfer, storage or remote access. Records the compatibility class and restrictions from Tool 2 and activates the module for the origin regime: EU SCCs, UK IDTA or Addendum, Swiss clauses, ANPD standard clauses, AAIP clauses, POPIA s. 72 agreement, Kenya reg. 41 instrument, NDPC instrument, NCSA authorisation, Québec s. 17 agreement, HIPAA DUA terms, or the generic module.","effect":"The mandatory instrument is attached unmodified and takes precedence to the extent its own law requires; the rest of the MDTAA supplements it.","why":"A single EU-style contract cannot serve a Brazilian, South African or Nigerian exporter."},
 {"id":"t4s3","p":"t4","step":"3–7","title":"Safeguards, enhanced protection, derivatives, AI, controlled access","text":"Supplementary safeguards for Class C pathways or Outcome 2; enhanced protection for Tiers 3–5; derivative-neurodata terms; AI and model governance; controlled-access, repository and statutory-authorisation conditions.","effect":"Each module adds obligations, responsible parties and verification requirements drawn from Tools 1–3.","why":"The contract should carry exactly the safeguards the assessments identified, no more and no less."},
 {"id":"t4s8","p":"t4","step":"8–13","title":"Onward transfer, commercial use, linkage, permitted inference","text":"Whether sub-processors and onward recipients are allowed; commercial versus research-only use; which datasets may be linked; which inferences are authorised and which are prohibited.","effect":"Onward permissions must be consistent with upstream conditions; commercial involvement is not permission for commercial use; prohibited inferences are listed explicitly.","why":"These are the uses that participants and communities most often object to."},
 {"id":"t4s14","p":"t4","step":"14–20","title":"Audit, deletion, persistent artefacts, community, coordination, law and forum","text":"Audit and monitoring; return, deletion and certification; retention and unlearning for models; community and Indigenous governance; benefit sharing; project-specific requirements; coordination with other instruments; governing law and forum chosen from a menu.","effect":"Completes the agreement and sets the reassessment triggers; governing law is selected per transfer rather than defaulting to an EU Member State.","why":"Agreements must remain enforceable in both parties' jurisdictions."},
]
OUTS = {
 "t1out":{"title":"Tier assigned","text":"The highest applicable tier governs, recorded as provisional or confirmed. The tier sets the minimum safeguards and is carried into Tool 2.","effect":"Feeds Tool 2; a linked dataset or a changed artefact returns here for re-tiering.","why":""},
 "t2out":{"title":"Pathway outcome","text":"1 Proceed subject to approvals; 2 Proceed after specified safeguards are implemented and verified; 3 Redesign the pathway (remote, federated, aggregation, another destination); 4 Do not proceed and obtain specialist review.","effect":"Outcome 1 cannot be selected while any 6B prerequisite, 7 item or linkage uncertainty is open. Conditions feed Tool 4.","why":""},
 "t3out":{"title":"Transformation outcome","text":"1 Retain the existing tier; 2 Refer for Tier 4; 3 Confirm Tier 5; 4 Specialist review required; 5 Do not proceed in the current form.","effect":"A changed tier returns the object to Tool 1; an affected pathway repeats Tool 2; findings feed Tool 4.","why":""},
 "t4out":{"title":"Implementation","text":"Compile the selected modules, check consistency, obtain legal, ethics and repository review, execute, implement and monitor.","effect":"A material change in object, purpose, recipient, jurisdiction, access, linkage, AI use or deployment reopens the affected tool.","why":""},
}
EDGES = [
 # sequence within tools
 ("t1s0b","t1s2a","seq"),("t1s2a","t1s4","seq"),("t1s4","t1s5","seq"),("t1s5","t1s6","seq"),("t1s6","t1s8","seq"),("t1s8","t1out","seq"),
 ("t2s3","t2s6a","seq"),("t2s6a","t2s6b","seq"),("t2s6b","t2s7","seq"),("t2s7","t2s9","seq"),("t2s9","t2s11","seq"),("t2s11","t2out","seq"),
 ("t3s4","t3s5","seq"),("t3s5","t3s7","seq"),("t3s7","t3s8","seq"),("t3s8","t3s10","seq"),("t3s10","t3out","seq"),
 ("t4s2","t4s3","seq"),("t4s3","t4s8","seq"),("t4s8","t4s14","seq"),("t4s14","t4out","seq"),
 # forward hand-offs
 ("t1out","t2s3","fwd","tier"),("t1s2a","t3s4","fwd","model object"),("t2s9","t3s4","fwd","AI use"),("t3s7","t2s3","fwd","release gate"),
 ("t2out","t4s2","fwd","conditions"),("t3out","t4s3","fwd","findings"),
 # loops
 ("t2s9","t1s0b","loop","linkage → re-tier"),("t3out","t1s0b","loop","tier changed"),("t3s8","t2s3","loop","pathway affected"),("t4out","t1s0b","loop","material change"),
]

def html():
    data = {"panels":PANELS,"nodes":NODES,"outs":OUTS,"edges":EDGES}
    return f'''
<p class="lead">Click any step to highlight what feeds it and what it feeds, and to read what the step decides. Click the background or “Reset” to clear. Hover shows a short summary.</p>
<div class="iwf-wrap">
 <figure class="iwf-fig"><div class="scroll"><svg id="iwf" role="img" aria-label="Interactive workflow of the four tools"></svg></div>
 <div class="iwf-legend"><span><i class="sw"></i>decision step</span><span><i class="sw tier"></i>output</span><span><i class="sw fwd"></i>hand-off to the next tool</span><span><i class="sw loop"></i>loop back</span><button class="sub" id="iwf-reset">Reset</button></div></figure>
 <aside class="iwf-side" id="iwf-side"><div class="iwf-empty"><b>Select a step</b><p>The explanation appears here: what the step asks, what each answer does, why it is in the workflow, and which steps are connected to it.</p></div></aside>
</div>
<div id="iwf-tip" class="iwf-tip" hidden></div>
<script>window.IWF={json.dumps(data, ensure_ascii=False)};</script>
'''

CSS = '''
.iwf-wrap{display:grid;grid-template-columns:minmax(0,1fr) 340px;gap:16px;align-items:start}
@media (max-width:980px){.iwf-wrap{grid-template-columns:1fr}}
.iwf-fig{margin:0} #iwf{min-width:760px;width:100%;height:auto;display:block;cursor:default}
.iwf-legend{display:flex;flex-wrap:wrap;gap:12px 18px;align-items:center;font-size:.85rem;color:var(--muted);margin-top:8px}
.iwf-legend span{display:inline-flex;align-items:center;gap:6px} .sw.fwd{border:0;height:2px;background:var(--accent);width:24px} .sw.loop{border:0;height:2px;background:var(--loop);width:24px}
.iwf-side{background:var(--panel);border:1px solid var(--line);border-radius:8px;padding:14px 16px;position:sticky;top:12px;font-size:.92rem;min-height:200px}
.iwf-side h3{margin:0 0 2px;font-size:1.05rem} .iwf-side .k{font-family:var(--mono);color:var(--accent);font-size:.8rem} .iwf-side p{margin:.5rem 0;max-width:none} .iwf-side h4{margin:.8rem 0 .2rem;font-size:.78rem;letter-spacing:.06em;text-transform:uppercase;color:var(--muted)}
.iwf-side .links a{display:inline-block;margin:2px 6px 2px 0;font-size:.85rem;cursor:pointer;color:var(--accent);text-decoration:underline dotted}
.iwf-empty{color:var(--muted)} .iwf-empty b{color:var(--fg)}
.iwf-tip{position:fixed;z-index:50;max-width:280px;background:var(--fg);color:var(--bg);padding:8px 10px;border-radius:6px;font-size:.82rem;pointer-events:none;box-shadow:0 4px 14px rgba(0,0,0,.25)}
#iwf .node{cursor:pointer} #iwf .node rect{transition:opacity .15s} #iwf.focus .node:not(.on) rect,#iwf.focus .node:not(.on) text{opacity:.22} #iwf.focus .edge:not(.on){opacity:.12}
#iwf .node.sel rect{stroke-width:3} #iwf .edge.on{stroke-width:3}
'''

JS = r'''
(function(){
const D=window.IWF;const NS='http://www.w3.org/2000/svg';
const el=(n,a,t)=>{const e=document.createElementNS(NS,n);for(const k in a)e.setAttribute(k,a[k]);if(t!=null)e.textContent=t;return e;};
const wrap=(s,m)=>{const w=s.split(' '),L=[],c=[];for(const x of w){c.push(x);if(c.join(' ').length>m){c.pop();L.push(c.join(' '));c.length=0;c.push(x);}}if(c.length)L.push(c.join(' '));return L;};
const svg=document.getElementById('iwf');if(!svg)return;
const PX0=20,PW=300,PG=26,PY=20,NH=46,GAP=10,HEAD=58;
const byP={};D.nodes.forEach(n=>{(byP[n.p]=byP[n.p]||[]).push(n)});
const maxGates=Math.max(...Object.values(byP).map(a=>a.length));
const outH=Math.max(...D.panels.map(p=>p.out.lines.length))*18+30;
const PH=HEAD+16+maxGates*(NH+GAP)+28+outH+36;
const W=PX0*2+4*PW+3*PG,H=PY+PH+150;
svg.setAttribute('viewBox',`0 0 ${W} ${H}`);
const defs=el('defs');[['fwd','var(--accent)'],['loop','var(--loop)'],['seq','var(--line)']].forEach(([k,c])=>{const m=el('marker',{id:'iwf-m-'+k,viewBox:'0 0 10 10',refX:'9',refY:'5',markerWidth:'6',markerHeight:'6',orient:'auto-start-reverse'});m.appendChild(el('path',{d:'M0,0 L10,5 L0,10 z',fill:c}));defs.appendChild(m);});svg.appendChild(defs);
const pos={},nodeEl={},edgeEls=[];
D.panels.forEach((p,i)=>{const x=PX0+i*(PW+PG);
 svg.appendChild(el('rect',{x,y:PY,width:PW,height:PH,rx:10,fill:'var(--panel)',stroke:'var(--accent)','stroke-width':'1.4'}));
 svg.appendChild(el('path',{d:`M${x},${PY+10} a10,10 0 0 1 10,-10 h${PW-20} a10,10 0 0 1 10,10 v${HEAD-10} h-${PW} z`,fill:'var(--tier)'}));
 svg.appendChild(el('text',{x:x+14,y:PY+24,'font-size':'15','font-weight':'700',fill:'var(--fg)'},p.title));
 svg.appendChild(el('text',{x:x+14,y:PY+43,'font-size':'11',fill:'var(--muted)'},p.sub));
 let y=PY+HEAD+16;
 byP[p.id].forEach(n=>{const g=el('g',{class:'node','data-id':n.id});g.appendChild(el('rect',{x:x+12,y,width:PW-24,height:NH,rx:NH/2,fill:'var(--panel)',stroke:'var(--line)','stroke-width':'1.4'}));
   g.appendChild(el('text',{x:x+28,y:y+NH/2+5,'font-size':'12','font-weight':'700',fill:'var(--accent)','font-family':'var(--mono)'},n.step));
   const tx=x+40+Math.max(3,n.step.length)*8;const L=wrap(n.title,28).slice(0,2);const y0=L.length>1?y+NH/2-2:y+NH/2+4;L.forEach((s,k)=>g.appendChild(el('text',{x:tx,y:y0+k*14,'font-size':'11.5',fill:'var(--fg)'},s)));
   svg.appendChild(g);pos[n.id]={x:x+12,y,w:PW-24,h:NH};nodeEl[n.id]=g;y+=NH+GAP;});
 const oy=PY+HEAD+16+maxGates*(NH+GAP)+8;const o=p.out;const g=el('g',{class:'node','data-id':o.id});
 g.appendChild(el('rect',{x:x+12,y:oy,width:PW-24,height:outH,rx:6,fill:'var(--tier)',stroke:'var(--accent)','stroke-width':'1.4'}));
 g.appendChild(el('text',{x:x+22,y:oy+15,'font-size':'10','font-weight':'700',fill:'var(--muted)','letter-spacing':'1'},o.label.toUpperCase()));
 o.lines.forEach((s,k)=>g.appendChild(el('text',{x:x+22,y:oy+32+k*18,'font-size':'11.5','font-weight':'600',fill:'var(--fg)'},s)));
 svg.appendChild(g);pos[o.id]={x:x+12,y:oy,w:PW-24,h:outH};nodeEl[o.id]=g;
 svg.appendChild(el('text',{x:x+14,y:PY+PH-12,'font-size':'10.5',fill:'var(--muted)'},'Records to: '+p.rec));
});
// edges
const pIdx={t1:0,t2:1,t3:2,t4:3};const pOf=id=>id.slice(0,2);
let loopCh=0,fwdCh=0;
D.edges.forEach(e=>{const [a,b,k,lb]=e;const A=pos[a],B=pos[b];let d,lab;const pa=pIdx[pOf(a)],pb=pIdx[pOf(b)];
 if(k==='seq'){d=`M${A.x+A.w/2},${A.y+A.h} L${B.x+B.w/2},${B.y}`;}
 else if(k==='fwd'){ if(pb===pa+1){const x1=A.x+A.w,x2=B.x,xm=(x1+x2)/2;d=`M${x1},${A.y+A.h/2} L${xm},${A.y+A.h/2} L${xm},${B.y+B.h/2} L${x2},${B.y+B.h/2}`;lab=[xm,Math.min(A.y,B.y)+ -4 + (A.y<B.y?A.h/2:B.h/2)];}
   else if(pb<pa){const x1=A.x,x2=B.x+B.w,xm=(x1+x2)/2;d=`M${x1},${A.y+A.h/2} L${xm},${A.y+A.h/2} L${xm},${B.y+B.h/2} L${x2},${B.y+B.h/2}`;lab=[xm,Math.min(A.y+A.h/2,B.y+B.h/2)-4];}
   else {const yc=PY-6-fwdCh*0;const x1=A.x+A.w/2,x2=B.x+B.w/2;const gx1=A.x+A.w+PG/2,gx2=B.x-PG/2;d=`M${A.x+A.w},${A.y+A.h/2} L${gx1},${A.y+A.h/2} L${gx1},${PY+PH+20+fwdCh*12} L${gx2},${PY+PH+20+fwdCh*12} L${gx2},${B.y+B.h/2} L${B.x},${B.y+B.h/2}`;lab=[(gx1+gx2)/2,PY+PH+16+fwdCh*12];fwdCh++;}}
 else { const y=PY+PH+40+loopCh*22;const xa=A.x+A.w/2,xb=B.x+B.w/2;d=`M${xa},${A.y+A.h} L${xa},${y} L${xb},${y} L${xb},${B.y+B.h+2}`;lab=[(xa+xb)/2,y-5];loopCh++;}
 const col={seq:'var(--line)',fwd:'var(--accent)',loop:'var(--loop)'}[k];
 const path=el('path',{d,fill:'none',stroke:col,'stroke-width':k==='seq'?'1.6':'2','stroke-dasharray':k==='loop'?'7 5':'','marker-end':`url(#iwf-m-${k})`,class:'edge','data-a':a,'data-b':b});
 svg.insertBefore(path,svg.firstChild.nextSibling);edgeEls.push(path);
 if(lb&&lab){const t=el('text',{x:lab[0],y:lab[1],'font-size':'10.5','text-anchor':'middle',fill:col,class:'edge','data-a':a,'data-b':b},lb);svg.appendChild(t);}
});
// interaction
const side=document.getElementById('iwf-side'),tip=document.getElementById('iwf-tip');
const info=id=>D.nodes.find(n=>n.id===id)||Object.assign({id,step:''},D.outs[id]||{});
const title=id=>{const n=info(id);return (n.step?n.step+'  ':'')+n.title;};
function neighbours(id){const set=new Set([id]);const links=[];D.edges.forEach(([a,b,k,lb])=>{if(a===id){set.add(b);links.push({id:b,dir:'→',k,lb});}if(b===id){set.add(a);links.push({id:a,dir:'←',k,lb});}});return {set,links};}
function select(id){const {set,links}=neighbours(id);svg.classList.add('focus');
 Object.entries(nodeEl).forEach(([k,g])=>{g.classList.toggle('on',set.has(k));g.classList.toggle('sel',k===id);});
 svg.querySelectorAll('.edge').forEach(e=>e.classList.toggle('on',e.dataset.a===id||e.dataset.b===id));
 const n=info(id);const lk=links.map(l=>`<a data-go="${l.id}">${l.dir} ${title(l.id)}${l.lb?' <em>('+l.lb+')</em>':''}</a>`).join('');
 side.innerHTML=`<div class="k">${n.step?'Step '+n.step:'Output'}</div><h3>${n.title}</h3><p>${n.text||''}</p>${n.effect?'<h4>What the answers do</h4><p>'+n.effect+'</p>':''}${n.why?'<h4>Why it is here</h4><p>'+n.why+'</p>':''}<h4>Connected steps</h4><div class="links">${lk||'—'}</div>`;
 side.querySelectorAll('a[data-go]').forEach(a=>a.addEventListener('click',()=>select(a.dataset.go)));
 if(window.innerWidth<980)side.scrollIntoView({behavior:'smooth',block:'nearest'});}
function reset(){svg.classList.remove('focus');Object.values(nodeEl).forEach(g=>g.classList.remove('on','sel'));svg.querySelectorAll('.edge').forEach(e=>e.classList.remove('on'));side.innerHTML='<div class="iwf-empty"><b>Select a step</b><p>The explanation appears here: what the step asks, what each answer does, why it is in the workflow, and which steps are connected to it.</p></div>';}
Object.entries(nodeEl).forEach(([id,g])=>{g.addEventListener('click',ev=>{ev.stopPropagation();tip.hidden=true;select(id);});
 g.addEventListener('mousemove',ev=>{const n=info(id);tip.textContent=(n.step?n.step+' · ':'')+n.title+' — '+(n.text||'').slice(0,140)+((n.text||'').length>140?'…':'');tip.hidden=false;tip.style.left=Math.min(ev.clientX+14,window.innerWidth-300)+'px';tip.style.top=(ev.clientY+14)+'px';});
 g.addEventListener('mouseleave',()=>tip.hidden=true);});
svg.addEventListener('click',reset);document.getElementById('iwf-reset').addEventListener('click',reset);
})();
'''
