import sys,re,glob,os,json,html
sys.path.insert(0,'.')
from deck_all import SLIDES
W='/mnt/user-data/outputs/wiki/'
pages={os.path.basename(p)[:-3]:open(p,encoding='utf-8').read() for p in glob.glob(W+'*.md')}
def vocab(pg):
    t=pages.get(pg,''); m=re.search(r'## 重要單字\n(.*?)(?:\n## |\Z)',t,re.S)
    rows=[]
    if m:
        for l in m.group(1).splitlines():
            c=[x.strip() for x in l.strip().strip('|').split('|')]
            if len(c)==3 and c[0] not in('中文','---') and not c[0].startswith('-'): rows.append(c)
    return rows
QUIZ=[("下列哪個鍵最極性？",["H–H","S–H","Cl–H","F–H"],3,"F 電負度 4.0，與 H 的差 1.9 最大。"),
("NH₃ 的分子形狀是？",["四面體","三角錐","V 形","平面三角形"],1,"電子對排列為四面體，但有 1 對孤對，原子排成三角錐。"),
("CO₂ 有極性鍵，為什麼整體沒有偶極矩？",["C=O 不是極性鍵","兩個鍵偶極方向相反而抵消","O 電負度比 C 小","孤對電子抵消了"],1,"線形對稱，鍵偶極相消。"),
("Al³⁺、Mg²⁺、Na⁺、F⁻、O²⁻ 中半徑最小的是？",["O²⁻","F⁻","Na⁺","Al³⁺"],3,"等電子系列，Z 愈大半徑愈小（50 pm）。"),
("SO₄²⁻ 全單鍵結構中，S 的形式電荷是？",["0","+1","+2","−2"],2,"6 − (0 + ½·8) = +2。"),
("O₂、O₂⁺、O₂⁻ 中，鍵最強的是？",["O₂","O₂⁺","O₂⁻","三者相同"],1,"鍵級依序 2、2.5、1.5。"),
("溫度升高時，金屬的導電性會？",["增加","降低","不變","先增後減"],1,"金屬降低；矽等半導體則增加。"),
("SiO₂ 為什麼是固體而 CO₂ 是氣體？",["SiO₂ 分子量大很多","Si 形成不了強 π 鍵，變成網狀固體","SiO₂ 有氫鍵","Si 電負度比 C 大"],1,"Si 的 3p 與 O 形成不了強 π 鍵，改用單鍵連成網狀。")]
CSS="""
:root{--bg:#f7f5f0;--fg:#1f2430;--mut:#667;--card:#fff;--acc:#c2410c;--ln:#d9d4c8;--b1:#1e5a8a}
@media(prefers-color-scheme:dark){:root{--bg:#171a21;--fg:#e8e6df;--mut:#9aa;--card:#222733;--acc:#fb923c;--ln:#3a4152;--b1:#7ab8e8}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--fg);font:17px/1.65 system-ui,"Noto Sans TC","PingFang TC",sans-serif}
header{padding:10px 20px;border-bottom:1px solid var(--ln);display:flex;justify-content:space-between;font-size:14px;color:var(--mut)}
main{max-width:1000px;margin:0 auto;padding:12px 20px 90px}
.slide{display:none}.slide.on{display:block}
.kick{color:var(--acc);font-weight:600;font-size:14px;letter-spacing:.05em}
h1{font-size:30px;margin:4px 0 16px;line-height:1.3}
.lead{font-size:19px}.small{font-size:14px;color:var(--mut)}.warn{background:rgba(234,179,8,.15);border-left:4px solid #ca8a04;padding:8px 12px;font-size:15px}
.cols{display:grid;grid-template-columns:1fr 1fr;gap:24px;align-items:start}.cols.tight{margin-top:8px}
@media(max-width:760px){.cols{grid-template-columns:1fr}h1{font-size:24px}}
.card{background:var(--card);border:1px solid var(--ln);border-radius:10px;padding:12px 16px}
.formula{font-family:"Cambria Math",Georgia,serif;font-size:18px;background:var(--card);border:1px solid var(--ln);padding:8px 12px;border-radius:8px}
.acc{color:var(--acc);font-weight:600;fill:var(--acc)}
.tbl{border-collapse:collapse;width:100%;font-size:15px}.tbl th,.tbl td{border:1px solid var(--ln);padding:6px 10px;text-align:left}.tbl th{background:var(--card)}.tbl .sum td{font-weight:700}
.chain{display:flex;flex-wrap:wrap;gap:6px;align-items:center;margin:18px 0}.node{background:var(--card);border:2px solid var(--b1);border-radius:10px;padding:8px 10px;font-weight:600;font-size:15px}.node small{display:block;font-weight:400;color:var(--mut);font-size:12px}.chain b{color:var(--acc)}
.bars .brow{display:grid;grid-template-columns:110px 1fr 70px;gap:8px;align-items:center;margin:5px 0;font-size:14px}.bt{background:var(--ln);border-radius:4px;height:16px;display:block}.bt i{display:block;height:100%;background:var(--b1);border-radius:4px}.bn{display:none}
.fig{width:100%;height:auto}.fig .axis{stroke:var(--mut);stroke-width:1.5}.fig .dash{stroke:var(--mut);stroke-dasharray:4 4}.fig .curve{fill:none;stroke:var(--b1);stroke-width:3}.fig .t{fill:var(--fg);font-size:14px}.fig .sm{font-size:12px;fill:var(--mut)}.fig .w{fill:#fff;font-weight:700}
.fig .o{fill:#c0392b}.fig .c{fill:#555}.fig .h{fill:#aab}.fig .arr{stroke:var(--acc);stroke-width:2.5}.fig .arr.thick{stroke-width:5}.afill{fill:var(--acc)}
.spectrum{margin:10px 0}.sp-bar{height:14px;border-radius:7px;background:linear-gradient(90deg,#3b82f6,#a78bfa,#ef4444)}.sp-l{display:flex;justify-content:space-between;font-size:14px;margin-top:4px}.sp-l.big span{text-align:center;flex:1}.sp-l small{display:block;color:var(--mut)}
.myth li{margin:8px 0}.myth s{color:var(--mut)}
details{margin-top:16px;font-size:14px}summary{cursor:pointer;color:var(--b1)}details table{width:100%;border-collapse:collapse;margin-top:6px}details td,details th{border:1px solid var(--ln);padding:3px 8px;text-align:left}
.vocab{margin-top:18px}.vocab h3{font-size:15px;margin:0 0 4px;color:var(--mut)}
nav{position:fixed;bottom:0;left:0;right:0;background:var(--card);border-top:1px solid var(--ln);display:flex;gap:10px;align-items:center;justify-content:center;padding:10px}
button{font:inherit;padding:6px 16px;border:1px solid var(--ln);background:var(--bg);color:var(--fg);border-radius:8px;cursor:pointer}
.q{background:var(--card);border:1px solid var(--ln);border-radius:10px;padding:10px 14px;margin:8px 0}.q button{display:block;margin:4px 0;width:100%;text-align:left}.q .ok{background:rgba(34,197,94,.25)}.q .no{background:rgba(239,68,68,.25)}.q p{margin:2px 0}
"""
out=[]
for i,s in enumerate(SLIDES,1):
    v=[];seen=set()
    for p in s['pages']:
        for r in vocab(p):
            if r[1] not in seen: seen.add(r[1]);v.append(r)
    cl="".join(f"<tr><td>{html.escape(c)}</td><td>[[{html.escape(pg)}]]</td></tr>" for c,pg,n in s['claims'])
    vt=""
    if v:
        vt='<div class="vocab"><h3>重要單字 Vocabulary</h3><table class="tbl"><tr><th>中文</th><th>English</th><th>符號</th></tr>'+"".join(f"<tr><td>{a}</td><td>{b}</td><td>{c}</td></tr>" for a,b,c in v[:12])+'</table></div>'
    out.append(f'<section class="slide" id="s{i}"><div class="kick">{s["kicker"]}　{i}/{len(SLIDES)}</div><h1>{s["title"]}</h1>{s["html"]}{vt}<details><summary>Wiki 依據（這頁每個論點出自哪裡）</summary><table><tr><th>論點</th><th>Wiki 頁面</th></tr>{cl}</table></details></section>')
