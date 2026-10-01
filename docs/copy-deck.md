# Quantum Karate site: copy deck (LOCKED 2026-09-27, claims-approved by V-Nat 3)

**Scope:** every user-visible string on `index.html`, `seduma.html`, `facts.html`, and `contact.html`, verbatim, including `<title>`, meta descriptions, and accessible names (`aria-label`).
**Claims authority:** `docs/SAFE_PUBLIC_NARRATIVE.md` on Seduma `main` (read 2026-09-27), cited below as **SP** plus the section or numbered sentence. The other sources are the locked strings in the brief and the locked copy decks `guided/uniqueness-copy-deck.md` (**UCD**) and `guided/first-run-copy-deck.md` (**FRCD**). Company lines taken from Chris's brief are marked **BRIEF**.
**Typography:** all apostrophes are curly (’). The em dashes (—) are part of the locked strings. `P&L` is written `P&amp;L` in the HTML source.
**Banned-term grep (HTML):** zero matches for `NAE`, `N.A.E`, `LLC`, `Inc`, `autopilot`, `set-and-forget`, `autonomous`, `return`, `profit`. A case-insensitive `inc` search finds only "including" (index.html: "Plain facts, including the limits."), which has nothing to do with a legal suffix.

---

## Global (every page)

| Slot | Copy |
|---|---|
| Skip link | Skip to content |
| Wordmark | Quantum Karate™ |
| Primary nav (`aria-label="Primary"`) | Home · Seduma™ · Facts · Contact |
| Footer wordmark + tag | Quantum Karate™ / Precision is Power |
| Footer nav (`aria-label="Footer"`) label | Pages |
| Footer nav | Home · Seduma™ · Facts · Contact |
| Footer disclaimer label | Disclaimer |
| Footer disclaimer | Seduma is not a broker or an investment adviser. It does not pick, recommend, or generate trades. Practice fills are simulated — they are not live fills. Paper/Practice P&L is not a promise of live results. Not investment advice. |
| Footer base left | © 2026 Quantum Karate *(deck historical; live HTML has no © line until LLC exists — see Addendum 2026-09-30)* |
| Footer base right | Master the smallest details. Create the biggest impact. |
| Console captions (every product visual) | Illustrative console view. |

---

## 1. Home: `index.html`

- **Title:** Quantum Karate™ — Precision is Power
- **Meta description:** Quantum Karate™ builds precise, disciplined technology. Our first product is Seduma™: Paper-first practice for trading rules you bring.

**Hero**
- Eyebrow: Quantum Karate™
- H1 (display, two lines): Precision / is Power
- Sub: Master the smallest details. Create the biggest impact.
- Buttons: Meet Seduma → · What Seduma is and isn’t

**01 Philosophy**
- Index: 01 Philosophy
- H2: Small decisions, made exactly.
- Lead: Quantum Karate™ builds technology the way a martial artist trains: with precision, discipline, and attention to the smallest detail.
- Pillar 01, Precision: The small details are the work, not the afterthought. We get them right before we call anything done.
- Pillar 02, Discipline: Clear defaults, clear limits, no shortcuts. We would rather do less, exactly, than more, loosely.
- Pillar 03, Advanced technology: Serious engineering, explained in plain words. If a term needs defining, we define it.

**02 Our first product** (the only cyan on Home)
- Index: 02 Our first product
- Eyebrow: Seduma™ · chip: Honest Practice
- H2: Seduma™: practice first, on your terms.
- P1: Seduma is a Paper-first, strategy-free runtime — software that runs trading rules you bring. It does not pick, recommend, or generate trades.
- P2: **Practice** (also called **Paper**) is the default: orders get simulated fills, and no real money moves. **Live** — real orders with real money — stays off until you choose it yourself.
- Buttons: Explore Seduma → · What it is and isn’t
- Mini console (`aria-label`): Illustrative Seduma status view: Practice mode, Live: Off, Emergency stop available, Last audit, and Simulated fills ≠ live.
  - Bar: Seduma · Paper Practice
  - Cards: Practice mode [chip: Practice mode] · Live election [chip: Live: Off] · Emergency stop / Emergency stop available · Audit honesty / Last audit / 14:32:08
  - Chip: Simulated fills ≠ live
  - Caption: Illustrative console view.

**03 How we talk about it**
- Index: 03 How we talk about it
- H2: We say what it doesn’t do, too.
- Lead: Plain facts, including the limits. No performance numbers and no promises of results.
- Link: Read the facts →

**04 Waitlist**
- Index: 04 Waitlist
- H2: Join the Practice waitlist.
- Lead: Get notified when Seduma™ is ready to try in Practice. No real money moves until you choose Live.
- Button: Email the waitlist → (`mailto:v-nat@outlook.com?subject=Seduma%20waitlist`)

---

## 2. Seduma: `seduma.html`

- **Title:** Seduma™ — Honest Practice | Quantum Karate™
- **Meta description:** Seduma™ is a Paper-first, strategy-free runtime from Quantum Karate™. Practice is the default. Live stays off until you choose it.

