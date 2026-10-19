# 拼版工具与安装后使用

`scripts/impose_cards.py` 用已经完成的**含出血图稿**生成 PDF，不生成球员照片或设计，也不会给成品图自动补真出血。

## 运行环境

Python 3.10+，依赖 Pillow 与 ReportLab。在任务环境的虚拟环境中安装缺少的依赖：

```sh
python -m pip install -r scripts/requirements.txt
```

无需 API 密钥、联网或 Adobe 账号即可拼版。设计阶段的图像工具由运行环境提供；本技能不绑定收费图像服务。

脚本不依赖 Codex、Claude 或 Gemini 的 SDK，可在任何具备上述运行环境并可访问素材的系统中运行。只有文本聊天时，这些命令是操作说明，不代表已经执行；依赖未安装时先报告实际缺项，不绕过宿主权限。

## 图稿输入约定

- 输入支持 PNG / JPEG，图像比例必须与含出血物理尺寸相符，默认比例为 69.5:94.9；容许约 0.25% 的像素取整误差。
- 使用已嵌入完整卡面、正常 EXIF 朝向的平面图稿。透明图像会被拒绝，避免把透明出血默默填白；请在设计阶段合成到最终不透明底。
- 图稿至少达到目标有效 PPI；四舍五入保留 0.5 ppi 余量。低清默认报错，`--allow-low-dpi` 才可生成明确标注为 proof 的低清样稿。
- CMYK JPEG 被拒绝。这个工具定位 RGB 桌面打样，不负责无 ICC 的隐式 CMYK 转换。输入若有 ICC 则需在图像编辑工具里先确认/转换为 sRGB。
- 每个卡 ID 仅可用字母、数字、下划线、短横线，不能重复。路径相对 job JSON 所在目录，不是相对当前终端。
- `common_back` 可提供同队通用背面；单卡 `back` 会覆盖它。跨球队应分别指定背面或分项目，不把一个队背面套到别队。
- 参数模板见 `assets/print-job.template.json`。图片路径是待替换的占位路径，不附带球员或球队数据。

## 常用命令

```sh
python scripts/impose_cards.py job.json --mode paste --out ./print/paste
python scripts/impose_cards.py job.json --mode duplex --flip long --out ./print/duplex-long
python scripts/impose_cards.py job.json --mode duplex --flip short --out ./print/duplex-short
python scripts/impose_cards.py job.json --mode singles --out ./print/singles
python scripts/impose_cards.py --mode calibration --flip long --out ./print/calibration-long
```

默认 A4 纵向 2×2，出血稿间距 8 mm，外部裁切线占 3 mm。paste 每页两对，duplex 每张纸四张卡。没有足够图稿填满一页时留白，不缩放。

`--back-dx-mm 0.3 --back-dy-mm -0.2` 仅修正 duplex/calibration 的背面；正值为背面 PDF 正读视角向右/向下。透光测量与修正符号见 [印刷与对位](print-production.md)。参数不能把图稿和标记推出保留 10 mm 的可印区。

工具拒绝覆盖已有目标文件。请使用新的输出目录或新版本目录，不用强制覆盖掩盖旧稿。所有输入、比例、有效 PPI 和几何先检查，错误时不写新的 PDF。

## 输出

- `a4-paste.pdf`：单面粘贴，页边只含配对 ID，卡面不加标签。
- `a4-duplex-long.pdf` / `a4-duplex-short.pdf`：正反交替的 PDF。
- `卡ID-front.pdf` / `卡ID-back.pdf`：带裁切线的单卡，具有 TrimBox / BleedBox。
- `calibration-long.pdf` / `calibration-short.pdf`：两页，不对称标记和 50 mm 标尺。
- `layout-report.json`：尺寸、输入分辨率/哈希、每页卡片位置、配对、翻边、偏移及局限；可用于复核，不是生产印前认证。

所有几何按 mm 转换为 PDF pt，页面渲染目标不由文件的 DPI 标签决定。工具只验证整体卡图像像素，不能自动知道卡图中某个局部人脸是否被放大；设计阶段仍需检查原图裁切有效像素。

## 能力边界

本工具不支持任意多拼、旋转横卡、折叠铰接拼版、圆角刀模、专色分色、PDF/X 输出或印刷机驱动控制。自定义尺寸可由 job 中 `trim_mm` / `bleed_mm` 设置，但如果 2×2 与标记放不下 A4，报错；应另做拼版，不能自动缩小成品。用户给印厂模板时优先按模板另行排版。

横版 `[88.9,63.5]` 可用 singles 输出单卡。默认 A4 纵向 2×2 不容纳两列横卡加裁切线与页边距，因此 paste/duplex 将拒绝，需另做横卡 A4 版式；这属于几何边界，与使用哪家 AI 无关。
