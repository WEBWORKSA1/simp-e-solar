"""Simple.solar data. Update yearly. Sources noted inline."""

# Residential electricity price, cents/kWh — EIA Electric Power Monthly Table 5.6.A, July 2026 data (released Sep 24, 2026).
# Peak sun hours/day — NREL PVWatts v8 / NSRDB for each state's largest city (approximate; varies by location).
STATES = [
    dict(code="AL", name="Alabama", slug="alabama", rate=16.4, sun=5.21),
    dict(code="AK", name="Alaska", slug="alaska", rate=28.8, sun=3.17),
    dict(code="AZ", name="Arizona", slug="arizona", rate=15.4, sun=6.54),
    dict(code="AR", name="Arkansas", slug="arkansas", rate=14.3, sun=5.18),
    dict(code="CA", name="California", slug="california", rate=33.6, sun=6.08),
    dict(code="CO", name="Colorado", slug="colorado", rate=17.0, sun=5.66),
    dict(code="CT", name="Connecticut", slug="connecticut", rate=24.2, sun=4.53),
    dict(code="DE", name="Delaware", slug="delaware", rate=18.5, sun=4.8),
    dict(code="FL", name="Florida", slug="florida", rate=15.0, sun=5.48),
    dict(code="GA", name="Georgia", slug="georgia", rate=16.3, sun=5.17),
    dict(code="HI", name="Hawaii", slug="hawaii", rate=48.0, sun=5.82),
    dict(code="ID", name="Idaho", slug="idaho", rate=13.7, sun=5.22),
    dict(code="IL", name="Illinois", slug="illinois", rate=19.2, sun=4.51),
    dict(code="IN", name="Indiana", slug="indiana", rate=16.7, sun=4.66),
    dict(code="IA", name="Iowa", slug="iowa", rate=16.0, sun=4.75),
    dict(code="KS", name="Kansas", slug="kansas", rate=15.3, sun=5.39),
    dict(code="KY", name="Kentucky", slug="kentucky", rate=13.8, sun=4.79),
    dict(code="LA", name="Louisiana", slug="louisiana", rate=12.7, sun=5.32),
    dict(code="ME", name="Maine", slug="maine", rate=32.4, sun=4.55),
    dict(code="MD", name="Maryland", slug="maryland", rate=21.4, sun=4.88),
    dict(code="MA", name="Massachusetts", slug="massachusetts", rate=30.5, sun=4.7),
    dict(code="MI", name="Michigan", slug="michigan", rate=23.1, sun=4.47),
    dict(code="MN", name="Minnesota", slug="minnesota", rate=17.4, sun=4.61),
    dict(code="MS", name="Mississippi", slug="mississippi", rate=14.5, sun=5.26),
    dict(code="MO", name="Missouri", slug="missouri", rate=16.1, sun=5.03),
    dict(code="MT", name="Montana", slug="montana", rate=15.0, sun=4.76),
    dict(code="NE", name="Nebraska", slug="nebraska", rate=13.8, sun=4.98),
    dict(code="NV", name="Nevada", slug="nevada", rate=12.8, sun=6.41),
    dict(code="NH", name="New Hampshire", slug="new-hampshire", rate=26.6, sun=4.58),
    dict(code="NJ", name="New Jersey", slug="new-jersey", rate=25.2, sun=4.66),
    dict(code="NM", name="New Mexico", slug="new-mexico", rate=16.1, sun=6.42),
    dict(code="NY", name="New York", slug="new-york", rate=29.9, sun=4.5),
    dict(code="NC", name="North Carolina", slug="north-carolina", rate=15.2, sun=5.25),
    dict(code="ND", name="North Dakota", slug="north-dakota", rate=13.4, sun=4.45),
    dict(code="OH", name="Ohio", slug="ohio", rate=19.4, sun=4.54),
    dict(code="OK", name="Oklahoma", slug="oklahoma", rate=14.3, sun=5.5),
    dict(code="OR", name="Oregon", slug="oregon", rate=16.0, sun=4.06),
    dict(code="PA", name="Pennsylvania", slug="pennsylvania", rate=21.7, sun=4.79),
    dict(code="RI", name="Rhode Island", slug="rhode-island", rate=28.3, sun=4.7),
    dict(code="SC", name="South Carolina", slug="south-carolina", rate=15.5, sun=5.33),
    dict(code="SD", name="South Dakota", slug="south-dakota", rate=15.4, sun=4.86),
    dict(code="TN", name="Tennessee", slug="tennessee", rate=13.7, sun=4.82),
    dict(code="TX", name="Texas", slug="texas", rate=15.9, sun=5.22),
    dict(code="UT", name="Utah", slug="utah", rate=13.1, sun=5.39),
    dict(code="VT", name="Vermont", slug="vermont", rate=23.8, sun=4.36),
    dict(code="VA", name="Virginia", slug="virginia", rate=17.6, sun=5.01),
    dict(code="WA", name="Washington", slug="washington", rate=14.7, sun=3.95),
    dict(code="DC", name="Washington, DC", slug="washington-dc", rate=25.2, sun=4.9),
    dict(code="WV", name="West Virginia", slug="west-virginia", rate=15.8, sun=4.57),
    dict(code="WI", name="Wisconsin", slug="wisconsin", rate=19.1, sun=4.58),
    dict(code="WY", name="Wyoming", slug="wyoming", rate=14.4, sun=5.36),
]