**Hero**
- Eyebrow: Seduma™ · by Quantum Karate™ · chip: Honest Practice
- H1 (named promise, two lines): We don’t fake Practice. / We don’t trade until you say so.
- Sub (front door): Seduma opens the door. The Neural Agency Engine researches. Practice protects your money until you choose Live.
- Buttons: How it works ↓ · What Seduma is and isn’t
- Definitions:
  - PRACTICE: Running your trading rules with simulated fills. No real money moves. It is the default.
  - PAPER: Another word for Practice. A broker’s own paper account is called Real paper — still not live money.
  - LIVE: Real orders with real money, through a connection you set up. Off until you elect it yourself.

**Console visual** (`aria-label`): Illustrative Seduma console. Status chips read Practice mode, Live: Off, and Honest Practice. Trust cards show Practice mode, Live election set to Live: Off, Emergency stop available, and Last audit. The Activity list, marked Simulated fills ≠ live, shows practice order states for the placeholder symbol EXAMPLE. No prices or results are shown.
- Bar: Seduma · Paper Practice · chips: Practice mode · Live: Off · Honest Practice
- Side nav: Home · Connections · Activity · Safety · foot: Live: Off · Practice default
- Banner: We don’t fake Practice. We don’t trade until you say so. · chip: Honest Practice · Practice fills are simulated — they are not live fills.
- Trust cards:
  - Practice mode · chip: Practice mode · Practice mode · Live: Off (until election). Soft locks on.
  - Live election · chip: Live: Off · Live: Off · Practice default
  - Emergency stop · Emergency stop available · button: Emergency stop
  - Audit honesty · Last audit · 14:32:08
- Activity header: Activity · chip: Simulated fills ≠ live
- Cycle line: Practice cycle complete · still Paper · Live: Off
- Rows (time · symbol · event · state):
  - 14:32:08 · EXAMPLE · Practice cycle · sample HOLD · No order
  - 14:31:52 · EXAMPLE · Practice order placed · Filled · simulated
  - 14:31:40 · EXAMPLE · Practice order sent to Practice stub · Placed
  - 14:30:12 · — · Emergency stop test · Stopped — still in Practice
- Soft locks: Practice only · Auto-trading off · Real sending off
- Caption: Illustrative console view.

**01 How it works** (`#how`)
- Index: 01 How it works
- H2: Four plain steps. Practice first.
- Lead: Seduma is strategy-free. You bring the rules. Seduma runs them in Practice by default, and nothing goes Live unless you say so.
- Step 01, Bring your rules: A strategy is the set of rules that decides when to place an order. You bring your own. Seduma does not pick, recommend, or generate trades.
- Step 02, Start in Practice: Practice is the default start. Fills are simulated and no real money moves. Your first Practice run needs no Live or real broker keys.
- Step 03, Know how to stop: Emergency stop lets you stop Practice calmly. Seduma keeps a chain-of-custody audit trail, written before any external call. / (small) Emergency stop does not close open positions.
- Step 04, Live, only if you choose: Live is optional and off by default. Finishing setup does not turn it on. To elect Live, you confirm it yourself by typing LIVE. It does not switch on by itself. / (small) Emergency stop is always available — Live does not remove it.

**First run (duo)**
- Label: First run
- H3: Setup stays Paper.
- P1: First-run setup has four steps: Welcome to Paper Practice, Safety check, Try a practice run, and You’re set — setup stays Paper.
- P2: The Safety check records that you read the Paper disclosures. It does not turn on Live. Completing setup does not turn on Live — you choose later.
- Wizard visual (`aria-label`): Illustrative first-run setup. Four steps: Welcome to Paper Practice, Safety check, Try a practice run, and You’re set — setup stays Paper. Status reads Live trading: Off · Practice default.
  - Head chips: Paper Practice · Live: Off
  - ✓ Welcome to Paper Practice: No real money · You bring or review the rules
  - ✓ Safety check: This does not turn on Live trading.
  - ✓ Try a practice run: Sample strategy: HOLD only · One Paper cycle
  - 04 You’re set — setup stays Paper: ✓ Paper Practice is ready · ✓ Kill switch and audit stay on · Live trading: Off · Practice default
  - Footer: Practice is the default. Completing setup does not turn on Live — you choose that later.
  - Caption: Illustrative console view.

**Live election (duo)**
- Label: Live election
- H3: Live is a choice, not a default.
- P1: If you ever elect Live, you confirm it yourself: check each item and type LIVE. Until you do, the button stays disabled. Cancelling keeps you in Practice.
- P2: Connecting a broker does not unlock Live, and Emergency stop is always available — Live does not remove it.
- Modal visual (`aria-label`): Illustrative Live confirm dialog titled Turn on Live trading. Three unchecked items, an empty field asking you to type LIVE, a Stay in Practice button, and a disabled Turn on Live button.
  - Label: Safety
  - Title: Turn on Live trading
  - Body: You’re choosing to leave Practice-only at your own will. Real money/orders may be at risk. You bring strategies & credentials. Seduma does not pick trades. Kill switch + audit stay on.
  - Checklist (unchecked): Choosing Live at my own will · Real money/orders may be at risk · Seduma does not pick trades for me
  - Field label: Type LIVE to confirm (field empty)
  - Buttons: Stay in Practice · Turn on Live (shown disabled)
  - Caption: Illustrative console view.

