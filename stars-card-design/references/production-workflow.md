# Production workflow

Read this reference when generating a finished card image.

## Intake schema

Track the job using this structure. `teamName`, `teamLogo`, and all back fields are optional.

```yaml
photo: user-provided image
player:
  name: required
  number: required
  position: required
  teamName: optional
  teamLogo: optional image
design:
  style: required after selection
  orientation: portrait | landscape
  sides: front | front-and-back
back:
  biography: optional
  statistics: optional, user supplied only
  achievement: optional, user supplied only
  motto: optional
  contact: optional
```

## First response template

When the photo or required data is missing, ask in one compact message:

```text
请上传要制作球星卡的球员照片，并提供：
1. 球员姓名
2. 背号
3. 场上位置
4. 所在球队（选填）
5. 球队 Logo 图片（选填）

收到后我会根据照片推荐卡面风格，并让你选择横版/竖版以及是否制作背面。
```

Do not ask for a logo URL when an image attachment is more reliable. Accept partial replies and ask only for still-missing required fields.

## Photo inspection

Prefer a source where:

- the face is sharp and not covered;
- the athlete is at least 800 px tall in the source image;
- limbs and sports equipment needed by the pose are not cropped;
- lighting does not destroy facial detail;
- the user has permission to use the image.

An imperfect background is acceptable because it can be replaced. Do not reject casual or youth-sports photography merely because it is not studio quality.

## Style recommendation logic

- Strong action and visible environment → 赛场瞬间 or 锋芒竞技.
- Clean portrait or posed photo → 荣耀典藏 or 复古档案.
- Youth athlete or playful brief → 热血英雄.
- Team/community identity and known location → 城市主场.
- Low-resolution photo → favor illustration or archival treatment rather than fake photographic sharpness.

Offer only choices that suit the source. The user may also describe a custom style.

## Two-stage rendering

### Stage A — artwork

Generate or edit the athlete and visual background with the uploaded photo as the identity reference. The artwork should include intentional quiet zones for later text. Avoid generated typography, numbers, logos, signatures, statistics, QR codes, and fine print.

Translate the selected style into visual characteristics, then remove the selection label from the image prompt's visible-copy list. State explicitly that the internal style name must not be rendered. Do not add decorative slogans unless the user supplied or approved them.

Do not casually change uniform colors or equipment. When a supplied uniform contains marks the user did not ask to reproduce, preserve only what is necessary for faithful personal depiction and avoid adding new third-party branding.

### Stage B — deterministic layout

Composite these elements after artwork generation:

- player name;
- jersey number;
- position;
- team name, when supplied;
- supplied logo, when supplied;
- card code or edition label, if honest and requested;
- all back text and statistics.

Use a real text/layout tool for this stage. Do not use generative pixels for exact text. Preserve the logo's aspect ratio and do not recolor it unless the user asks.

Do not place internal style-selection names such as 赛场瞬间, 锋芒竞技, 复古档案, 城市主场, 热血英雄, or 荣耀典藏 on the exported card. They describe how to design the card; they are not card copy.

## Canvas, bleed, and safe area

The default trim is 2.5 × 3.5 inches.

| Output | Trim size | Print canvas with 0.125 in bleed |
|---|---:|---:|
| Portrait | 1500 × 2100 px | 1650 × 2250 px |
| Landscape | 2100 × 1500 px | 2250 × 1650 px |

These pixel sizes use a 600 ppi master. For a print canvas, the trim line sits 75 px from every outer edge. Keep critical content at least 90 px inside the trim line. Background artwork must extend through the full bleed.

For digital-only delivery, use the trim size without bleed. Do not stretch a generated image to fit; crop proportionally and protect the face, hands, ball/equipment, and logo.

## Front hierarchy

Required information:

1. athlete image;
2. player name;
3. jersey number;
4. position.

Optional information:

5. team name;
6. team logo;
7. year, card code, or rarity label when explicitly requested.

Use at most two prominent text levels. The player should remain recognizable at a 240 px-tall thumbnail.

## Back layout

Use one simple, neutral back design across all front styles for the same set. The back must not reveal whether the front is modern, retro, comic, premium, or another variant. Do not repeat the front style's title, signature frame, foil/chrome treatment, illustration motif, rarity effect, or distinctive palette behavior.

Prefer a restrained team-adjacent palette, flat background, thin border, generous whitespace, and conventional information hierarchy. A useful hierarchy is:

1. small player portrait or neutral monogram;
2. player identity line;
3. biography, achievement, or motto;
4. user-supplied statistics table;
5. team/contact field when supplied;
6. small note such as “Personal commemorative card” when appropriate.

Never invent missing statistics. Omit empty sections rather than displaying fake placeholder values in a final card.

When generating multiple front variants, generate the common back once and reuse the same file for every variant. Create variant-specific backs only when the user explicitly asks for them.

## File naming

Use filesystem-safe names:

```text
<player-name>-star-card-front.png
<player-name>-star-card-back.png
<player-name>-star-card-preview.png
```

Use transliteration or a safe fallback only when the environment cannot preserve the player's writing system.

## Final QA

Check the exported pixels, not only the source document:

- expected width and height;
- no clipped letters or logo;
- no generated text artifacts remain in the art layer;
- exact agreement with user-supplied spelling and numbers;
- sufficient contrast in light and dark regions;
- no style-selection name printed on the front or back;
- back is simple, neutral, and reusable across front variants;
- no claim of official licensing, autograph authentication, or game-used material.
