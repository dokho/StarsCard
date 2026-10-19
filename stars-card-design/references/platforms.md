# 跨工具安装与使用

技能名统一为 `stars-card-design`。跨工具兼容的是工作流和文件结构；实际看图、出图、导出和运行脚本取决于宿主能力。平台说明核对于 2026-10-19，尚未在每个平台登录导入实测。

## 选择哪种文件

| 使用环境 | 使用方式 |
|---|---|
| 支持 Agent Skills 的代理 | 安装完整 `stars-card-design/` 文件夹，入口是 `SKILL.md` |
| Claude 网页/桌面自定义技能入口 | 上传 `dist/stars-card-design-portable.zip`，其顶层仅有技能文件夹 |
| Claude Code | 把技能文件夹放入 `~/.claude/skills/` 或项目 `.claude/skills/` |
| Gemini CLI | 放入 `~/.gemini/skills/` 或项目 `.gemini/skills/`，也可 link 本地目录 |
| Codex | 安装到宿主发现的技能目录，或使用 skill-installer 指向本仓库的技能子目录 |
| 普通聊天、项目资料或自定义智能体 | 上传或完整粘贴 `通用制卡指令.md`，再提供原照片与本次需求 |
| 只有文生图输入框的工具 | 由有文本能力的助手按通用指令生成单独视觉提示词；没有参考图编辑时只做卡框/背景素材 |

普通聊天方式适用于能接收这些文字的工具；不是声称所有产品都有原生技能安装入口，也不是声称它们都能处理照片或执行 Python。

## Claude Code

克隆仓库后，将 `stars-card-design` 整个文件夹复制到个人或项目的 `.claude/skills` 中。最终路径例如 `~/.claude/skills/stars-card-design/SKILL.md`。已有同名技能先比较、备份，再由用户决定替换，不盲目覆盖。

调用示例：

```text
/stars-card-design 使用我上传的团队合照做横版球星卡，保留全部成员，未知队名省略。
```

文件夹位置与命令见 [Claude Code 官方技能文档](https://code.claude.com/docs/en/skills)。

## Claude 网页 / 桌面

如果账号界面有自定义技能上传入口，上传 `dist/stars-card-design-portable.zip`，不要上传整个仓库 ZIP。包结构是 `stars-card-design/SKILL.md` 加相邻资源，不是把 SKILL.md 散放到 ZIP 顶层。启用后用自然语言请求制卡。

导入结构见 [Claude 官方自定义技能说明](https://support.claude.com/en/articles/12512198-how-to-create-custom-skills)。具体按钮与可用能力按当前账号界面；没有入口时使用单文件指令。

## Gemini CLI

克隆仓库后，在仓库目录使用：

```sh
gemini skills link ./stars-card-design
```

在 Gemini CLI 中用 `/skills list` 查看；修改后用 `/skills reload`，然后自然语言请求使用 `stars-card-design`。也可直接复制到 `~/.gemini/skills/stars-card-design`。宿主要求的技能激活确认仍有效。

这些命令见 [Gemini CLI 官方技能管理说明](https://geminicli.com/docs/cli/using-agent-skills/)。Gemini 网页聊天与 Gemini CLI 不是同一个安装环境；网页端采用单文件指令方式。

## Codex

可以让 Codex 的 skill-installer 从以下 GitHub 路径安装：

```text
https://github.com/dokho/StarsCard/tree/main/stars-card-design
```

或将技能文件夹放入个人/项目技能目录，例如 `~/.agents/skills/stars-card-design`、项目 `.agents/skills/stars-card-design`。本环境也发现 `~/.codex/skills`；以实际宿主的已配置目录为准，同名技能只保留一个安装位置。

```text
使用 $stars-card-design，根据我上传的照片制作球星卡。
```

目录与发现规则参考 [OpenAI 官方技能说明](https://learn.chatgpt.com/docs/build-skills)。

## 豆包、火山引擎与其他聊天工具

先使用 `通用制卡指令.md`：完整上传或粘贴，再输入本次任务并上传原照片。它包含核心规则、印刷说明和输入模板，无需工具能自动跟随本地相对引用。即使不支持 Markdown 文件上传，也可复制其全文。

已有接受根级 `SKILL.md` 的豆包/火山引擎导入器可继续使用 `dist/stars-card-design-doubao.zip`。此包沿用本仓库既有布局，去掉可选的 OpenAI 界面文件；不保证每个豆包相关产品接受同一种 ZIP。相应运行能力映射见 `doubao-volcengine.md`。

只粘贴 `SKILL.md` 入口会缺少相邻参考文件；不支持文件夹读取时，改用完整单文件，而不是让模型猜这些参考内容。

## Python 拼版

有 Python 3.10+、Pillow、ReportLab 的环境可以独立运行 `scripts/impose_cards.py`；无需安装任何模型 SDK。仅上传单文件指令不会把脚本部署到聊天环境。需要执行时，再提供完整技能文件夹和实际图稿。

## 仓库结构与标准

标准入口、资源目录和前置元数据遵循 [Agent Skills 规范](https://agentskills.io/specification)。`agents/openai.yaml` 只用于支持它的界面；其他工具可以忽略。没有加入厂商专属强制工具列表，也没有自动写入 `CLAUDE.md`、`GEMINI.md` 或账户配置。