**02 Honest Practice** (`#honesty`)
- Index: 02 Honest Practice
- H2: Three lines we keep everywhere.
- 01 Practice fills are simulated — they are not live fills.
- 02 Paper/Practice P&L is not a promise of live results.
- 03 Emergency stop is always available — Live does not remove it.
- Note: P&L is the running gain or loss on trades. A broker’s paper account also differs from that broker’s live market, and Seduma does not paper over that.

**03 Connections** (`#connections`)
- Index: 03 Connections
- H2: Bring your own connections.
- Lead: A connection links Seduma to a trading platform you have access to. Built-in connections are conveniences, not an exclusive list. You can bring another API.
- Card, Built-in / Practice stub: First run uses the built-in Practice connection. No broker account or keys needed.
- Card, Connection type / Real paper: Broker paper account — still not live money.
- Card, Connection type / Test sandbox: Vendor/test sandbox — not the same as broker paper trading.
- Card, Connection type / Live-capable: Can send live orders only after you elect Live.
- Foot 1: Connecting does not unlock Live.
- Foot 2: Advanced: bring your own HTTP connection. Invalid settings fail closed — they stop instead of sending.
- Foot 3: Each connection is labeled Real paper, Test sandbox, or Live-capable, so you know which one you are using.

**04 Research** (`#research`)
- Index: 04 Research
- H2: Where the Neural Agency Engine fits.
- P1: The Neural Agency Engine is the research brain — not the front door. It is a separate research engine.
- P2: It does not pick trades and is not the Live switch. Seduma is the front door.

**Facts CTA**
- H2: Read the plain facts.
- Lead: What Seduma is, what it isn’t, and the words we use.
- Link: What Seduma is and isn’t →

**Waitlist CTA** (after Read the plain facts.)
- H2: Join the Practice waitlist.
- Lead: Get notified when Seduma™ is ready to try in Practice. No real money moves until you choose Live.
- Button: Email the waitlist → (`mailto:v-nat@outlook.com?subject=Seduma%20waitlist`)

---

## 3. What Seduma is and isn’t: `facts.html`

- **Title:** What Seduma™ is and isn’t | Quantum Karate™
- **Meta description:** Plain facts about Seduma™: what it is, what it isn’t, and the words we use.
- Eyebrow: Seduma™ · Facts
- H1: What Seduma™ is and isn’t
- Sub: Plain facts, in plain words, including the limits.
- Section `aria-label`: Facts

**Seduma™ is** (each item: **bold lead**, then detail. The claim IDs refer to the table below.)
1. **A Paper-first, strategy-free runtime.** Software that runs trading rules you bring, starting in Practice. *(C1, C3, C4)*
2. **Practice by default.** Paper is the default start. Lockdown is on and execution is off by default. *(C4, C5)*
3. **Built around your own strategy.** You bring the strategy — the rules that decide when to place an order. *(C3)*
4. **Live only when you elect it.** Live is available when you elect it, through a confirm-gated step. Completing setup does not turn on Live — you choose later. *(C6, C7)*
5. **Equipped with an Emergency stop.** Emergency stop is always available — Live does not remove it. *(C14)*
6. **Recorded before external calls.** Seduma keeps a chain-of-custody audit trail, written before any external call. *(C17)*
7. **Bounded by limits you set.** Risk limits are configured by you, the operator. *(C18)*
8. **Open to the connections you bring.** Named platforms are examples, not an exclusive list. You can bring another API you have access to. *(C26)*
9. **Ready to practice without broker keys.** Your first Practice run needs no Live or real broker keys. *(C19)*

**Seduma™ isn’t**
1. **A broker.** Seduma is not a broker and makes no broker-license claim. *(C28)*
2. **An investment adviser.** It makes no investment-adviser claim. It does not pick, recommend, or generate trades. *(C29, C2)*
3. **A source of strategies.** It is strategy-free. It is not a strategy marketplace. *(C1, C31)*
4. **Trading before you say so.** We don’t trade until you say so. Installing Seduma or completing setup does not place live orders. *(C32, C9)*
5. **A promise of results.** Paper/Practice P&L is not a promise of live results. Practice fills are simulated — they are not live fills. *(C12, C10)*
6. **Unlocked by connecting.** Connecting a broker or loading a connection does not unlock Live. *(C25)*
7. **An auto-close.** Emergency stop does not close open positions. *(C16)*
8. **The Neural Agency Engine.** Seduma is the front door. The Neural Agency Engine is the research brain. It does not pick trades and is not the Live switch. *(C34)*

**Machine-readable link** (below the two lists, small mono text): `Machine-readable facts: facts.json` linking to relative `facts.json` so it works on the GitHub Pages subpath and a custom domain (generated from Seduma main, mirrors /v1/facts; engineer-owned).

