# Stars Card Design Skill

一个把用户照片和球员资料制作成标准尺寸球星卡的 Codex Skill，适用于棒球、篮球、足球及其他运动项目。

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

将 `stars-card-design` 文件夹复制到 Codex 的 skills 目录：

```text
~/.codex/skills/stars-card-design
```

也可以使用 Codex 的 skill installer 从本 GitHub 仓库安装。

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
    ├── production-workflow.md
    ├── style-catalog.md
    └── style-system.md
```
