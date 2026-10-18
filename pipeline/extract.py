"""Split each downloaded story page into paragraphs.

Usage: python pipeline/extract.py [raw_dir] [out_dir]
Defaults: corpus/raw -> corpus/text. Writes one JSON array of paragraph strings per story.
"""
import html
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, 'corpus', 'raw')
out = sys.argv[2] if len(sys.argv) > 2 else os.path.join(ROOT, 'corpus', 'text')
os.makedirs(out, exist_ok=True)

for fn in sorted(os.listdir(src)):
    if not fn.endswith('.html'):
        continue
    raw = open(os.path.join(src, fn), encoding='cp1252', errors='replace').read()
    # the story body sits in the first justified div and ends before the page footer
    i = raw.find('<div align="justify">')
    j = raw.find('This page last revised')
    body = raw[i:j]
    k = body.rfind('</div>')
    body = body[:k] if k > 0 else body
    parts = re.split(r'<br\s*/?>|</p>|<p[^>]*>', body)
    paras = []
    for p in parts:
        t = html.unescape(re.sub(r'<[^>]+>', ' ', p))
        t = re.sub(r'\s+', ' ', t).strip()
        if t:
            paras.append(t)
    json.dump(paras, open(os.path.join(out, fn.replace('.html', '.json')), 'w', encoding='utf-8'), ensure_ascii=False)
    print(f'{fn:18} {len(paras):>4} paragraphs {sum(len(p.split()) for p in paras):>7} words')