**Glossary**
- Index: — Glossary · H2: Words we use.
- **Practice**: Running trading rules with simulated fills. No real money moves. In Seduma, Practice is the default.
- **Paper**: Another word for Practice.
- **Real paper**: A broker’s own paper account. Still not live money.
- **Live**: Real orders with real money, sent through a connection you set up. In Seduma, Live is off until you elect it yourself.
- **Confirm-gated**: A step that stays locked until you confirm it yourself. For Live, that means checking each item and typing LIVE.
- **Fill**: The moment an order completes, and the price it completes at. In Practice, fills are simulated.
- **P&L**: The running gain or loss on trades. Paper/Practice P&L is not a promise of live results.
- **Strategy**: The rules that decide when to place an order. You bring these. Seduma does not supply them.
- **Connection**: A link from Seduma to a trading platform you have access to, labeled Real paper, Test sandbox, or Live-capable.
- **Emergency stop**: A control that lets you stop calmly. It stays available in Practice and in Live. It does not close open positions.
- **Audit trail**: A chain-of-custody record Seduma writes before it makes an external call.

---

## 4. Contact: `contact.html`

- **Title:** Contact | Quantum Karate™
- **Meta description:** Contact Quantum Karate™ about product questions, partnership, or acquisition inquiries.
- Eyebrow: Contact
- H1: Talk to Quantum Karate™.
- Sub: Reach out about product questions, partnership, or acquisition inquiries.
- Label (H2): Email
- Link: `<a href="mailto:{{CONTACT_EMAIL}}">{{CONTACT_EMAIL}} →</a>`
- Helper: Opens your own email app.
- Topic chips (`aria-label="Topics"`): Product questions · Partnership · Acquisition inquiries
- **Placeholder flag** (`aria-label="Placeholder notice"`, `data-remove-before-launch`), plus an HTML comment next to the link:
  - PLACEHOLDER — REMOVE BEFORE LAUNCH
  - Chris must supply the real contact address. Replace both instances of {{CONTACT_EMAIL}} in contact.html (the mailto: link and its visible text), then delete this note.
- No form, no backend, no phone, no location.

> ⚠️ **FLAG FOR CHRIS:** `{{CONTACT_EMAIL}}` is a placeholder. You need to supply the real address before launch. Nothing was invented.

---

## Claims table

Every factual claim on the site is listed below with its source. "SP n" means numbered sentence n under SAFE_PUBLIC "Approved sentences".

