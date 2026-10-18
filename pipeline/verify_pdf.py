"""Cross-check name counts against a second edition (a PDF of the complete works).

Usage: python pipeline/verify_pdf.py "path/to/The Complete Works of H.P. Lovecraft.pdf"
Needs `pdftotext` (poppler) on PATH. Prints whole-PDF counts beside corpus counts.
The PDF omits the five revisions but adds stories outside the corpus, so totals can differ
in either direction; exact matches on names confined to Lovecraft's solo corpus stories are the signal.
"""
import json
import os
import re
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NAMES = ['Akeley', 'Wilbur', 'Yog-Sothoth', 'Azathoth', 'Cthulhu', 'Necronomicon', 'Nyarlathotep',
         'Innsmouth', 'Arkham', 'Kadath', 'Curwen', 'Gilman', 'Zamacona']

pdf = sys.argv[1]
with tempfile.TemporaryDirectory() as d:
    txt = os.path.join(d, 'all.txt')
    subprocess.run(['pdftotext', '-enc', 'UTF-8', pdf, txt], check=True)
    t = open(txt, encoding='utf-8').read()
t = re.sub(r'-\n(\w)', r'\1', t.replace('’', "'"))
t = re.sub(r'\s+', ' ', t)

text_dir = os.path.join(ROOT, 'corpus', 'text')
corpus = ' '.join(' '.join(json.load(open(os.path.join(text_dir, f), encoding='utf-8')))
                  for f in os.listdir(text_dir) if f.endswith('.json')).replace('’', "'")
print(f'{"name":15} {"pdf":>6} {"corpus":>7}')
for n in NAMES:
    a, b = len(re.findall(n, t)), len(re.findall(n, corpus))
    print(f'{n:15} {a:>6} {b:>7}{"   exact" if a == b else ""}')
