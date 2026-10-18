"""Assemble the site.

Usage:
  python pipeline/build.py              -> public/index.html (full document, for Cloudflare Pages)
  python pipeline/build.py --fragment F -> F (body fragment without <html>/<head>, for embedding)

Inputs: src/index.template.html, src/catalogue.js, data/counts.json.
"""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def read(*p):
    return open(os.path.join(ROOT, *p), encoding='utf-8').read()


def fragment():
    tpl = read('src', 'index.template.html')
    cat = read('src', 'catalogue.js')
    counts = json.loads(read('data', 'counts.json'))
    data = 'const DATA=' + json.dumps(counts, ensure_ascii=False, separators=(',', ':')) + ';'
    for marker in ('/*CATALOGUE*/', '/*COUNTS*/'):
        assert tpl.count(marker) == 1, f'template must contain {marker} exactly once'
    return tpl.replace('/*CATALOGUE*/', cat).replace('/*COUNTS*/', data)


HEAD = '''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="description" content="A data deep dive into H. P. Lovecraft's fiction: every god, creature, person, place and book he names, counted and connected.">
<meta property="og:title" content="The Arkham Index">
<meta property="og:description" content="Every name in the Mythos, counted and connected.">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<style>:root{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}body{margin:0}img{max-width:100%}[hidden]{display:none!important}</style>
'''


def main():
    frag = fragment()
    if '--fragment' in sys.argv:
        dest = sys.argv[sys.argv.index('--fragment') + 1]
        open(dest, 'w', encoding='utf-8').write(frag)
        print('wrote', dest, len(frag), 'bytes')
        return
    # the fragment opens with <title>, <meta>, <link> and <style>; they belong in <head>
    split = frag.index('</style>') + len('</style>')
    page = HEAD + frag[:split] + '\n</head>\n<body>\n' + frag[split:] + '\n</body>\n</html>\n'
    os.makedirs(os.path.join(ROOT, 'public'), exist_ok=True)
    dest = os.path.join(ROOT, 'public', 'index.html')
    open(dest, 'w', encoding='utf-8').write(page)
    print('wrote', dest, len(page), 'bytes')


if __name__ == '__main__':
    main()