| ID | Claim as it appears on the site | Where | Source | Quoted source line |
|---|---|---|---|---|
| C1 | Seduma is a Paper-first, strategy-free runtime | Home, Seduma, Facts | SP 1 | "**Seduma is a Paper-first, strategy-free runtime.**" |
| C2 | It does not pick, recommend, or generate trades | Home, Seduma, Facts, footer | SP 1 | "Seduma does not pick, recommend, or generate trades." |
| C3 | You bring the rules / strategy; Seduma does not supply them | Home, Seduma, Facts | SP 1 | "You bring the `Strategy`." |
| C4 | Practice (Paper) is the default start | all | SP 2 | "Paper is the default start." |
| C5 | Lockdown is on and execution is off by default | Facts | SP "What this pack is" | "a Paper-first, strategy-free runtime with lockdown on and execution off by default." |
| C6 | Live is available when you elect it, through a confirm-gated step; off until you choose | Home, Seduma, Facts | SP "What this pack is" / SP 2 | "Live is available when the **user** elects it (confirm-gated)." |
| C7 | Completing / finishing setup does not turn on Live — you choose later | Seduma, Facts | SP 2 | "Completing setup does not turn on Live — you choose later." |
| C8 | You confirm Live by typing LIVE; it does not switch on by itself | Seduma, Facts glossary | SP 13 | "**Turn on Live trading…** opens the confirm modal (type **LIVE**) and does not auto-elect." |
| C9 | Installing Seduma or completing setup does not place live orders | Facts | SP "Hard ceiling" | "No live order placement from install, wizard, or Paper two-ack." |
| C10 | Practice fills are simulated — they are not live fills | all | SP 9 + locked honesty line | "**Practice fills are simulated — they are not live fills.**" |
| C11 | No real money moves in Practice | Home, Seduma, Facts | SP 13 | "Run a Paper cycle with the sample HOLD — still Practice, still no real money." |
| C12 | Paper/Practice P&L is not a promise of live results | all | SP 9 + locked honesty line | "Paper/Practice P&L is not a promise of live results." |
| C13 | A broker’s paper account differs from its live market; Seduma does not paper over that | Seduma | SP 9 | "Broker paper (Alpaca paper, IBKR paper, Tradier sandbox) also diverges from that venue’s live book; Seduma does not paper over that." |
| C14 | Emergency stop is always available — Live does not remove it | Seduma, Facts | SP 12 + locked honesty line | "Emergency stop is always available — Live does not remove it." |
| C15 | Emergency stop lets you stop Practice calmly | Seduma, Facts glossary | SP 13 | "*Confirm you can stop Practice calmly; Live does not remove this control later.*" |
| C16 | Emergency stop does not close open positions | Seduma, Facts | SP 14 | "Emergency stop does not close open positions." |
| C17 | Chain-of-custody audit trail, written before any external call | Seduma, Facts | SP 3 | "**Safety primitives are real:** kill-switch, chain-of-custody audit *before* external calls, operator-configured risk limits." |
| C18 | Risk limits are configured by you, the operator | Facts | SP 3 | "operator-configured risk limits" |
| C19 | Your first Practice run needs no Live or real broker keys | Seduma, Facts | SP 10 / SP 15 | "First Practice success needs no Live / real venue keys." |
| C20 | First run uses the built-in Practice connection (Practice stub); no broker account or keys | Seduma | SP 15 | "First-run stays the built-in **Practice stub** (no keys)." |
| C21 | Real paper: Broker paper account — still not live money | Seduma, Facts | SP 15 + UCD §3 | "Guided Alpaca Paper is **Real paper** (*Broker paper account — still not live money.*)." |
| C22 | Test sandbox: Vendor/test sandbox — not the same as broker paper trading | Seduma | UCD §3 (locked) + SP 15 | UCD: "**Test sandbox** \| Vendor/test sandbox — not the same as broker paper trading." SP 15: "undeclared fidelity is **Test sandbox**." |
| C23 | Live-capable: Can send live orders only after you elect Live | Seduma | UCD §3 (locked) | "**Live-capable** \| Can send live orders only after you elect Live." |
| C24 | Each connection is labeled Real paper, Test sandbox, or Live-capable | Seduma, Facts glossary | SP 14 | "Connections fidelity (**Real paper** / **Test sandbox** / **Live-capable**)." |
| C25 | Connecting (a broker / loading a connection) does not unlock Live | Seduma, Facts | SP 15 / SP 5 | "Connecting does not unlock Live." / "Loading an adapter does not unlock Live." |
| C26 | Built-in / named platforms are not an exclusive list; you can bring another API | Seduma, Facts | SP 5 | "Tradier / Coinbase / Kalshi are not exclusive: operators may bring another API via `SEDUMA_USER_ADAPTER_DIR` or a generic HTTP config." |
| C27 | Advanced: bring your own HTTP connection; invalid settings fail closed | Seduma | SP 15 | "**Advanced: BYO HTTP** is labeled advanced; invalid configs fail closed" |
| C28 | Seduma is not a broker; makes no broker-license claim | Facts, footer | SP "What this pack is not" + Banned list | "A SOC 2 attestation, broker license, or investment-adviser claim." / banned: "licensed-as-broker" |
| C29 | Not an investment adviser; no investment-adviser claim | Facts, footer | SP "What this pack is not" + Banned list | "…broker license, or investment-adviser claim." / banned: "we are an RIA" |
| C30 | (removed from site 2026-09-27 per claims check) We make no SOC 2 attestation claim | — | SP "What this pack is not" + Banned list | "A SOC 2 attestation…" / banned: "SOC 2 certified" |
| C31 | Not a strategy marketplace | Facts | SP 14 + Banned list | "Do not pitch returns, a marketplace, or a Live funnel." / banned: "Marketplace" |
| C32 | We don’t fake Practice. We don’t trade until you say so. (also "nothing goes Live unless you say so") | Seduma, Facts | SP 10 + locked named promise | "**We don’t fake Practice. We don’t trade until you say so.**" |
| C33 | Seduma opens the door. The Neural Agency Engine researches. Practice protects your money until you choose Live. | Seduma | SP 11 + locked front door | same, verbatim |
| C34 | The Neural Agency Engine is the research brain — not the front door; it does not pick trades and is not the Live switch; Seduma is the front door | Seduma, Facts | SP 11 | "*The Neural Agency Engine is the research brain — not the front door.*" … "The Neural Agency Engine does not pick trades and is not the Live switch." |
| C35 | The Neural Agency Engine is a separate research engine | Seduma | **BRIEF** (implied by SP 11) | Brief: "The Neural Agency Engine is the separate research engine." |
| C36 | Honest Practice (chip) | Home, Seduma | SP 10 | "Chip: **Honest Practice**." |
| C37 | First-run steps: Welcome to Paper Practice · Safety check · Try a practice run · You’re set — setup stays Paper | Seduma | SP 13 | "wizard titles stay Welcome to Paper Practice · Safety check · Try a practice run · You’re set — setup stays Paper" |
| C38 | The Safety check records that you read the Paper disclosures; it does not turn on Live | Seduma | SP "What this pack is not" | "The in-repo two-ack … is **Paper-eval only**. It records disclosure fingerprints. It does **not** elect Live." |
| C39 | Trust chrome: Practice mode · Live election · Live: Off · Emergency stop available · Audit honesty · Last audit · Simulated fills ≠ live | Home, Seduma | SP 12 + UCD §5 | "Cards: **Practice mode**; **Live election** (**Live: Off** / …); **Emergency stop** (**Emergency stop available**); **Audit honesty** (**Last audit** …). … Optional fill chip: *Simulated fills ≠ live*." |
| C40 | Sample HOLD | Seduma | SP 13 | "Run a Paper cycle with the sample HOLD" |
| C41 | Live = real orders with real money | Home, Seduma, Facts | FRCD Live modal (locked) | "Real money/orders may be at risk." |
| C42 | Live modal content (title, body, checklist, type LIVE, Stay in Practice / Turn on Live, disabled until valid, cancelling keeps you in Practice) | Seduma | FRCD "Live graduation modal" + SP 13 | "Title: Turn on Live trading" … "Primary: Turn on Live · Secondary: Stay in Practice" … "Primary disabled until valid; cancel returns to Practice." *(body/checklist trimmed; see deviations)* |
| C43 | Wizard lines: No real money · You bring or review the rules · This does not turn on Live trading. · Sample strategy: HOLD only · One Paper cycle · Paper Practice is ready · Kill switch and audit stay on · Live trading: Off · Practice default · Practice is the default. Completing setup does not turn on Live — you choose that later. | Seduma | FRCD Steps 1–4 + global footer (locked) | verbatim FRCD strings |
| C44 | Soft locks: Practice only · Auto-trading off · Real sending off; Practice cycle complete · still Paper · Live: Off; Stopped — still in Practice | Seduma | FRCD microcopy (locked) | verbatim FRCD strings |
| C45 | Practice mode · Live: Off (until election). Soft locks on. / Live: Off · Practice default | Seduma | UCD §5 (locked) | verbatim |
| C46 | Emergency stop stays available in Practice and in Live | Facts glossary | SP 12 | "Emergency stop is always available — Live does not remove it." |
| C47 | Quantum Karate is an early-stage company; philosophy of precision, discipline, advanced technology | Home | **BRIEF** | "Quantum Karate is an early-stage company. Its philosophy is precision, disciplined execution, and advanced technology." |
| C48 | Seduma is Quantum Karate’s first product ("Seduma · by Quantum Karate", "from Quantum Karate") | Home, Seduma meta | **BRIEF** | "Seduma is Quantum Karate’s first product." |
| C49 | Precision is Power / Master the smallest details. Create the biggest impact. | Home, footer | **BRIEF** (locked taglines) | verbatim |

