"""Count entity mentions and same-paragraph co-mentions.

Usage: python pipeline/count.py [text_dir] [out_json]
Defaults: corpus/text -> data/counts.json.
Each entry in A maps an entity id to a list of (regex, stories) pairs. stories=None means the
pattern runs in every story; a list scopes it to those stories only (see METHODOLOGY.md).
"""
import json, re, os, sys, itertools
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TD = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, 'corpus', 'text')
OUT = sys.argv[2] if len(sys.argv) > 2 else os.path.join(ROOT, 'data', 'counts.json')
STORIES = sorted(f[:-5] for f in os.listdir(TD) if f.endswith('.json'))
CARTER = ['statement','unnamable','silverkey','kadath','gate']
NOT_CEL = [s for s in STORIES if s != 'celephais']
A = {  # id: [(regex, stories or None)]
 'azathoth':[(r"Azathoth",None)],
 'yogsothoth':[(r"Yog-Sothoth",None)],
 'nyarlathotep':[(r"Nyarlathotep|[Cc]rawling [Cc]haos",None),(r"Black Man",['witch']),(r"Haunter of the Dark",['haunter'])],
 'shub':[(r"Shub-Niggurath",None)],
 'cthulhu':[(r"Cthulhu",None),(r"\bTulu\b",['mound'])],
 'dagon':[(r"(?<!Order of )\bDagon\b",None)],
 'hydra':[(r"\bHydra\b",[x for x in STORIES if x!='witch'])],  # the constellation in Witch House
 'tsathoggua':[(r"Tsathoggua",None)],
 'yig':[(r"\bYig\b",None)],
 'ghatanothoa':[(r"Ghatanothoa",None)],
 'rhantegoth':[(r"Rhan-Tegoth",None)],
 'bokrug':[(r"Bokrug",None)],
 'nodens':[(r"Nodens",None)],
 'greatones':[(r"Great Ones|gods of [Ee]arth",['othergods','kadath'])],
 'umr':[(r"Umr at-Tawil",None)],
 'elderthings':[(r"Elder Things?",[x for x in STORIES if x not in ('shadowtime','dunwich')]),(r"(?<!Great )Old Ones",['mountains'])],
 'shoggoths':[(r"[Ss]hoggoths?",None)],
 'migo':[(r"Mi-[Gg]o",None),(r"Outer Ones?",['whisperer'])],
 'yith':[(r"Great Race|\bYith\b",None)],
 'polyps':[(r"[Pp]olyp|Elder Things?",['shadowtime'])],
 'deepones':[(r"Deep Ones?",None),(r"[Ff]ish-frogs?|[Ff]rog-fish|[Ss]ea-things?|[Tt]hem things",['innsmouth'])],
 'starspawn':[(r"[Ss]tar-spawn|spawn of Cthulhu|Cthulhu spawn",None)],
 'colour':[(r"\b[Cc]olou?r\b",['colour'])],
 'twin':[(r"\b[Tt]win\b|[Tt]he [Hh]orror\b|[Ii]nvisible (?:thing|[Hh]orror)",['dunwich'])],
 'brownjenkin':[(r"Brown Jenkin",None)],
 'kenyan':[(r"K'n-yan",None)],
 'ghouls':[(r"\b[Gg]houls?\b",[x for x in STORIES if x not in ('cdw','hound','west','nameless')])],  # grave-robbers and figures of speech there
 'nightgaunts':[(r"[Nn]ight-gaunts?",None)],
 'gugs':[(r"\b[Gg]ugs?\b",None)],
 'ghasts':[(r"\b[Gg]hasts?\b",None)],
 'moonbeasts':[(r"[Mm]oon-beasts?",None)],
 'lengmen':[(r"men (?:of|from) Leng",None)],
 'zoogs':[(r"\b[Zz]oogs?\b",None)],
 'shantaks':[(r"[Ss]hantaks?",None)],
 'cats':[(r"\b[Cc]ats?\b",['ulthar','kadath'])],
 'thurston':[(r"Thurston",['coc'])],  # "Thurston's Tavern" in Ward
 'angell':[(r"Angell|my (?:grand-?|great-?)?uncle",['coc'])],
 'legrasse':[(r"Legrasse",None)],
 'johansen':[(r"Johansen",None)],
 'wilcox':[(r"Wilcox",None)],
 'castro':[(r"Castro",None)],
 'carter':[(r"\bCarter\b",CARTER),(r"Randolph Carter",[s for s in STORIES if s not in CARTER])],
 'warren':[(r"\bWarren\b",['statement'])],
 'west':[(r"\bWest\b",['west'])],
 'alhazred':[(r"Alhazred|mad Arab",None)],
 'wilbur':[(r"Wilbur",None)],
 'lavinia':[(r"Lavinia",None)],
 'oldwhateley':[(r"[Oo]ld Whateley|Wizard Whateley",None)],
 'armitage':[(r"Armitage",None)],
 'wilmarth':[(r"Wilmarth",None)],
 'akeley':[(r"Akeley",None)],
 'dyer':[(r"\bDyer\b",None)],
 'danforth':[(r"Danforth",None)],
 'lake':[(r"\bLake\b",['mountains'])],
 'olmstead':[(r"Olmstead",None)],
 'zadok':[(r"Zadok",None)],
 'obed':[(r"\bObed\b",None)],
 'peaslee':[(r"Peaslee",None)],
 'ward':[(r"\bWard\b|\bCharles\b",['cdw'])],
 'curwen':[(r"Curwen",None)],
 'willett':[(r"Willett",None)],
 'gilman':[(r"Gilman",['witch'])],  # Innsmouth's Gilman House and Gilman family are not Walter
 'keziah':[(r"Keziah",None)],
 'pickman':[(r"Pickman",['pickman','kadath'])],
 'zann':[(r"\bZann\b",None)],
 'blake':[(r"\bBlake\b",['haunter'])],
 'derby':[(r"\bDerby\b|\bEdward\b",['doorstep'])],
 'asenath':[(r"Asenath|Ephraim",['doorstep'])],
 'upton':[(r"\bUpton\b",['doorstep'])],
 'nahum':[(r"Nahum",None)],
 'ammi':[(r"\bAmmi\b",None)],
 'delapore':[(r"Delapore|de la Poer",['rats'])],
 'jermyn':[(r"\bArthur\b",['jermyn'])],
 'kuranes':[(r"Kuranes",None)],
 'barzai':[(r"Barzai",None)],
 'atal':[(r"\bAtal\b",None)],
 'rogers':[(r"Rogers",['museum'])],
 'zamacona':[(r"Zamacona",None)],
 'tyog':[(r"T'yog",None)],
 'outsider':[],
 'cthulhucult':[(r"\b[Cc]ult\b",['coc'])],
 'eod':[(r"Order of Dagon|Esoteric Order|\bthe Order\b",['innsmouth'])],
 'starrywisdom':[(r"Starry Wisdom",None)],
 'rlyeh':[(r"R'lyeh",None)],
 'yhanthlei':[(r"Y'ha-nthlei",None)],
 'arkham':[(r"Arkham",None)],
 'miskatonic':[(r"Miskatonic(?! River| [Vv]alley)",None)],
 'innsmouth':[(r"Innsmouth",NOT_CEL)],
 'dunwich':[(r"Dunwich",None)],
 'kingsport':[(r"Kingsport",None)],
 'blastedheath':[(r"blasted heath",None)],
 'sentinelhill':[(r"Sentinel Hill",None)],
 'exham':[(r"Exham",None)],
 'yuggoth':[(r"Yuggoth",None)],
 'leng':[(r"\bLeng\b",None)],
 'kadath':[(r"Kadath\b",None)],  # not Kadatheron in Sarnath
 'ulthar':[(r"Ulthar",None)],
 'celephais':[(r"Celepha[iï]s",None)],
 'sarnath':[(r"Sarnath",None)],
 'namelesscity':[(r"[Nn]ameless [Cc]ity|\bthe city\b",['nameless'])],
 'antarctic':[(r"\bcity\b",['mountains'])],
 'yithcity':[(r"\bcity\b|\barchives?\b",['shadowtime'])],
 'necronomicon':[(r"Necronomicon|Al Azif",None)],
 'pnakotic':[(r"Pnakotic",None)],
 'eibon':[(r"Eibon",None)],
 'kulten':[(r"Unaussprechlichen|von Junzt",None)],
 'trapezohedron':[(r"Trapezohedron",None)],
 'silverkey':[(r"[Ss]ilver [Kk]ey",None)],
}
comp = {k:[(re.compile(r), set(s) if s else None) for r,s in v] for k,v in A.items()}
mentions = {k:{} for k in A}; co = {}; words = {}
for s in STORIES:
    paras = json.load(open(os.path.join(TD, s+'.json'), encoding='utf-8'))
    paras = [p.replace('\u2019',"'").replace('\u2018',"'") for p in paras]
    words[s] = sum(len(p.split()) for p in paras)
    for p in paras:
        present = []
        for k, pats in comp.items():
            n = sum(len(rx.findall(p)) for rx, ss in pats if ss is None or s in ss)
            if n:
                mentions[k][s] = mentions[k].get(s, 0) + n
                present.append(k)
        for a, b in itertools.combinations(sorted(present), 2):
            d = co.setdefault((a,b), {}); d[s] = d.get(s, 0) + 1
out = {'mentions':mentions, 'co':[[a,b,w] for (a,b),w in sorted(co.items(), key=lambda x:-sum(x[1].values()))], 'words':words,
       'aliases':{k:[[r, s if s and len(s) < len(STORIES)-1 else None] for r,s in v] for k,v in A.items()}}
json.dump(out, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False)
tot = sorted(((sum(v.values()),k) for k,v in mentions.items()), reverse=True)
print('TOP', tot[:30]); print('LOW', tot[-25:]); print('edges', len(co), 'top', out['co'][:5])
