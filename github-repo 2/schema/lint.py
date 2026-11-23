import glob,os,re,sys
W='/mnt/user-data/outputs/wiki/'
pages={os.path.basename(p)[:-3]:open(p,encoding='utf-8').read() for p in glob.glob(W+'*.md')}
F=['定義','重點','例題','常見誤解','矛盾','相關頁面','來源','信心程度','重要單字']
adm={'index','glossary','log'}
bad=0
for n,t in pages.items():
    for l in re.findall(r'\[\[([^\]]+)\]\]',t):
        if l not in pages and n not in('log',): print('LINK',n,'->',l); bad+=1
    if n in adm or n.startswith('分析'): continue
    for f in F:
        if not re.search(r'^## '+f+r'\s*$',t,re.M): print('FIELD',n,f); bad+=1
# glossary consistency: same English -> same Chinese
eng={}
for n,t in pages.items():
    if n in adm: continue
    m=re.search(r'## 重要單字\n(.*?)(?:\n## |\Z)',t,re.S)
    if not m: continue
    for l in m.group(1).splitlines():
        c=[x.strip() for x in l.strip().strip('|').split('|')]
        if len(c)==3 and c[0] not in('中文','---') and not c[0].startswith('-'):
            eng.setdefault(c[1].lower(),{}).setdefault(c[0],[]).append(n)
for e,d in eng.items():
    if len(d)>1: print('GLOSS',e,d); bad+=1
zh={}
for e,d in eng.items():
    for c in d: zh.setdefault(c,set()).add(e)
for c,s in zh.items():
    if len(s)>1: print('GLOSS-ZH',c,s); bad+=1
print('issues',bad,'pages',len(pages))