The following are **definitions or illustration, not product claims**: Practice, Paper, Fill, P&L, and Strategy as general terms; "A connection links Seduma to a trading platform you have access to"; the console's neutral timestamps (14:32:08, and so on); the placeholder symbol EXAMPLE; and the illustrative order states (No order / Placed / Filled · simulated).

### Deviations from locked sources (need Chris's or Muse's OK)
1. **Wizard step 4 title.** SP 13 says "You’re set — setup stays Paper", but UCD and FRCD say "You’re set — Live stays off". I used the SP version because SP is the claims authority.
2. **Live modal body and checklist.** In FRCD, the body contains "…Seduma does not pick trades or run set-and-forget automation…" and checklist item 3 is "Seduma does not pick trades / set-and-forget for me". The site grep bans `set-and-forget`, so I trimmed these to "Seduma does not pick trades." and "Seduma does not pick trades for me". I also rephrased checklist item 1 as "Choosing Live at my own will".
3. **Live confirm token.** FRCD says both "type **LIVE**" and "type **REAL** to enable confirm". SP 13 says type LIVE, so I used LIVE only.
4. **"Automations"** is left out of the console side nav (FRCD nav is Home · Connections · Automations · Activity · Safety) so the visual can't be read as automation hype.
5. **Philosophy wording.** The brief's "disciplined execution" is rendered as "discipline", so it doesn't collide with trade "execution" or the banned "Execution engine" phrase.
6. **"What Seduma is and isn’t"** uses a curly apostrophe for consistency. The `/v1/human-policy` label in UCD uses a straight one.

### Claims I wanted but could not support (left out)
| Wanted | Why left out |
|---|---|
| "Self-hosted package" | Not in SAFE_PUBLIC. Only README install steps imply it. |
| "Localhost console" (`127.0.0.1:8765`) | Not in SAFE_PUBLIC. `HUMAN_CONFIRMATION.md` lists local consoles but is explicitly headed "Design direction. Not a SAFE_PUBLIC claim." |
| "Not cloud trading" | SAFE_PUBLIC only says the pack is not a "B2C mobile / multi-region AWS / Stripe-production story". That is too weak to support a "not cloud" claim. |
| "Seduma is not an execution engine / not the engine" | SAFE_PUBLIC only bans the phrase "Execution engine (as this week's SKU)". I used the supported line "Seduma is not the Neural Agency Engine" (SP 11) instead. |
| "Research workflows" as a Seduma feature | The only research feature in SP is SP 16 Research assist, which is experimental, flag-gated, and default off. I left it out rather than qualify it on a public page. |
| Human confirmation for API and agent calls (Needs your confirmation / Nothing changed.) | `HUMAN_CONFIRMATION.md` says "Not a SAFE_PUBLIC claim". |
| "Seduma does not custody your funds" / "does not give investment advice" | README only ("What Seduma is not"). Useful for acquirers, so I suggest adding them to SAFE_PUBLIC. |
| "Tamper-evident, hash-chained audit log" | README only. The site says only "chain-of-custody". |
| Win/Mac installers, "no Docker" Practice | README only. |
| Named venues (Alpaca, IBKR, Schwab, Tradier, Coinbase, Kalshi) | Supportable (SP 5 and 15) but left out on purpose: the brief asks for generic connections and no logo wall. |
| Plan tiers, billing, KYC, optional Postgres | Supportable (SP 6–8) but too technical and off-message for a public site. |
| Any company fact beyond the brief (founding year, team, location, phone) | No source. Not invented. |
| A "Research lab" link to the Neural Agency Engine | No public target URL. The Neural Agency Engine repository should not be linked publicly while IP protection is pending. |

