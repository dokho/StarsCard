# Stars Card Design Skill

一个把用户照片和球员资料制作成标准尺寸球星卡的跨平台 AI Skill，适用于 Codex，以及支持 `SKILL.md`/ZIP 导入的豆包系火山引擎 Agent 产品。覆盖棒球、篮球、足球及其他运动项目。

它可以帮助你：

- 引导用户上传球员照片并补全姓名、背号和位置；
- 接受选填的球队名称与球队 Logo；
- 根据照片推荐风格，并选择横版/竖版、单面/正反面；
- 提供写实竞技、复古收藏、插画潮流、高端典藏和故事主题等多组风格；
- 风格名称仅用于选择，默认不会印在最终卡面上；
- 先生成视觉底图，再精确排版姓名、号码、位置和 Logo；
- 输出 2.5 × 3.5 英寸标准比例的高清 PNG；
- 继续支持风格研究、稀有度体系和可维护模板设计。

## 安装

### Codex

将 `stars-card-design` 文件夹复制到 Codex 的 skills 目录：

```text
~/.codex/skills/stars-card-design
```

也可以使用 Codex 的 skill installer 从本 GitHub 仓库安装。

### 豆包 / 火山引擎

直接下载并上传 [`dist/stars-card-design-doubao.zip`](dist/stars-card-design-doubao.zip)。ZIP 根目录包含 `SKILL.md` 和全部运行参考文件，不包含 Codex 专属的 `agents/openai.yaml`。

适用入口包括支持技能文件导入的火山引擎 Skill Center、iDA、ArkClaw 或 OpenViking。不同控制台的按钮名称可能略有差异，通常选择“技能中心 → 导入/上传技能”，上传 ZIP 后再把技能授权给对应 Agent。

普通豆包聊天客户端是否提供第三方技能导入入口取决于当前产品版本和账号能力；如果看不到“技能中心/导入技能”，不能直接安装这个 ZIP。此时可改在火山引擎 Agent 产品中使用，或将 `SKILL.md` 内容配置为工作流/智能体指令。

如需重新生成豆包安装包：

```text
python scripts/build_doubao_package.py
```

相关官方文档：

- [iDA Skill Center：上传 SKILL.md 或 Skill.zip](https://docs.volcengine.com/docs/DataAgentPrivate/SkillsCentre_2?lang=zh)
- [OpenViking：导入 Skills](https://docs.volcengine.com/docs/vector_database_vikingdb/Importskills?lang=zh)
- [豆包 Seedream：图片生成与编辑](https://docs.volcengine.com/docs/LakeAIService/ImagegenerationandeditingDoubaoseedreamseriesmodels?lang=zh)

## 使用

```text
$stars-card-design 帮我把这张篮球运动员照片制作成一张球星卡。
```

```text
$stars-card-design 把现有的“酷炫竞技”风格拆成卡面骨架、视觉工艺和故事主题，并给出生成提示词。
```

## 目录

```text
stars-card-design/
├── SKILL.md
├── agents/
│   └── openai.yaml
└── references/
    ├── doubao-volcengine.md
    ├── production-workflow.md
    ├── style-catalog.md
    └── style-system.md

dist/
└── stars-card-design-doubao.zip

scripts/
└── build_doubao_package.py
```
