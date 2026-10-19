# The Arkham Index

A data deep dive into H. P. Lovecraft's fiction. Every god, creature, person, place and forbidden book he names, counted across 37 stories and connected by the paragraphs they share.

The site is one static page. Its centrepiece is an interactive network with a guided tour, followed by findings (frequency, distribution, growth, strongest bonds), a catalogue of every entry, the stories with their casts, a quiz, and a full methodology.

## Repository layout

```
src/
  index.template.html   page markup, styles and code; /*CATALOGUE*/ and /*COUNTS*/ mark where data goes
  catalogue.js          hand-written stories (S) and entries (E): names, epithets, descriptions, curated links
data/
  counts.json           generated mention and co-mention counts (committed)
pipeline/
  fetch_texts.py        download the 37 stories from hplovecraft.com -> corpus/raw/
  extract.py            split each story into paragraphs           -> corpus/text/
  count.py              apply the search patterns                  -> data/counts.json
  verify_pdf.py         cross-check counts against a PDF edition (optional)
  build.py              assemble the site                          -> public/index.html
public/                 the deployable site (index.html, favicon.svg, _headers)
METHODOLOGY.md          how the numbers are made, checked and limited
wrangler.toml           Cloudflare Pages config
```

`corpus/` is git-ignored. The story texts are downloaded fresh by the pipeline rather than redistributed.

## Building

Python 3.9+ is the only requirement. No packages are needed.

```sh
# rebuild the site from the committed counts (all a deploy needs)
python pipeline/build.py

# re-derive the counts from the source texts
python pipeline/fetch_texts.py
python pipeline/extract.py
python pipeline/count.py
python pipeline/build.py
```

To change how an entry is counted, edit its patterns in `pipeline/count.py`, then run `count.py` and `build.py`. To change descriptions or curated links, edit `src/catalogue.js`, then run `build.py`.

Preview locally with any static server, for example `python -m http.server -d public 8000`.

## Deploying to Cloudflare Pages

**Git integration (recommended).** Push this repo to GitHub or GitLab. Then, in the Cloudflare dashboard, go to Workers & Pages → Create → Pages → Connect to Git and use these settings:

| Setting | Value |
|---|---|
| Framework preset | None |
| Build command | `python3 pipeline/build.py` (or leave empty) |
| Build output directory | `public` |

Every push to the production branch deploys, and other branches get preview URLs. Because `public/index.html` is committed, an empty build command also works. Cloudflare then serves `public/` as it is, so run `build.py` locally before you push.

**Direct upload.** From the repo root, run:

```sh
npx wrangler pages deploy
```

Wrangler reads `wrangler.toml` and uploads `public/`.

`public/_headers` sets a Content Security Policy that allows only the page's inline code and Google Fonts, plus basic security and cache headers.

## Credits

Story texts come from [hplovecraft.com](https://www.hplovecraft.com/writings/texts/). Descriptions, epithets and curated connections are original writing. Short quotations are used for commentary.
