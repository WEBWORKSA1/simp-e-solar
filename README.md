# Simple.solar

Plain-English solar decisions: free calculators, 20 guides, 51 state pages, a high-converting quote funnel, and community pages (support, contests, careers, advertising). Static HTML, built for GitHub Pages (free plan) and Google AdSense.

**Live domain:** https://simple.solar

## Structure
- `index.html`, `quotes.html`, … — generated pages (served as-is by GitHub Pages)
- `tools/` — six in-browser calculators
- `guides/` — 20 long-form guides
- `states/` — 51 state pages + sortable comparison table
- `assets/` — CSS, JS (`config.js` holds AdSense, payment links and ad slot IDs)
- `_build/` — source: `build.py`, `data.py`, page fragments, guide fragments
- `RESEARCH.md` — survey of 44 solar-niche websites
- `PROMPTS.md` — phase-wise build prompt

## Rebuild
```
python3 _build/build.py
```

## Publishing
GitHub Pages publishes the `gh-pages` branch (kept identical to `main`). After changing `main`, merge `main` into `gh-pages` to publish. Alternatively switch Settings → Pages → Source to `main` / root and the `gh-pages` branch can be deleted.

## After launch
1. GitHub → Settings → Pages: confirm the source branch and the custom domain `simple.solar`, then tick Enforce HTTPS.
2. DNS at the registrar: A records for `@` → 185.199.108.153, 185.199.109.153, 185.199.110.153, 185.199.111.153; CNAME `www` → `webworksa1.github.io`.
3. AdSense: add the site, `ads.txt` is already at the root. Turn on Auto ads; optionally paste display-unit slot IDs into `assets/js/config.js` → `adSlots`.
4. AdSense → Privacy & messaging: enable Google's certified consent message for EEA/UK visitors.
5. Forms: the first form submission triggers a one-time FormSubmit activation email to the site inbox. Confirm it once.
6. Donations: paste a PayPal/Stripe/Buy Me a Coffee link into `assets/js/config.js` → `payments` to switch the Support page from pledge mode to instant checkout.

## Trademark
"Simple.solar" is used descriptively as the site's domain name. The site is not affiliated with any company using a similar name. See `trademark.html`.
