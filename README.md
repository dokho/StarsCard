# Stars Card Design Skill

一个用于研究、规划和设计原创球星卡视觉方案的 Codex Skill，适用于棒球、篮球、足球及其他运动项目。

它可以帮助你：

- 选择适合球员与场景的卡面结构；
- 设计基础卡、特卡和稀有度体系；
- 生成不依赖现有品牌名称的 AI 绘图提示词；
- 将单张卡面扩展成可维护的模板系统；
- 识别签名、纪念物、联盟和球队素材相关的版权风险。

## 安装

将 `stars-card-design` 文件夹复制到 Codex 的 skills 目录：

```text
~/.codex/skills/stars-card-design
```

也可以使用 Codex 的 skill installer 从本 GitHub 仓库安装。

## 使用

```text
$stars-card-design 为一名校园篮球后卫设计一套包含基础卡、城市特卡和冠军限量卡的视觉方案。
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
    └── style-system.md
```
