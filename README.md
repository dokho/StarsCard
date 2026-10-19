# StarsCard · 球星卡制作 Skill

用真实照片制作可收藏、可打印的球星卡。支持单人卡、团队合照卡、多时期成长卡，以及复古、杂志、镭射等风格。保留原有完整风格库；不虚构姓名、队伍、年份、统计或荣誉，缺失字段直接省略。

当前版本 **1.1.0**，技能名保持 **`stars-card-design`**。

## 跨工具使用

| 环境 | 安装或使用 |
|---|---|
| Codex | 让 skill-installer 安装本仓库的 `stars-card-design` 子目录，或复制到宿主技能目录 |
| Claude Code | 将 `stars-card-design/` 复制到 `~/.claude/skills/` 或项目 `.claude/skills/`，调用 `/stars-card-design` |
| Claude 自定义技能 | 下载并上传 [通用技能 ZIP](dist/stars-card-design-portable.zip)，包顶层是完整技能文件夹 |
| Gemini CLI | 克隆后运行 `gemini skills link ./StarsCard/stars-card-design`；用 `/skills list` 查看 |
| 普通聊天 / 项目资料 / 自定义智能体 | 完整上传或粘贴 [通用制卡指令](stars-card-design/通用制卡指令.md)，再提供照片和要求 |
| 接受根级 SKILL.md 的豆包/火山引擎导入器 | 使用保留的 [豆包布局 ZIP](dist/stars-card-design-doubao.zip)，具体入口按目标宿主要求 |

详细路径、示例与官方资料见 [跨工具使用说明](stars-card-design/references/platforms.md)。以上是格式与指令层适配，没有在所有平台登录导入实测；模型能否看图、编辑或导出文件，取决于宿主实际能力。没有原生技能入口时，用单文件指令即可，不声称所有聊天客户端都能安装 ZIP。

Codex 安装时可以直接给出：

```text
使用 skill-installer，从 https://github.com/dokho/StarsCard/tree/main/stars-card-design 安装球星卡制作技能。
```

## 开始制卡

提供原照片；姓名、球队、背号、位置和 Logo 都按实际已有资料使用，不必为了填满页面补造。

```text
请按球星卡制作技能，用这张团队合照做一张横版团队卡。
保留所有成员和奖杯，背景不要新增人物，不要“成长轨迹”文字。
采用蓝银收藏卡边框；没有确认的队名、年份和荣誉不写。
```

```text
使用 stars-card-design，把同一人的几张真实时期照片做成成长卡。
按我标注的顺序排版，采用复古风；未知年份省略，不生成缺失时期。
```

用户需要风格推荐时提供适合素材的选择；已经指定或交由助手决定时直接制作。风格名称仅用于选择，默认不印在卡面。真实人物优先原照片嵌入/遮罩排版；AI 参考编辑必须检查是否变脸、遗漏或复制成员。

## 印刷与交付

- 竖版成品默认 **63.5 × 88.9 mm**，横版交换宽高；四边 **3 mm 出血**，重要内容默认距裁切边 5 mm。
- 支持球队 Logo 通用背面，保持背面独立于正面风格；缺 Logo 时不猜造真实球队标志。
- 区分干净含出血稿、带裁切线单卡、A4 同页裁开粘贴与双面印刷，附长边/短边翻转规则及校准页。
- 镭射视觉模拟与真实镭射卡纸、覆膜、箔、白墨等工艺分别说明；不把数字效果冒充实体工艺。

详见 [印刷制作](stars-card-design/references/print-production.md)、[输入规范](stars-card-design/references/input-spec.md) 和 [交付质检](stars-card-design/references/delivery-qa.md)。印厂模板优先于默认值。

## 自动拼版（可选）

在具备 Python 3.10+ 的环境中：

```sh
python -m pip install -r stars-card-design/scripts/requirements.txt
python stars-card-design/scripts/impose_cards.py --mode calibration --flip long --out ./print/calibration
```

复制 `stars-card-design/assets/print-job.template.json` 为 `job.json`，填写已完成的含出血 PNG/JPEG 路径，再执行：

```sh
python stars-card-design/scripts/impose_cards.py job.json --mode paste --out ./print/paste
python stars-card-design/scripts/impose_cards.py job.json --mode duplex --flip long --out ./print/duplex
python stars-card-design/scripts/impose_cards.py job.json --mode singles --out ./print/singles
```

脚本与模型厂商无关，输出 RGB 桌面打样 PDF。当前 A4 纵向 2×2 拼版适合默认竖卡；横卡支持 singles，A4 横卡需要另外排版，不能自动缩小成品。未连接打印机、未做印厂 ICC/PDF-X 或真实工艺验证。其余边界见 [工具说明](stars-card-design/references/tooling.md)。

## 重新生成下载包

```sh
python scripts/build_packages.py
```

会生成/更新完整单文件指令、两种 ZIP 和校验和；单文件从同一套正文自动导出，不另维护一套规则。旧的 `python scripts/build_doubao_package.py` 命令继续保留。

```sh
python -m unittest discover -s tests -v
```

## 目录

```text
stars-card-design/       标准技能入口、照片/风格/印刷参考、输入模板、可选工具
  SKILL.md
  通用制卡指令.md        普通聊天使用的完整单文件
scripts/                打包工具
tests/                  导出、包布局和引用检查
dist/                   通用 ZIP、豆包布局 ZIP、SHA256SUMS.txt
VERSION
CHANGELOG.md
```

分发包不包含真实人物照片、球队 Logo、字体、密钥或聊天附件。创建时可见的偏好与默认假设分别记录在 [偏好来源](stars-card-design/references/preferences.md)。