js="""
const S=[...document.querySelectorAll('.slide')];let n=0;
function go(k){n=Math.max(0,Math.min(S.length-1,k));S.forEach((e,i)=>e.classList.toggle('on',i===n));document.getElementById('pos').textContent=(n+1)+' / '+S.length;try{location.hash='s'+(n+1)}catch(e){}}
document.getElementById('prev').onclick=()=>go(n-1);document.getElementById('next').onclick=()=>go(n+1);
addEventListener('keydown',e=>{if(e.key==='ArrowRight'||e.key===' ')go(n+1);if(e.key==='ArrowLeft')go(n-1)});
const Q=%s;const qb=document.getElementById('quiz');
Q.forEach((q,qi)=>{const d=document.createElement('div');d.className='q';d.innerHTML='<p><b>'+(qi+1)+'. '+q[0]+'</b></p>';const fb=document.createElement('p');fb.className='small';
q[1].forEach((o,oi)=>{const b=document.createElement('button');b.textContent=o;b.onclick=()=>{d.querySelectorAll('button').forEach(x=>x.disabled=true);b.classList.add(oi===q[2]?'ok':'no');if(oi!==q[2])d.querySelectorAll('button')[q[2]].classList.add('ok');fb.textContent=(oi===q[2]?'答對！':'再想想。')+q[3]};d.appendChild(b)});d.appendChild(fb);qb.appendChild(d)});
let h=parseInt((location.hash||'').slice(2));go(isNaN(h)?0:h-1);
"""%json.dumps(QUIZ,ensure_ascii=False)
doc=f'<!doctype html><html lang="zh-Hant"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>化學鍵結與分子結構入門</title><style>{CSS}</style></head><body><header><span>化學鍵結與分子結構入門（LLM Wiki 產出）</span><span>← → 換頁</span></header><main>{"".join(out)}</main><nav><button id="prev">← 上一頁</button><span id="pos"></span><button id="next">下一頁 →</button></nav><script>{js}</script></body></html>'
os.makedirs('/mnt/user-data/outputs/slides',exist_ok=True)
open('/mnt/user-data/outputs/slides/化學鍵結與分子結構入門.html','w',encoding='utf-8').write(doc)
print(len(doc))
