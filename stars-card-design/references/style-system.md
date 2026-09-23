# Sports-card style system

Use this reference when a task needs visual archetype selection, prompt construction, or a reusable template/rarity system.

## Archetypes

| Archetype | Visual language | Best use | Common failure |
|---|---|---|---|
| Annual base card | Clear sports photography, stable nameplate, team and year data | Large team or season sets | Generic layout with no story |
| Full-bleed stadium | Cinematic action photo, minimal corner typography | Emotional match moments | Text obscures the photograph |
| Competitive chrome | Sharp geometry, metallic depth, speed lines, luminous edge | Modern base and rookie cards | Too many flares and frames |
| Spectrum parallel | Stable layout with controlled color/material variants | Rarity ladders | Hue swaps with no rarity meaning |
| Archival retro | Warm stock, limited colors, halftone, old editorial type | Youth history and anniversary cards | Excessive distressing reduces clarity |
| Minimal premium | Large quiet field, one portrait, tiny labels, restrained metal accent | MVP, retirement, honor cards | Generic black-and-gold luxury styling |
| Color energy | Pale field with directed powder, ink, or spectral energy | Breakout and high-impact moments | Random splashes obscure silhouette |
| Hero comic | Original illustration, exaggerated action, motion marks | Youth and fan-focused special cards | Imitating a known insert or superhero |
| Local story | Athlete plus original city, food, landscape, and fan-culture symbols | Home-team and hometown editions | Background symbols overwhelm player |
| Geometric glass | Jewel colors, dark dividing lines, emblematic symmetry | Rare ceremonial inserts | Copying a recognizable stained-glass pattern |
| Auto/memorabilia | Signature or keepsake zone, serial field, certification hierarchy | User-supplied signature and memento cards | False authenticity or game-used claim |
| Acetate/booklet | Transparent layers, suspended subject, unfolding narrative | Digital motion or multi-moment stories | Novelty harms name and face legibility |

Commercial lines such as Topps Flagship/Chrome/Heritage/Stadium Club, Panini Prizm/Color Blast/Kaboom/Downtown, and Upper Deck Clear Cut are research references only. Never use their names as the output's style name or reconstruct their card face.

## Composition patterns

### Photo-led

- Subject occupies roughly 65–85% of card height.
- Place text in natural negative space or a controlled tonal fade.
- Use one visual climax and keep badges subordinate.
- Landscape works well for diving, swinging, dunking, celebrating, and multi-player moments.

### Competitive badge

- Choose one geometric family: cut corners, circular orbit, or track lines.
- Let the shared frame identify the series and the photograph identify the athlete.
- A rare version should change material, depth, or silhouette—not only color.

### Archival

- Use warm white rather than bright digital white.
- Limit the palette to two to four inks.
- Add fields with archival meaning: season, debut date, hometown, role, or achievement.
- Preserve facial clarity even when using grain, halftone, or registration offset.

### Illustrated story

- Write the card's story in one sentence before choosing imagery.
- Limit background symbols to three to five meaningful items.
- Preserve a readable silhouette at thumbnail scale.
- Keep an intentionally calm zone for the name and number.

### Honor edition

- Use an axis, emblem, or restrained symmetry for ceremony.
- Apply metallic accent to one hierarchy level only.
- Label digital keepsake windows accurately; do not imply physical memorabilia.

## Suggested product taxonomy

### Skeleton — choose one

- `photo`: full-bleed competition photography.
- `badge`: structured geometric frame.
- `archive`: retro editorial record.
- `illustration`: original narrative artwork.
- `honor`: ceremonial premium composition.

### Finish — choose zero or one

- `chrome`: metallic surface and controlled diffraction.
- `spectrum`: rainbow refraction or energetic color.
- `matte`: uncoated paper and soft ink.
- `acetate`: translucent stacked layers.
- `foil`: restrained metallic accent.
- `canvas`: tactile print grain.

### Story — choose zero or one

- `debut`
- `home_city`
- `champion`
- `clutch`
- `team_soul`
- `milestone`

## Rarity ladder

| Tier | Structural change | Finish change | Information change |
|---|---|---|---|
| Base | Standard frame | Paper or neutral gloss | Core identity |
| Special | Controlled break-out | Spectrum or canvas | Theme title |
| Limited | Distinct frame | Foil or acetate | Honest edition number |
| Unique | Bespoke composition | Combined finish | Unique commemorative copy |

Color must never be the only rarity indicator. Add a label, icon, material change, or layout change.

## Prompt vocabulary

Use generic visual language instead of commercial style names.

**Composition:** `full-bleed sports photography`, `centered hero portrait`, `low-angle action shot`, `asymmetric editorial layout`, `badge-based composition`, `quiet lower nameplate`, `large jersey number as background typography`.

**Finish:** `chromium metallic finish`, `subtle rainbow diffraction`, `matte vintage cardstock`, `embossed foil accents`, `transparent acetate layers`, `canvas paper grain`, `spot gloss`.

**Mood:** `stadium spotlight`, `directed color powder energy`, `archival season record`, `original local city iconography`, `championship ceremony`, `comic motion energy`, `museum-like restraint`.

**Negative constraints:** `no existing trading-card logos`, `no league trademarks`, `no copied card borders`, `no fake autograph`, `no unreadable microtext`, `no excessive lens flare`, `no cluttered background`.

## Stable data model

```ts
type CardDesign = {
  skeleton: 'photo' | 'badge' | 'archive' | 'illustration' | 'honor'
  finish: 'none' | 'chrome' | 'spectrum' | 'matte' | 'acetate' | 'foil' | 'canvas'
  story: 'debut' | 'home_city' | 'champion' | 'clutch' | 'team_soul' | 'milestone'
  rarity: 'base' | 'special' | 'limited' | 'unique'
  palette: [string, string, string]
  textContrast: 'light' | 'dark'
}
```

Keep athlete content separate from `CardDesign`. A visual template should accept structured player data instead of baking names and statistics into artwork.

## Research sources

- [Topps Card Tech Glossary](https://www.topps.com/pages/card-tech-glossary)
- [Topps Hobby Glossary](https://uk.topps.com/pages/uk-hobby-glossary)
- [Topps Stadium Club](https://www.topps.com/pages/topps-stadium-club-baseball)
- [Topps Heritage](https://uk.topps.com/pages/topps-heritage-baseball)
- [Panini guide to inserts and parallels](https://assets.paniniamerica.net/resources/Whitepaper_Inserts.pdf)
- [Upper Deck Clear Cut](https://upperdeck.com/product/2024-25-clear-cut/)