---

## Lock addendum — 2026-09-28 (Tester fail on quantumkarate PR #1 @ f5c07d6)

**Blocking fix (seduma.html, Live election):**
- Prose is now: "If you ever elect Live, Seduma won’t turn it on until every item is checked and LIVE is typed. Cancelling keeps you in Practice." The false line about a disabled button is gone. The shipped #turn-on-live is never disabled, and the server enforces the checks and the LIVE phrase.
- Modal aria-label is now: "Illustrative Live confirm dialog titled Turn on Live trading. Three unchecked items, an empty field labeled Type LIVE, a Turn on Live button, and a Stay in Practice button."
- The drawing no longer uses disabled styling. `.mbtn--disabled` is removed and `.mbtn--primary` added. Buttons follow the shipped order: Turn on Live, then Stay in Practice.

**Illustrated UI now uses shipped strings (Practice console on main):**
- Live dialog: the intro paragraph and the "Safety" eyebrow are removed (neither is shipped). The label is "Type LIVE". Item 1 is "I am choosing Live at my own will — not Practice-only." Item 2 is "I understand real money and real orders may be at risk." Item 3 is a deliberate paraphrase, "I understand Seduma does not pick trades for me.", because the shipped text negates a banned phrase and would trip the guard.
- Console: the nav footer reads "Live trading: Off · Practice default". The Practice mode card meta reads "Practice mode — no real money". The Live election card meta reads "Practice stays Practice — Live only when you choose."
- Activity now has only two rows: "Sample strategy: HOLD only" / "One Paper cycle", and "Emergency stop" / "Stopped — still in Practice". The invented order-placed and filled rows are removed, since a HOLD cycle places no order. The aria-label was updated to match.
- Wizard: the step 1 sub is "No real money". The step 4 card reads "Kill switch + audit on".

**Other:**
- seduma.html Research: removed "It is a separate research engine."
- facts.html item 8 sub is now "Built-in connections are conveniences, not an exclusive list. You can bring another API you have access to."
- facts.html: the machine-readable link is now in the file with a relative `href="facts.json"` (small mono note below the two lists). Remove that one line if facts.json doesn't ship.
- All four pages: og:type, og:site_name, og:title, and og:description, reusing the existing locked title and meta description. No og:image or og:url yet, because both need an absolute URL.
- site.css: the internal path is removed from the header comment. Added `@media print` so revealed content always prints.
- site.js: content already in view on load is shown at once. This fixes the blank hero console at 1280×900.
- **Declined:** a "Nothing here is investment advice." footer line. "No advice" was one of the held claims Chris chose to keep off the site (no new claims).

---

## Lock addendum 2: 2026-09-28 (V-Nat 3 public / consumer-advertising review, public-copy-review-2026-09-28.md)

**Applied in the files:**
- M1. Seduma hero sub is now "In Practice, no real money moves until you choose Live."
- M2. Every "Emergency stop is always available — Live does not remove it." on the site (Step 04, the Live election prose, honesty line 03, and facts item 5) now reads "Emergency stop stays available in Practice and in Live. It does not close open positions." The honesty section heading is now "Three plain lines.", because the site wording no longer matches the product word for word. Both console aria-labels add "(does not close open positions)". The limit is not added to the drawn stop cards, because the illustrations use shipped strings only. It goes in the figcaption instead: "Illustrative console view. Emergency stop does not close open positions." (Home mini console and Seduma hero console.)
- M2c/d (checked against shipped code: docs/KILL_SWITCH.md and execution/kill_switch.py). Step 03 now reads "Emergency stop makes Seduma refuse to send new orders until you release it. It does not close open positions or cancel orders already at your broker.", followed by "Seduma keeps an audit trail: a record written before it contacts any outside service." (V-Nat 3 R2, final.) The glossary now reads "A control that makes Seduma refuse to send new orders until you release it. It stays available in Practice and in Live. It does not close open positions or cancel orders already at your broker." The facts "An auto-close." item now reads "Emergency stop does not close open positions or cancel orders already at your broker."
- M3. Step 03 and facts item 6 now read "Seduma keeps an audit trail: a record written before it contacts any outside service." The facts heading is "Recorded before outside requests." The glossary Audit trail entry is "A record Seduma writes before it contacts any outside service. It is Seduma’s own log, not an independent audit." The illustrated "Audit honesty / Last audit" card is **removed** from both consoles rather than renamed, because renaming would break the shipped-string rule. The trust grid is now 3 cards.
- M4. The facts heading is "Uses risk limits you set." The line is "You configure the risk limits."
- M5. The soft-locks row keeps only "Practice only" (a shipped string). "Auto-trading off" and "Real sending off" are removed.
- M6. The Research section now reads "The Neural Agency Engine is the research engine behind Seduma." and "It does not pick or recommend trades, and it is not the Live switch. Seduma is the front door." Facts item 8 is updated to match.
- M7 (Chris decided): no change. The footer disclaimer stays exactly as it was: no advice line and no risk line.
- M8. The facts.json line is removed. contact.html now uses v-nat@outlook.com for both the mailto link and the visible text (relayed by V-Nat 3). The placeholder comment and the "remove before launch" aside are gone.
- © line removed from all footers until the LLC exists (Chris decided).
- S1 "Sending real orders is off by default." · S2 "Seduma is not a broker." / "Seduma is not an investment adviser. It does not pick, recommend, or generate trades." · S3 "no real money" in place of "not live money" (hero Paper definition, Real paper card, glossary) · S5 "Invalid settings are designed to stop instead of sending."
- Also fixed: the glossary Confirm-gated entry is now "A step that doesn’t take effect until you confirm it yourself. For Live, Seduma won’t turn it on until every item is checked and LIVE is typed." The old "stays locked" wording had the same flaw as the disabled-button line.

