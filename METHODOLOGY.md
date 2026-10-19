# Methodology

The Arkham Index asks one question of Lovecraft's fiction: **how often does he name each god, creature, person, place and book, and which names does he put together?** Every number on the site comes from the pipeline in `pipeline/`. It fetches the stories, splits them into paragraphs, runs a fixed set of search patterns over every paragraph, and records what it finds.

With revisions included, the current corpus gives 5,327 name mentions of 109 entries across 37 stories (434,000 words), and 588 pairs of entries that share at least one paragraph. The site recomputes these figures live when revisions are switched off.

## 1. Corpus

There are 37 stories: 32 written by Lovecraft alone, plus five revisions and collaborations he ghost-wrote or substantially rewrote:

- *The Curse of Yig* and *The Mound*, with Zealia Bishop
- *The Horror in the Museum* and *Out of the Aeons*, with Hazel Heald
- *Through the Gates of the Silver Key*, with E. Hoffmann Price

The revisions are tagged throughout, and the site's **Revisions** switch removes them and their counts everywhere.

The corpus covers the Mythos-relevant fiction from "Dagon" (1917) to "The Haunter of the Dark" (1935). Juvenilia, poetry and stories with no Mythos entities are excluded. The full list, with the page code for each story, is in `pipeline/fetch_texts.py`.

- **Source.** The e-texts at hplovecraft.com, one page per story.
- **Paragraphs.** The source's own paragraph breaks (`<br>`/`<p>` in the page markup), extracted by `pipeline/extract.py`.
- **Words.** Whitespace-separated tokens.
- **Years.** Dates of composition, not publication.

## 2. What counts as an entry

Entries are chosen by hand, using one canon rule: **only what appears in Lovecraft's own fiction**. August Derleth's additions and later writers' creations are excluded. A few names Lovecraft borrowed from friends are included and flagged, because Lovecraft wrote them into his own stories:

- Tsathoggua and the Book of Eibon, from Clark Ashton Smith
- von Junzt's *Unaussprechlichen Kulten*, from Robert E. Howard
- the Hounds of Tindalos, from Frank Belknap Long

There are 109 entries in eight categories: Other Gods; Great Old Ones & Deities; Beings & Races; Dreamlands Creatures; People; Cults; Places; Tomes & Artifacts. The web folds these into four groups: gods, creatures, people & cults, and places & books. Descriptions, epithets and "curated connections" (`src/catalogue.js`) are editorial. The counts are not.

## 3. Counting mentions

`pipeline/count.py` defines, for each entry, a list of `(regex, stories)` pairs. Each pattern is the entry's name, plus a few fixed aliases where Lovecraft uses another name for the same thing. Some examples:

| Entry | Alias | Story |
|---|---|---|
| Cthulhu | `Tulu` | *The Mound* |
| Mi-Go | `Outer Ones` | *The Whisperer in Darkness* |
| Nyarlathotep | `Black Man` | *The Dreams in the Witch House* |
| Nyarlathotep | `Haunter of the Dark` | *The Haunter of the Dark* |
| Deep Ones | `them things`, `sea-things`, `fish-frogs` | *The Shadow over Innsmouth* |

The rules:

1. **Case-sensitive** unless a pattern allows both cases (`[Gg]houls?`). This keeps "West" the man apart from "west" the direction.
2. **Word boundaries** (`\b`) where a name could match inside another word.
3. **Story scoping.** A pattern that is ambiguous across the corpus runs only in the stories where it's unambiguous:
   - `\bWest\b` only in *Herbert West—Reanimator*
   - `\bLake\b` only in *At the Mountains of Madness*
   - `Innsmouth` everywhere except "Celephaïs", whose Innsmouth is a Cornish village
4. **Normalisation.** Curly apostrophes become straight ones before matching.
5. **Every match counts.** Three uses in one paragraph count three times.

An entry's "Appears in" list combines the stories where it was matched with stories where a hand check found it present but unnamed, such as a first-person narrator. Present-but-unnamed stories show a dash.

## 4. Co-mentions

Two entries are **co-mentioned** when both are matched in the same paragraph. Each pair counts **at most once per paragraph**, however many times either name appears. A link's weight is the number of shared paragraphs. `data/counts.json` stores these weights per story, so the site can drop revision stories and light up a single story's links.

The paragraph is the unit because it's the smallest span where Lovecraft reliably keeps one subject in view. Sentences are too short to catch an invocation and its effect. Whole stories are too coarse, since everything would link to everything. The web's "at least" slider hides links below a chosen weight (default 2) to remove one-off coincidences.

## 5. Validation

