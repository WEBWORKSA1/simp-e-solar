/* Simple.solar site configuration.
   Payments: paste a PayPal donate link, Stripe Payment Link or Buy Me a Coffee URL to switch the
   Support page from pledge mode to instant checkout. Leave blank to keep pledge mode.
   Ad slots: after AdSense approval, create display units and paste their slot IDs below to place
   manual units in the reserved spots. Auto ads work without any slot IDs. */
window.SITE = {
  name: "Simple.solar",
  domain: "simple.solar",
  ownerContactUrl: "https://web.works/contact",
  adsenseClient: "ca-pub-6620975821265271",
  adSlots: {
    top: "",      // e.g. "1234567890"
    inArticle: "",
    sidebar: "",
    bottom: ""
  },
  payments: {
    paypal: "",
    stripe: "",
    buymeacoffee: ""
  },
  /* Form relay key (encoded). Keep it encoded — never paste a plain address anywhere on the site. */
  _k: ["MWFza3Jvd2Jldw==", "bW9jLmxpYW1n"]
};