**Chris decided (via V-Nat 3):** no footer advice or risk line, and the named promise stays "We don’t fake Practice. We don’t trade until you say so." on the site and in the console banner. The D1 public variant is not used.

**Kept as shipped strings in the illustrations:**
- S4. The wizard's "Kill switch + audit on" item is removed rather than renamed.
- S6. The "Simulated fills ≠ live" chip stays inside the drawings because it's the shipped chip. Aria-labels read it as "Simulated fills (not live)". To change the chip, change the product string first.

---

## Addendum 2026-09-30 — common-law ™ (DIY marketplace Step 1)

**Marks:** Seduma™ and Quantum Karate™ only (Unicode ™ / U+2122). Never ®.

**Placement policy (brand chrome only — do not spam every prose mention):**
- **Quantum Karate™:** header/footer wordmarks; home hero eyebrow; contact H1; document `<title>` / matching `og:title` where the company name is the brand; `og:site_name` on all four pages; first company-name occurrence in meta / og descriptions; Seduma page hero eyebrow (`Seduma™ · by Quantum Karate™`); home philosophy lead first word.
- **Seduma™:** home product section eyebrow + H2; home meta / og description first product mention; Seduma / Facts titles and meta (first Seduma); Facts eyebrow, H1, and column heads (`Seduma™ is` / `Seduma™ isn’t`); primary nav + footer nav product link text on all four pages.
- **Do not mark:** named promise (`We don’t fake Practice. We don’t trade until you say so.` — hero H1 + console banner); footer disclaimer (any word); illustrated console chrome / aria-labels (shipped-app UI mirrors); CTA button / link text (`Meet Seduma`, `Explore Seduma`, `What Seduma is and isn’t`, etc.); running body prose / glossary / steps / honesty / Live dialog after the brand chrome above; CSS/JS.

**Footer disclaimer synced to live HTML (Chris via V-Nat 1):** now ends with `Not investment advice.` Deck Global row updated to match. Exact disclaimer (HTML uses `P&amp;L`):
`Seduma is not a broker or an investment adviser. It does not pick, recommend, or generate trades. Practice fills are simulated — they are not live fills. Paper/Practice P&L is not a promise of live results. Not investment advice.`
Do **not** insert ™ inside the disclaimer.

**© line:** live HTML footers still have no © (until LLC exists; Chris decided in Lock addendum 2). Deck Global still lists the historical © row with a note — do not re-add © to HTML.

**Claims:** otherwise unchanged (SAFE_PUBLIC / approved wording). V-Nat 3 re-reviews ™ only if anything else drifted.


---

## Addendum 2026-09-30b — Practice waitlist CTA (DIY marketplace)

**Channel:** `mailto:v-nat@outlook.com?subject=Seduma%20waitlist` (opens the visitor’s email app). No form unless Chris picks one later.

**Placement**
- `index.html`: new section **04 Waitlist**, after the “How we talk about it” facts band, before `</main>`.
- `seduma.html`: new band section after “Read the plain facts.”, before `</main>` (no section index number; matches the facts CTA band pattern).

**Locked strings (both pages)**
- H2: Join the Practice waitlist.
- Lead: Get notified when Seduma™ is ready to try in Practice. No real money moves until you choose Live.
- Button: Email the waitlist →
- `href`: `mailto:v-nat@outlook.com?subject=Seduma%20waitlist`
- Home-only index label: `04` / `Waitlist`

**Ceiling:** no new product claims; named promise untouched; footer disclaimer untouched (still ends with Not investment advice.). Does not promise launch dates, results, or Live access.


---

## Addendum 2026-10-01 — scrub personal GitHub handle from public site copy

**Ask (Chris via Grok Bot):** remove the personal GitHub handle from live-site copy; company site is `Quantum-Karate/website` → https://quantum-karate.github.io/website/. Keep Quantum Karate™ / Seduma™ branding.

**Applied:** claims-authority line no longer names a personal GitHub owner; it cites Seduma `main` only. Public HTML pages (`index` / `seduma` / `facts` / `contact`) had no personal-handle hits.

**Flagged for engineering (not Muse copy):** repo README temporary address + DNS still reference the personal `*.github.io` host; the old personal Pages home URL for this site still returns HTTP 200 and should be disabled or redirected to https://quantum-karate.github.io/website/.
