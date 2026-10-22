# Simple.solar — phase-wise build prompt

Use these phases in order with any capable AI coding assistant to rebuild, extend or clone this site. Each phase is self-contained; paste one phase at a time and verify before moving on.

---

## The idea (why this wins)

**Simple.solar = the plain-English solar decision engine.** Most solar sites sell one thing (rooftop quotes, or one brand of power station). Simple.solar routes every visitor to the right *kind* of solar — rooftop, battery, plug-in/balcony, portable, RV, off-grid or community — then monetizes each path:

| Revenue stream | Mechanism | Why it pays |
|---|---|---|
| Installer lead generation | 6-step quote funnel → up to 3 installers | Solar leads are among the most valuable in home services (typically tens to low hundreds of dollars each, exclusive higher) |
| Google AdSense | Auto ads + reserved manual slots | Home-improvement, energy and finance ads carry high CPCs |
| Sponsorships | Calculator, guide-cluster, newsletter, contest-prize sponsors | Power-station, battery and solar brands buy reach to in-market readers |
| Programmatic SEO | 51 state pages generated from public data | Captures "is solar worth it in [state]" and "solar cost [state]" searches |
| Reader support | Pledge form now; PayPal/Stripe links via `config.js` | Funds operations, contests, hiring and promotion |

Timing edge (October 2026): the US 30% homeowner tax credit ended for systems installed after 2025, and 10 states legalized plug-in solar in 2025–26. Search demand is shifting to "is solar still worth it", leases/PPAs, and balcony solar — exactly what this site answers.

---

## Phase 1 — Research and positioning
> Survey at least 35 leading solar websites (marketplaces like EnergySage, SolarReviews, Solar.com, Angi; publishers like Forbes Home, ConsumerAffairs, pv magazine; tools like NREL PVWatts, DSIRE, Google Project Sunroof; DIY/portable brands like Renogy, EcoFlow, Jackery, Anker SOLIX, Bluetti, Will Prowse; plug-in advocates like Bright Saver; international sources for the UK, Australia, Germany and India). For each, record what visitors come for, standout features, lead-form steps and fields, trust elements and design cues. Output: ranked list of shared patterns, the highest-converting lead-form sequence, content gaps a plain-English site can own, and design patterns to avoid copying. Save as RESEARCH.md.

## Phase 2 — Verified data
> Collect and cite, with "as of" dates: US federal incentive status (IRC 25D end date and the "expenditure made when installation is completed" rule; 48E for leases/PPAs), state tax credits (via DSIRE), Canada/UK/Australia/India programs, 2026 installed cost per watt (EnergySage, SEIA/Wood Mackenzie), battery cost ranges, EIA residential electricity price for all 50 states + DC, NREL peak sun hours by state, plug-in solar laws by state (bill numbers, caps, effective dates), Germany's balcony-solar rules. Verify 10–15 YouTube explainer videos via the oEmbed endpoint and keep only IDs that resolve. Save as `_build/data.py`.

