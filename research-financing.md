# Acorn Finance research notes (24 November 2026)

Internal notes for the Highland Construction site. Highland has not signed up as an Acorn contractor/dealer as far as we know. The live site therefore links homeowners to Acorn’s public apply page, not a personalized partner link. Swap that URL after Highland has a portal account (see `ACORN_FINANCING_URL` in `script.js`).

## What Acorn is

Acorn Finance (Headway Sales Inc. dba Acorn Finance) is a lending *marketplace*, not a lender. Homeowners check loan offers from Acorn’s lending partners. Acorn’s own site states: “The operator of this website is not a lender and does not make loans or credit decisions.”

- Home: https://www.acornfinance.com/
- Contractor page: https://www.acornfinance.com/contractors/
- FAQ (homeowner-facing marketplace language): https://www.acornfinance.com/faq/
- Dealer agreement: https://www.acornfinance.com/dealer-agreement/

## How contractors sign up

Acorn’s contractor FAQ: “Click the ‘Sign Up’ button, fill out our quick online form, and start offering financing instantly.” They work with licensed contractors in good standing and “will verify your business credentials” during onboarding. Signup is described as free (no setup cost, no monthly / dealer fees; Acorn is paid by lenders when loans originate).

**Signup URL:** https://sign-up.acornfinance.com/#/  
(Also linked as “Sign up now” from https://www.acornfinance.com/ and https://www.acornfinance.com/contractors/)

After registration, contractors log in at **https://my.acornfinance.com/** to get:

- A shareable / personalized financing link (also shareable by text, email, or QR code)
- Marketing tools
- A payment calculator
- Customer application statuses

That post-signup path is confirmed on the contractor thank-you page: https://www.acornfinance.com/contractors/thank-you/

There is also a contractor app surface at https://pro.acornfinance.com/ (sign in with portal credentials).

## Personalized partner link, widget, and badges

Yes — once a contractor is in the portal:

1. **Personalized financing link** unique to the business, for texts, emails, estimates, and the website. (Contractor page, steps 2–3; thank-you page; homepage.)
2. **Website banner / widget.** “How to Add Financing to Your Website” (updated 8 July 2026): log in to the Acorn portal, copy the banner embed code, and paste it into the site. https://www.acornfinance.com/contractor-resources/how-to-add-financing-to-your-website/
3. **Financing landing page.** Same article: in the portal, click “Copy your financing page,” then add that link to the website navigation.
4. **Marketing materials.** The contractor page offers “free-to-use advertising resources” and “advertising and marketing materials customized to your brand” in the portal.

Until Highland has a portal account, we must not embed a banner or use a dealer-coded apply URL (some Acorn marketing pages append `?d=…` codes that would attribute a lead to someone else). Use the public apply page with no dealer id:

**Public homeowner apply page:** https://your.acornfinance.com/apply/  
Title: “Apply For a Personal Loan Online: Acorn Finance” (HTTP 200). This same apply host is linked from acornfinance.com. Returning borrowers can also use https://your.acornfinance.com/access-offers.

## Logos and promotional materials — what Acorn requires

The Dealer Agreement (https://www.acornfinance.com/dealer-agreement/), section 4:

- **4.1 Promotional Materials:** “Dealer may use Promotional Materials only if provided, or approved in advance, by Acorn.”
- **4.2 Consumer Financing:** Dealer will not make representations on Acorn’s behalf. Questions about Acorn, loan products, or the application process must be referred to Acorn. Do not promise or predict that a lender will or will not approve an application. Do not represent Highland or Acorn as a lender or broker. Do not say Acorn is the exclusive source of funding, or that Acorn displays all available options. Do not complete a consumer loan application for the customer. The consumer is not obligated to use the dealer if they obtain financing.
- **4.4:** Do not infringe Acorn’s intellectual property or misuse promotional materials.

Because Highland is not yet a dealer and we do not have portal-approved badges, the site uses a **text mention only** — no Acorn logo, badge, or unofficial widget.

## Public wording we can use (and limits)

Acorn states publicly that checking / prequalifying for offers does not impact a credit score (soft check). A hard inquiry happens if the customer chooses an offer and proceeds with a lender.

Examples (paraphrase carefully; do not invent numbers on the site):

- Homepage: “No credit score impact when checking offers. Clients receive pre-qualified offers without any impact to their credit scores in a few minutes.”
- Homepage FAQ: “Will checking loan offers hurt my customer's credit? No. Checking offers through Acorn Finance does not impact your customer's credit score. Some lenders will conduct a ‘hard pull’ on your customer's credit score as part of the loan approval process.”
- Contractor FAQ: “Prequalification is a soft credit check and will not impact their score. A hard inquiry is only performed once they choose and proceed with a lender.”
- FAQ: “Acorn Finance is an online lending marketplace where you can easily compare rates and monthly payments from different lenders without impacting your credit score.”

Acorn also publishes loan-size and term ranges, example APRs, and funding-time claims on contractor/marketing pages. **Do not invent APRs, monthly payments, terms, or approval claims on the Highland site.** If we mention those later, quote Acorn and keep the footnotes. Offers are subject to credit approval and are provided by lending partners, not by Highland.

Recommended on-site disclaimer (combines Acorn’s “not a lender” stance with the required subject-to-credit language):

> Checking offers through Acorn Finance does not impact your credit score. If you choose an offer and continue with a lender, that lender may perform a hard credit inquiry, which could affect your score. Offers are provided by Acorn Finance’s lending partners and are subject to credit approval. Highland Construction is not a lender or a broker, and checking offers does not guarantee approval.

Acorn customer support listed on contractor materials: 916-404-1982, support@acornfinance.com.

## What we could not verify

- Whether Highland already has a silent/unfinished Acorn account (none is in this repo; treat as not signed up).
- The exact format of a personalized partner URL (portal-only; typically issued after signup).
- Whether official badges are downloadable without logging in (public site points to portal materials; 4.1 requires Acorn-provided or pre-approved assets).
- Current APRs or payment examples as of this date — not used on the site.
