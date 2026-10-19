# 输入规范

先把现有输入整理成 `assets/intake.template.json` 的结构。该模板是人工/代理的需求表，不是拼版工具的参数；拼版工具使用另一个 `print-job.template.json`。

## 最小可执行输入

| 项目 | 要求 | 缺失处理 |
|---|---|---|
| 人物照片 | 可读取原始文件，注明每张照片里哪位是主体 | 缺照片只做版式；多人照主体不明需问清，不能猜 |
| 人物标识 | 用户给出的姓名或任务内部 ID | 姓名可省略，内部 ID 不当作真实姓名上卡 |
| 卡型 | `single`、`team` 或 `growth` | 默认 single；合照且用户要求团队卡时用 team，多张照片不自动认定为成长卡 |
| 方向 | `portrait` 或 `landscape` | 用户指定优先；团队横卡保留全部成员，不按单人卡裁切 |
| 风格 | `retro`、`magazine`、`holographic` 或明确自定义 | 最近明确选择优先；无选择用克制现代收藏卡，并标为假设 |
| 交付 | `design`、`paste`、`duplex`、`singles`，可多选 | 未要求印刷时先做设计，不替用户增加复杂工艺 |

## 事实与来源

`facts` 的每个字段使用 `{value, source}`，未知值是 `null`，不使用看似真实的示例资料。`source` 写用户消息、附件文件名和位置，或经用户要求查询的可靠来源与日期。

- 字段可包含 name、team、jersey_number、position、season、birth_date、height、weight、statistics、awards；均为可选。
- 数据必须带对应赛季/时间范围、单位及来源。不把身高体重从外貌估计出来。
- 网图文件名、球衣印花或照片 EXIF 不足以确认身份、号码所属赛季、时期或荣誉。
- 用户自述可以作为用户提供资料使用，但不称作已独立验证。
- 自定义卡号写入 `design.catalog_id`，区别于球衣号。不要默认增加 Rookie、MVP、签名、1/1、限量、官方认证等声称；用户要求装饰性卡号也需标明自定义系列。
- 无资料时删掉对应模块，留下空间，不用随机统计填版。

## 照片记录

每项 `photos[]` 使用：

```json
{
  "id": "photo-01",
  "path": "./photos/source-01.jpg",
  "subject": null,
  "stage_label": null,
  "captured_at": null,
  "source": "用户上传原图",
  "approved_identity_reference": false,
  "allowed_edits": ["crop", "mask", "exposure", "white_balance"]
}
```

`subject` 是用户指认的对象，例如“左侧穿白色球衣的人”，不是模型识别出的姓名。`approved_identity_reference=true` 仅用于用户确实认可过且文件可读取的版本。`captured_at` 和时期标签未确认时保持 null。

成长卡通常用 2–4 张照片作为设计建议，不是硬性数量限制；照片不足不能通过年龄生成补齐历史。可用单图卡替代，并说明缺少的真实时期素材。

## 背面与印刷输入

- Logo：原始 SVG/PDF/透明 PNG，记录用户指认的球队及文件来源；禁止 AI 重绘真实 Logo。照片中的 Logo 过小不能直接当作可印刷原稿。
- `back.mode` 默认 `team_common`：同一球队/系列共用背面。正面可变，背面不加某个球员的资料。队伍未确认或 Logo 缺失时只交付明确的待补稿。
- `production.trim_mm` 默认 `[63.5, 88.9]`；`bleed_mm=3`；`safe_mm=5`；`target_ppi=300`。印厂明确参数优先。
- 横版用 `design.orientation="landscape"` 且 `production.trim_mm=[88.9,63.5]`。方向与尺寸冲突时先解决，不旋转图或拉伸图假装兼容。团队卡不加未确认队名、赛事、年份或荣誉；合照里现有成员都是主体。
- `production.duplex_flip` 为 `long` 或 `short`，仅描述 A4 纵向驱动设置；手工翻纸需现场校准，不能从打印机品牌猜进纸方向。
- `production.finish` 区分 `digital_simulation`、`holographic_stock`、`holographic_laminate`、`foil` 等；真正工艺需供应商规范。

## 缺省行为

有足够素材就做，简要列出关键假设。事实缺失通过省略解决；人物不可访问、多人身份不明或正反配对不明会影响结果，必须先明确相关部分，其他独立部分可继续。不得把输入模板中的 null 直接印在成品上。
