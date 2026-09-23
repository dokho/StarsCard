# Style catalog

Use this catalog when recommending or expanding card-style choices. Style names are UI labels only and must not appear on the exported card unless the user explicitly requests visible style copy.

Recommend six styles that fit the source photo. Always offer “查看更多风格” so the user can see this complete catalog without requesting repeated refreshes.

## 写实竞技

| Selection label | Visual direction | Works best for |
|---|---|---|
| 赛场瞬间 | Full-bleed game photography, restrained score-broadcast accents | Strong action and match context |
| 锋芒竞技 | Sharp metallic geometry, team-color light, controlled speed trails | Clean portraits and competitive poses |
| 极速破风 | Diagonal motion blur, wind-cut lines, high-contrast lighting | Running, skating, racing, pitching and swinging |
| 聚光主场 | Dark stadium, concentrated spotlight, crowd bokeh, dramatic entrance | Portraits and hero introductions |
| 冰晶能量 | Cool silver-blue facets, frost-like refraction, crisp highlights | Winter sports and blue/white uniforms |
| 烈焰对决 | Dark field, controlled red-orange energy, ember trails | Aggressive action and rivalry moments |

## 复古收藏

| Selection label | Visual direction | Works best for |
|---|---|---|
| 复古档案 | Warm cardstock, limited inks, halftone and season-record layout | School teams and commemorative sets |
| 校园年鉴 | Yearbook portrait framing, school colors, handwritten-note accents | Students, academy and youth teams |
| 胶片记忆 | Analog film grain, contact-sheet details, date-stamp language without fake dates | Candid and nostalgic portraits |
| 报纸头条 | Editorial columns, bold headline hierarchy, monochrome action crop | Milestones and tournament stories |
| 经典票根 | Event-ticket geometry, perforation cues and admission-stub typography | Finals, debuts and special matches |
| 老牌海报 | Two- or three-color screen print, large type and simplified sport symbols | Strong silhouettes and team promotion |

## 插画潮流

| Selection label | Visual direction | Works best for |
|---|---|---|
| 热血英雄 | Original sports-comic energy, ink strokes and exaggerated motion | Youth athletes and energetic personalities |
| 美式漫画 | Bold contour, halftone dots, dynamic panels and impact shapes | Expressive poses and dramatic action |
| 水彩手绘 | Transparent paint edges, paper texture and soft color blooms | Calm portraits and keepsake gifts |
| 都市涂鸦 | Spray-paint texture, marker strokes and court/street language | Basketball, skateboarding and street sports |
| 霓虹赛博 | Dark background, neon contour light and clean HUD-like geometry | Esports-adjacent and futuristic briefs |
| 拼贴纪事 | Photo cutouts, tape, labels and layered paper fragments | Multi-moment storytelling and youth teams |

## 高端典藏

| Selection label | Visual direction | Works best for |
|---|---|---|
| 荣耀典藏 | Ceremonial symmetry, deep color, restrained foil and generous spacing | Captains, aces and commemorative portraits |
| 黑金王者 | Matte black field, one controlled gold hierarchy and strong silhouette | Confident portraits and awards |
| 极简白金 | Pale neutral field, precise typography and tiny metallic accents | Studio portraits and modern premium sets |
| 宝石切面 | Jewel-tone facets, dimensional border and subtle refraction | Limited variants without excessive effects |
| 博物馆肖像 | Framed portrait, quiet gallery lighting and archival caption structure | Retirement, anniversary and formal cards |
| 冠军勋章 | Emblematic geometry, medal/ribbon cues and victory lighting | User-supplied championship achievements |

## 故事主题

| Selection label | Visual direction | Required context |
|---|---|---|
| 城市主场 | Original local landmarks, fan culture and place-based symbols | User provides or confirms a city/location |
| 新秀首秀 | Fresh color, debut marker and optimistic forward motion | User confirms debut/rookie context |
| 决胜时刻 | Clock/inning/score tension expressed abstractly, focused action | User provides the real moment; do not invent it |
| 球队灵魂 | Team-color field, community symbols and leadership focus | Team identity is known |
| 里程碑 | Numeric hierarchy and restrained celebration | User supplies the real milestone |
| 双人羁绊 | Balanced paired portrait and shared story structure | Two authorized athlete photos are available |

## Recommendation rules

- Clean posed portrait: prioritize 荣耀典藏, 锋芒竞技, 校园年鉴, 极简白金, 博物馆肖像, or 水彩手绘.
- Strong action photo: prioritize 赛场瞬间, 极速破风, 热血英雄, 烈焰对决, 决胜时刻, or 报纸头条.
- Low-resolution source: prioritize 复古档案, 老牌海报, 水彩手绘, 美式漫画, or 拼贴纪事 instead of inventing photographic sharpness.
- Youth or school athlete: include 校园年鉴, 复古档案, 热血英雄, 拼贴纪事, and one premium option.
- Do not offer 城市主场, 新秀首秀, 决胜时刻, 里程碑, 冠军勋章, or 双人羁绊 unless the required context is available.
- Keep recommendations visually distinct. Do not present six variations of metallic blue.

## Prompt boundary

Translate the selected label into its visual direction, then omit the label itself from all visible-text instructions. Explicitly state:

```text
The internal style-selection label is not card copy. Do not render it anywhere on the front or back.
```

Also avoid invented slogans. Visible copy should normally be limited to user-supplied player data, approved back content, and generic functional labels such as `PLAYER PROFILE` when useful.