RATE_SOURCE = "US Energy Information Administration (EIA), Electric Power Monthly, residential average price, July 2026"
SUN_SOURCE = "NREL PVWatts / NSRDB, average peak sun hours for each state's largest city"

COST_PER_WATT = 3.00   # midpoint: EnergySage H1 2026 ~$2.60/W, SEIA/Wood Mackenzie Q3 2026 $3.36/W
EXPORT_FACTOR = 0.85   # haircut for self-consumption vs. export credit differences
BATTERY = {"low": 900, "high": 1300}  # $/kWh installed; EnergySage H1 2026 avg ~$15,647 for 13.5 kWh

PLUGIN = {
    "UT": "Legal. Utah's HB 340 (2025) was the first US plug-in solar law: up to 1,200 W into a standard 120 V outlet, certified equipment with anti-islanding protection, no interconnection application.",
    "ME": "Legal. Maine's LD 1730 (signed April 2026) allows up to 1,200 W; you can self-install up to 420 W, while 420–1,200 W needs an electrician.",
    "VA": "Legal. Virginia's HB 395 / SB 250 allows plug-in systems up to 1,200 W, effective July 1, 2026.",
    "CO": "Legal from January 1, 2027. Colorado's HB 26-1007 allows up to 1,920 W per meter.",
    "MD": "Legal. Maryland's HB 1532 (May 2026) allows plug-in systems up to 1,200 W.",
    "CT": "Legal. Connecticut's HB 5340 (May 2026) allows plug-in systems up to 1,200 W.",
    "NH": "Legal. New Hampshire's SB 540 (2026) allows plug-in systems up to 1,200 W.",
    "VT": "Legal. Vermont's S.202 (June 2026) allows plug-in systems up to 1,200 W.",
    "NJ": "Legal from March 1, 2027. New Jersey's S2368 / A4836 allows up to 1,200 W; devices of 400 W or less are exempt from some code requirements.",
    "CA": "Legal from January 1, 2027. California's SB 868 (signed September 30, 2026) allows up to 1,200 W AC per dwelling.",
    "NY": "Pending. New York's SUNNY Act (1,200 W) passed the legislature and was awaiting the governor's signature as of October 2026.",
}
POLICY = {
    "SC": 'South Carolina offers a state income tax credit of 25% of system cost, up to $35,000 (applied over several years). Check DSIRE for current rules.',
    "NY": 'New York offers a 25% state tax credit up to $5,000, plus NY-Sun rebates of roughly $0.15–0.35 per watt depending on region.',
    "HI": 'Hawaii offers a 35% state tax credit, capped at $5,000 per system.',
    "NM": 'New Mexico offers a 10% state tax credit, up to $6,000.',
    "UT": 'Utah offers a state tax credit of 25%, capped at $1,600 and stepping down over time.',
    "MA": 'Massachusetts offers a 15% state tax credit up to $1,000, plus SMART program payments for solar production.',
    "AZ": 'Arizona offers a 25% state tax credit, up to $1,000.',
    "MD": 'Maryland offers a $1,000 residential clean energy grant, subject to funding.',
    "CA": 'California has no state tax credit, but SGIP rebates of roughly $150–200 per kWh can cut battery costs. Most utilities use net billing (NEM 3.0), which makes batteries more valuable.',
}