- **Reproducibility.** Re-running `fetch_texts.py`, `extract.py` and `count.py` from scratch reproduces the committed `data/counts.json` exactly: mentions, co-mentions and word counts.
- **Second edition.** `pipeline/verify_pdf.py` counts raw names in a *Complete Works* PDF and in the corpus. These appear the same number of times in both:

  | Name | Count |
  |---|---|
  | Akeley | 135 |
  | Wilbur | 48 |
  | Curwen | 204 |
  | Gilman | 122 |
  | Necronomicon | 49 |

  This checks the transcription, not attribution: only 103 of the 122 "Gilman"s are Walter Gilman (see below). Other names differ in both directions, for known reasons. The PDF leaves out the five revisions (it never mentions Zamacona) and includes stories outside this corpus.
- **Review of low counts.** Suspiciously small totals were read in context, which led to three corrections:
  - *The Shadow over Innsmouth* uses the words "Deep Ones" only twice, so their usual names there were added as scoped aliases.
  - In *The Shadow Out of Time*, "Elder Things" means the flying polyps, so those matches are credited to the polyps.
  - "Old Ones" in *At the Mountains of Madness* excludes "Great Old Ones".
- **Review of stray matches.** Every match in a story outside an entry's expected stories was read in context. Most are Lovecraft name-dropping his own creations, and they stay. Six were other things with the same name and were scoped out:
  - "Gilman" in *Innsmouth* and *Doorstep*: the Gilman House hotel and the Innsmouth Gilman family, not Walter (19 matches).
  - "Ghoul" in *Charles Dexter Ward*, "The Hound", *Herbert West* and "The Nameless City": grave-robbers or a figure of speech (11).
  - "Kadath" inside "Kadatheron", in "Sarnath" and *Dream-Quest* (6). The pattern is now `Kadath\b`.
  - "Hydra" in *Witch House*: the constellation (2).
  - "Thurston" in *Ward*: Thurston's Tavern (1).
  - "Elder Things" in *Dunwich*: Armitage's vague phrase, not the Antarctic beings (1).
- **Transparency.** Every entry shows its exact patterns, on its card and in the site's Method table.

## 6. Limitations

- **Pronouns aren't counted.** First-person narrators come out tiny. Thurston is named 2 times and Dyer 7, and two entries (the Innsmouth narrator and the Outsider) are never named. A node's size measures how often it's named, not how important it is.
- **Aliases are judgment calls.** Adding or removing one changes a count. They're all listed.
- **Some scoped patterns are broad.** These also catch some generic uses, so their counts run high:
  - "colour" in *The Colour Out of Space*
  - "city" in *Mountains of Madness* and *The Shadow Out of Time*
  - "cats" in the Ulthar stories
  - "cult" in *The Call of Cthulhu*
- **Name collisions.**
  - "Ward" also catches Charles's father.
  - "de la Poer" catches the whole family.
  - Both "Edward" and "Derby" count for Edward Derby.
  - "Ephraim" counts for Asenath, because they share one mind.
- **Paragraph length varies.** *Charles Dexter Ward* has long paragraphs, which inflates co-mentions within it.
- **One edition.** Spelling and paragraph breaks follow a single e-text source.

## 7. Visual encoding

- **Node size.** Radius = 2.6 + 1.05 × √mentions, so a node's *area* roughly tracks its count.
- **Layout.** A force simulation: linked entries attract, all entries repel, and colliding nodes push apart. The pull toward the centre is weaker sideways, so the web stretches to fit a wide screen. Closeness means "often named together." Absolute position carries no meaning and varies slightly per visit.
- **Labels.** Drawn in order of mention count. A label that would overlap one already drawn is hidden until you zoom in or hover.
- **Clusters.** Shaded bubbles are communities found by Louvain modularity optimisation on the links currently drawn, weighted by shared paragraphs. Nodes are visited in id order, so the result is deterministic for a given link set. Changing the "at least" slider or the revisions switch re-runs it. Communities with fewer than five members get no bubble, and each bubble is named after its two most-named members. In the layout, links inside a community pull harder than links between communities, which keeps bubbles apart. This is an aid to reading the web, not a claim about what the clusters mean.
- **Links.** Width grows with √weight. In "light up a story" mode, links and node sizes use that story's counts only.
- **Colour.** Four group colours (alien magenta, sickly green, drowned blue, oozing purple) were checked for all six pairs against the page surface `#120D1C`, covering lightness band, chroma, separation under colour-vision deficiency, separation under normal vision, and contrast. All four pass. Each group also has a distinct shape (diamond, triangle, circle, square), so colour is never the only cue.
- **Heatmap.** A single-hue sequential scale on a square-root curve, so rare names stay visible next to common ones.

## 8. Reproducing

```sh
python pipeline/fetch_texts.py   # download stories -> corpus/raw/
python pipeline/extract.py       # paragraphs       -> corpus/text/
python pipeline/count.py         # counts           -> data/counts.json
python pipeline/build.py         # site             -> public/index.html
python pipeline/verify_pdf.py "path/to/complete-works.pdf"   # optional, needs pdftotext
```
