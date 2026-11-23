import sys,re,glob,os
sys.path.insert(0,'.')
from deck_all import SLIDES, MISSING
W='/mnt/user-data/outputs/wiki/'
pages={os.path.basename(p)[:-3]:open(p,encoding='utf-8').read() for p in glob.glob(W+'*.md')}
corpus="\n".join(v for k,v in pages.items() if not k.startswith('分析-'))
bad=0
for i,s in enumerate(SLIDES,1):
    for p in s['pages']:
        if p not in pages: print(f"S{i} page missing: {p}"); bad+=1
    for c,pg,n in s['claims']:
        if pg not in pages: print(f"S{i} claim page missing {pg}"); bad+=1
        elif n not in pages[pg]: print(f"S{i} NEEDLE MISS [{pg}] {n!r}  <- {c}"); bad+=1
print("needle failures:",bad)
# numbers in slides html must appear in corpus
nb=0
for i,s in enumerate(SLIDES,1):
    txt=re.sub(r'<[^>]+>',' ',s['html'])
    for m in set(re.findall(r'[−-]?\d+(?:\.\d+)?',txt)):
        if m.lstrip('−-') not in corpus.replace('−','-'):
            print(f"S{i} number not in wiki: {m}"); nb+=1
print("number failures:",nb)
for t,keys,note in MISSING:
    hit=[k for k in keys if k in corpus]
    print("MISSING-list:",t,"| in wiki:",hit)