## Phase 3 — Design system
> Create a distinct visual identity, not a template: palette (panel-cell ink #16233F, sun yolk #FFC23D, savings leaf #1D8A57, roof slate #5B6676, sky paper #F6F9FC), type (Bricolage Grotesque for headings, Atkinson Hyperlegible for body), one signature element (a hero "sun arc" whose fill tracks the share of the bill solar covers, driven by a bill slider and state select). Light and dark themes, visible focus, reduced-motion support, mobile-first, no horizontal scroll at 360 px. No all-caps eyebrows, no arrow-suffixed buttons.

## Phase 4 — Static site generator
> Write `_build/build.py` (Python, no dependencies) that turns page fragments (`_build/pages/*.html` with a `<!--meta-->` header) and guide fragments into finished HTML. Every page gets: canonical URL, Open Graph tags, JSON-LD (Organization, WebSite, Article, FAQPage, BreadcrumbList, WebApplication for tools), the AdSense script in `<head>`, the `google-adsense-account` meta tag, a top bar on every page reading "Contact, if you are interested in this website/domain name/Sponsorship/Advertisement/Partnership" linked to https://web.works/contact, sticky header, footer with legal links, cookie notice with "Essential only" → non-personalized ads. Also generate `sitemap.xml`. Output must run on GitHub Pages free plan (static only, `.nojekyll`, `CNAME`).

## Phase 5 — Calculators (client-side only)
> Build `assets/js/tools.js` with one shared model (production = kW × sun hours × 365 × 0.78; savings with 3% price rise, 0.5% degradation, 15% export haircut; no federal credit by default). Tools: savings & payback (bar chart of cumulative savings), system size, battery backup sizer (appliance list builder), portable power station runtime (brand-neutral), plug-in solar savings, and a 4-question "Which solar fits me?" quiz. Nothing is stored server-side.

## Phase 6 — Lead generation funnel
> Build a 6-step form: ZIP + state → own/rent/buying/business (renters routed to plug-in & community solar, not dropped) → monthly bill slider → roof sun → interest + timeline + payment → instant estimate shown *before* contact fields → name, email, optional phone, "who may contact you" (up to 3 / 1 / email only) → TCPA-style consent ("not a condition of purchase"). Progress bar, auto-advance on single-choice steps, prefill from the hero calculator and URL params, honeypot field, redirect to a thank-you page that repeats the estimate. Put it on the home page and a dedicated /quotes page; add an installer-partner application page for the B2B side.

## Phase 7 — Hidden-email form delivery
> All forms (quotes, installer, advertise, contact, careers, contests, support pledge, reader question, newsletter) POST JSON to FormSubmit's AJAX endpoint. The destination address must never appear in HTML, JS strings or the repo in plain text: store it as two reversed base64 fragments in `config.js` and assemble it at runtime. Grep the output for the address before every deploy; the result must be empty.

## Phase 8 — Content
> Write 20 original guides (1,100–1,600 words each, 8th-grade reading level, worked arithmetic, at least one table, 3–5 FAQs, "short answer" box): is solar worth it, cost, incentives, plug-in/balcony, how solar works, home batteries, renters, power stations, buy/loan/lease/PPA, net metering, quote checklist, choosing an installer, roof readiness, panel types, outage backup, RV/van, off-grid, winter, maintenance, selling a solar home. Plus glossary (57 terms, searchable), FAQ, video library (lite embeds that load YouTube only on click), trusted resources, and 51 generated state pages with verdict, bill-size table, incentives, plug-in status, FAQs and similar states.

## Phase 9 — Monetization and community pages
> Support page (amount tiers, designation: operations / research / contests & prizes / hiring / promotion; pledge form until payment links are pasted into `config.js`), contests page (two open contests + a student challenge, short official rules: no purchase necessary, skill-based judging, eligibility, Canadian skill-testing question), careers page (writers, solar advisors, video creators, data researchers, partnerships, ambassadors; anti-scam note), advertise page (sponsorship formats, ad rules, media-kit form), community hub, installer partner page.

## Phase 10 — AdSense approval readiness
> Ensure: original substantial content (20+ guides), About, Contact, Privacy (with the Google cookie/third-party vendor disclosure and opt-out links), Terms, Disclaimer, Editorial policy (including AI-use statement), Trademark & copyright notice; `ads.txt` with `google.com, pub-6620975821265271, DIRECT, f08c47fec0942fa0`; no ads on thank-you or 404 pages beyond Auto ads; no misleading buttons near ad slots; clear navigation; fast load; mobile-friendly. Reserve `.ad-slot` containers that only render manual units once slot IDs are added to `config.js`.

## Phase 11 — Trademark safety
> Always write the brand as "Simple.solar" (with the dot) — never "SimpleSolar" or "Simple Solar". Publish a trademark/copyright page stating independence from any company using a similar name, nominative fair use for third-party brands, copyright terms and an IP notice process. Use only original logo artwork.

## Phase 12 — QA, deploy and grow
> Automated checks: every page has the AdSense script and the owner top bar; zero broken internal links; no unrendered template tokens; no exposed email; no JS errors; screenshots at 1366 px and 390 px. Push to GitHub, enable Pages (branch `main`, root), set custom domain `simple.solar` with Enforce HTTPS, add DNS A/CNAME records. Submit `sitemap.xml` in Google Search Console, apply for AdSense, confirm the FormSubmit activation email. Growth backlog: city pages for the top 100 metros, monthly "solar price index", plug-in law tracker page, Spanish edition, YouTube shorts for each calculator, installer reviews.
