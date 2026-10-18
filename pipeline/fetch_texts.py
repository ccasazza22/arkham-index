"""Download the 37 corpus stories from hplovecraft.com into corpus/raw/.

Usage: python pipeline/fetch_texts.py
The raw HTML is not committed (see .gitignore); re-run this to rebuild the corpus.
"""
import os
import time
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'corpus', 'raw')
BASE = 'https://www.hplovecraft.com/writings/texts/fiction/{}.aspx'

# story id used throughout the site -> page code on hplovecraft.com
STORIES = {
    'dagon': 'd', 'polaris': 'p', 'statement': 'src', 'sarnath': 'ds', 'jermyn': 'faj',
    'ulthar': 'cu', 'celephais': 'c', 'nyarl': 'n', 'othergods': 'og', 'zann': 'mez',
    'nameless': 'nc', 'outsider': 'o', 'west': 'hwr', 'hound': 'h', 'rats': 'rw',
    'unnamable': 'u', 'festival': 'f', 'coc': 'cc', 'pickman': 'pm', 'silverkey': 'sk',
    'strangehouse': 'shh', 'kadath': 'dq', 'cdw': 'cdw', 'colour': 'cs', 'yig': 'cy',
    'dunwich': 'dh', 'mound': 'mo', 'whisperer': 'wid', 'mountains': 'mm', 'innsmouth': 'soi',
    'witch': 'dwh', 'museum': 'hm', 'gate': 'tgsk', 'aeons': 'oa', 'doorstep': 'td',
    'shadowtime': 'sot', 'haunter': 'hd',
}


def main():
    os.makedirs(OUT, exist_ok=True)
    for sid, code in STORIES.items():
        req = urllib.request.Request(BASE.format(code), headers={'User-Agent': 'Mozilla/5.0 (arkham-index corpus fetch)'})
        with urllib.request.urlopen(req, timeout=30) as r:
            data = r.read()
        with open(os.path.join(OUT, sid + '.html'), 'wb') as f:
            f.write(data)
        print(f'{sid:13} {len(data):>8} bytes')
        time.sleep(0.5)  # be polite to the host


if __name__ == '__main__':
    main()