PLUGIN_DEFAULT = "No dedicated plug-in solar law yet as of October 2026. Ask your utility before connecting anything to an outlet; most require an interconnection application. Over 30 states have considered bills, so check back."
POLICY_DEFAULT = "No major statewide solar tax credit as of October 2026. Many states exempt solar from property or sales tax, and some utilities offer rebates. Search DSIRE (dsireusa.org) for your ZIP code."

for _s in STATES:
    if _s["code"] in PLUGIN: _s["plugin"] = PLUGIN[_s["code"]]
    if _s["code"] in POLICY: _s["policy"] = POLICY[_s["code"]]

GUIDE_CATS = [
    ("start", "Getting started", "What solar is, whether it pays, and whether your roof is ready."),
    ("money", "Cost, incentives and quotes", "Prices, incentives, financing and how to compare installers."),
    ("batteries", "Batteries and backup", "Home batteries and keeping the lights on in an outage."),
    ("portable", "Plug-in, portable and off-grid", "Solar for renters, balconies, RVs, vans and cabins."),
    ("living", "Living with solar", "Maintenance, winter performance and selling a solar home."),
]
GUIDE_ORDER = ["is-solar-worth-it", "solar-cost", "solar-incentives", "plug-in-balcony-solar", "how-solar-works",
    "home-batteries-explained", "solar-for-renters", "portable-power-stations", "buy-lease-loan-ppa", "net-metering-explained",
    "solar-quote-checklist", "choosing-an-installer", "roof-and-solar", "solar-panel-types", "power-outage-backup",
    "rv-van-solar", "off-grid-basics", "solar-in-winter", "solar-maintenance-cleaning", "selling-home-with-solar"]

# Every ID verified via YouTube oEmbed on Oct 22, 2026.
VIDEOS = [
    dict(id="xKxrkht7CpY", title="How do solar panels work?", channel="TED-Ed", why="the clearest five-minute start", topics=["how", "types"]),
    dict(id="0elhIcPVtKE", title="Energy 101: Solar PV", channel="U.S. Department of Energy", why="official, short primer", topics=["how"]),
    dict(id="TUGRWepCH90", title="Are solar panels worth it?", channel="Undecided with Matt Ferrell", why="real bills from a real home", topics=["worth"]),
    dict(id="Yxt72aDjFgY", title="How solar panels work", channel="The Engineering Mindset", why="animated look inside a cell", topics=["how", "types"]),
    dict(id="9SQuES3M-B8", title="What is net metering?", channel="EnergySage", why="how exports become bill credits", topics=["netmeter", "worth"]),
    dict(id="YrO9TArSK6o", title="The hidden problem with home batteries", channel="Undecided with Matt Ferrell", why="when a battery pays and when it doesn't", topics=["battery"]),
    dict(id="g3_YAZvX42A", title="The unexpected genius of apartment solar", channel="Undecided with Matt Ferrell", why="balcony solar, explained", topics=["plugin"]),
    dict(id="jxt3v7kTlvw", title="4-year update: are home solar panels still worth it?", channel="Undecided with Matt Ferrell", why="long-term real-world results", topics=["worth"]),
    dict(id="adFGmOlDM-Y", title="Beginner and budget-friendly DIY solar system", channel="DIY Solar Power with Will Prowse", why="a first off-grid build", topics=["portable"]),
    dict(id="_xhyAyChumw", title="5 ways portable power stations outshine gas generators", channel="Bailey Line Road", why="RV and camping perspective", topics=["portable", "battery"]),
    dict(id="kriIXJkoyBs", title="The hidden problem with the world's most efficient solar panel", channel="Undecided with Matt Ferrell", why="what efficiency really means", topics=["types"]),
    dict(id="IAr53ohY3w4", title="What to expect during your solar installation", channel="All Energy Solar", why="install day, step by step", topics=["install"]),
    dict(id="zsjhD1InL64", title="What I learned after 1 year with new solar panels", channel="Undecided with Matt Ferrell", why="first-year lessons", topics=["worth", "install"]),
    dict(id="R3eEzdpi12I", title="Why Australia's solar is so cheap", channel="Undecided with Matt Ferrell", why="why soft costs drive US prices", topics=["worth"]),
    dict(id="9SQuES3M-B8", title="Net metering, explained", channel="EnergySage", why="exports and credits", topics=["netmeter"]),
]
VIDEOS = [v for i, v in enumerate(VIDEOS) if v["id"] not in [x["id"] for x in VIDEOS[:i]]]
