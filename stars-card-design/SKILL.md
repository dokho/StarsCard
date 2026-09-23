---
name: stars-card-design
description: Create finished, standard-size sports trading cards from a user-provided athlete photo and player information. Use when a user asks to 制作球星卡, generate a player card, turn a photo into a sports card, choose a card style, create a front/back card, design card templates, or build a reusable sports-card style system. Do not use for card pricing, grading, authentication, or investment advice.
---

# Stars Card Design

Guide the user from an athlete photo to a finished, original sports card. Collect only the information needed at each stage, confirm the design once, then produce the card instead of stopping at a prompt or concept.

## Workflow

### 1. Collect the source photo and player data

If the user has not attached an athlete photo, ask them to upload one. The photo is required for a finished card. Request the following information in the same message so the user can answer once:

- player name — required;
- jersey number — required;
- playing position — required;
- team name — optional;
- team logo image — optional.

Accept details already present in the conversation without asking again. Do not require team name or logo. If no logo is supplied, omit it or use a simple typographic team monogram derived from a provided team name; never invent an official-looking logo.

Inspect the uploaded photo before proposing styles. Note the crop, pose, direction of movement, background quality, resolution, and whether the face is clear. Warn briefly if the source is too small, heavily blurred, obstructed, or lacks enough body area for the requested layout, and request a better photo only when the current one cannot produce an acceptable result.

### 2. Let the user choose the design

After the required photo and player data are available, offer a compact set of suitable choices based on the actual image. Include:

- 6 recommended style choices, each with a one-line visual description;
- an explicit “查看更多风格” option that opens the full catalog;
- portrait or landscape;
- front only or front and back.

Use original generic style names. Good defaults are:

- **赛场瞬间** — full-bleed photography with restrained match graphics;
- **锋芒竞技** — sharp geometry, team-color light, metallic depth;
- **复古档案** — warm paper, limited inks, season-record typography;
- **城市主场** — player plus original local symbols and fan culture;
- **热血英雄** — original comic illustration and strong motion energy;
- **荣耀典藏** — premium spacing, ceremonial symmetry, restrained foil.

Style names are selection labels only. Never print the selected style name on the finished front or back unless the user explicitly requests it as visible copy.

Read [references/style-catalog.md](references/style-catalog.md) before recommending styles. Match recommendations to the photo, sport, age group, and intended mood instead of always showing the same six defaults. If the user asks for more choices, show the full catalog grouped by category; do not make them repeatedly ask for another batch.

Read [references/style-system.md](references/style-system.md) when the user requests comparisons, rarity variants, prompt details, or a reusable template system.

If the user selects a card back, ask only for missing back-specific content that materially matters: a short bio, season statistics, achievement, motto, or social/contact field. These fields are optional. Never fabricate statistics, awards, dates, or biographical facts; a back can use identity data, decorative structure, and clearly labeled empty/omitted fields.

### 3. Confirm once

Before generating, summarize the exact choices in a compact production brief:

- player name / number / position;
- team and logo usage;
- chosen style;
- portrait or landscape;
- front only or front and back;
- any optional back content.

Ask for confirmation only when the user has not already clearly approved all choices. Do not repeatedly reconfirm details after production starts.

### 4. Produce the card

Read [references/production-workflow.md](references/production-workflow.md) before creating final artwork.

Use the athlete photo as a reference and preserve recognizable facial features, body proportions, uniform details, skin tone, and jersey number unless the user explicitly asks for stylization. Build the visual artwork first, then place exact text and the supplied logo in a deterministic layout step. Do not rely on an image generator to spell the player name, number, position, statistics, or team name.

Use a standard 2.5 × 3.5 inch trading-card trim size:

- portrait master: **1500 × 2100 px**;
- landscape master: **2100 × 1500 px**.

For print-ready output, also support a 0.125 inch bleed on every side at 600 ppi:

- portrait with bleed: **1650 × 2250 px**;
- landscape with bleed: **2250 × 1650 px**.

Keep essential faces, names, numbers, and logos inside the safe area defined in the production reference. When a back is requested, create a separate file at the same orientation and dimensions, plus a side-by-side preview when practical.

Keep the back visually neutral and shared across style variants. Do not echo the front's distinctive frame, finish, illustration language, style name, or rarity treatment on the back. A viewer should not be able to identify which front style is paired with the card by looking at the back alone. When several front variants belong to the same player or set, reuse one common back unless the user explicitly requests variant-specific backs.

### 5. Verify and deliver

Before presenting the result, visually check:

- likeness and face integrity;
- exact spelling of every supplied field;
- correct number and position;
- logo aspect ratio and legibility;
- orientation and pixel dimensions;
- text contrast and safe margins;
- front/back consistency;
- no visible style-selection label on either side;
- back remains neutral and does not reveal the front variant;
- absence of unintended trademarks or fake certification claims.

Deliver the final PNG file or files inline when the environment supports it. State the dimensions and identify front/back clearly. If a requested generation or editing tool is unavailable, provide a production-ready prompt and layout specification, explicitly noting that no final bitmap was produced.

## Originality and rights

Learn from broad card conventions without recreating recognizable commercial borders, proprietary patterns, insert names, logo placements, or complete compositions. Keep user-provided trademarks confined to the authorized card.

Do not fabricate authenticated autographs, game-used memorabilia, serial numbering, or licensing claims. Decorative handwriting and digital keepsake windows must be described honestly.
