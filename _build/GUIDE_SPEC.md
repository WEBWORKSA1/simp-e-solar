# Guide fragment spec (Simple.solar)

Each guide is ONE file: `_build/guides/<slug>.html`. Exact format:

```
<!--meta
title: Plain title, sentence case, under 65 characters
description: One sentence, 120–155 characters, plain English, no hype.
cat: <one of: start | money | batteries | portable | living>
answer: 1–2 sentence direct answer to the title's question (plain text, may use <b>).
video: <one of: how | worth | battery | portable | plugin | install | types | netmeter> (topic for related videos)
-->
<p>Opening paragraph…</p>
<h2>Question-style heading</h2>
<p>…</p>
...
<h2>Frequently asked questions</h2>
<details class="faq"><summary>Question?</summary><p>Answer.</p></details>
(3–5 FAQ items, each on ONE line exactly in that format)
```

Rules
- 1,100–1,600 words of body. Original writing, plain English, 8th-grade reading level, short paragraphs, active voice, second person ("you").
- Use 5–8 `<h2>` sections (no ids — the builder adds them). `<h3>` allowed inside. No `<h1>`.
- Concrete numbers wherever possible, with worked examples ("a 6 kW system in a sunny state makes about 9,000 kWh a year"). Show the arithmetic.
- At least one `<table>` with `<thead>`/`<tbody>` where it helps (comparisons, sizing).
- Use `<div class="note">…</div>` for one key tip, at most two per guide.
- Internal links are relative to /guides/: other guides as `slug.html`; tools as `../tools/savings-calculator.html`, `../tools/system-size.html`, `../tools/battery-sizer.html`, `../tools/power-station.html`, `../tools/plug-in-solar.html`, `../tools/solar-match.html`; quotes page `../quotes.html`; glossary `../glossary.html`; states `../states/index.html`. Link 3–6 times naturally. Never link to external commercial sites. You may cite authorities in text (NREL, US DOE, EIA, SEIA, IEA) without links.
- No brand recommendations or affiliate language. Brand names may appear only as neutral examples (e.g., "power stations from brands like EcoFlow, Jackery, Anker and Bluetti").
- Do NOT state current incentive amounts, tax-credit availability or legal status as fact (those live in the incentives guide). Write "check current incentives in our <a href="solar-incentives.html">incentives guide</a>". Exception: the US 30% homeowner tax credit (25D) ended for systems installed after Dec 31, 2025 — you may say that.
- No medical, legal or guaranteed-savings claims. Safety advice: tell readers to use licensed electricians for wiring into a home panel.
- Never write an email address. Never use the words "Simple Solar" or "SimpleSolar"; the site name is "Simple.solar" if needed (rarely).
- No ALL CAPS, no emoji, no "In conclusion", no "In today's world", no "delve".
- Valid HTML only; escape `&` as `&amp;` and `<`/`>` in prose.
