#!/usr/bin/env python3
"""Deterministic RGB proof imposition. No design generation or printer control."""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import tempfile
from pathlib import Path

from PIL import Image, ImageOps
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas

MM = 72 / 25.4
PAGE = (210.0, 297.0)
MARGIN, GAP, MARK = 10.0, 8.0, 3.0
LIMITS = [
    "RGB desktop proof only; no printer ICC OutputIntent or PDF/X certification.",
    "No face, logo, fact, safe-area, actual bleed-content or physical registration verification.",
    "Raster dimensions cannot prove the effective resolution of a composited face/photo.",
    "Duplex needs a matching driver flip setting and a physical calibration print.",
]


def positive(value, name):
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{name} must be a finite positive number")
    result = float(value)
    if not math.isfinite(result) or result <= 0:
        raise ValueError(f"{name} must be a finite positive number")
    return result


def in_bounds(x, y, w, h, page=PAGE, margin=MARGIN):
    return (x - MARK >= margin - 1e-6 and y - MARK >= margin - 1e-6
            and x + w + MARK <= page[0] - margin + 1e-6
            and y + h + MARK <= page[1] - margin + 1e-6)


def slots(w, h):
    x0 = (PAGE[0] - 2 * w - GAP) / 2
    y0 = (PAGE[1] - 2 * h - GAP) / 2
    result = [(x0 + col * (w + GAP), y0 + row * (h + GAP))
              for row in range(2) for col in range(2)]
    if any(not in_bounds(x, y, w, h) for x, y in result):
        raise ValueError("2x2 artwork plus marks does not fit A4 inside the 10 mm margin")
    return result


def back_position(x, y, w, h, flip, dx=0, dy=0):
    if flip == "long":
        return PAGE[0] - x - w + dx, y + dy
    return x + dx, PAGE[1] - y - h + dy


def read_asset(path, w, h, target, allow_low):
    if not path.is_file():
        raise ValueError(f"Image not found: {path}")
    with Image.open(path) as source:
        if source.format not in ("PNG", "JPEG"):
            raise ValueError(f"Only PNG/JPEG supported: {path}")
        if source.mode == "CMYK":
            raise ValueError(f"CMYK source unsupported; prepare an sRGB proof first: {path}")
        if getattr(source, "n_frames", 1) != 1:
            raise ValueError(f"Animated/multiframe source unsupported: {path}")
        original_orientation = source.getexif().get(274, 1)
        normalized = ImageOps.exif_transpose(source)
        rgba = normalized.convert("RGBA")
        if rgba.getchannel("A").getextrema()[0] != 255:
            raise ValueError(f"Transparent artwork rejected; composite final opaque art first: {path}")
        img = rgba.convert("RGB")
        has_icc = bool(source.info.get("icc_profile"))
    pixels = img.size
    if abs((pixels[0] / pixels[1]) / (w / h) - 1) > 0.0025:
        raise ValueError(f"Wrong bleed aspect ratio: {path}; got {pixels}, expected {w:g}:{h:g}")
    ppi = min(pixels[0] * 25.4 / w, pixels[1] * 25.4 / h)
    low = ppi + 0.5 < target
    if low and not allow_low:
        raise ValueError(f"Low resolution {ppi:.1f} ppi < {target:g}: {path}; proof override: --allow-low-dpi")
    info = {
        "path": str(path), "pixels": list(pixels), "effective_ppi": round(ppi, 3),
        "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        "icc_present": has_icc, "exif_orientation_normalized": original_orientation != 1,
        "low_resolution_override": low,
    }
    return img, info


def read_job(path, allow_low):
    doc = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(doc, dict):
        raise ValueError("Job must be a JSON object")
    trim = doc.get("trim_mm", [63.5, 88.9])
    if not isinstance(trim, list) or len(trim) != 2:
        raise ValueError("trim_mm must contain [width, height]")
    tw, th = [positive(v, "trim_mm") for v in trim]
    bleed = positive(doc.get("bleed_mm", 3), "bleed_mm")
    target = positive(doc.get("target_ppi", 300), "target_ppi")
    w, h = tw + 2 * bleed, th + 2 * bleed
    records = doc.get("cards")
    if not isinstance(records, list) or not records:
        raise ValueError("cards must be a nonempty array")
    cache, cards, seen = {}, [], set()
    for item in records:
        if not isinstance(item, dict):
            raise ValueError("Each card must be an object")
        cid = item.get("id")
        if not isinstance(cid, str) or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]{0,63}", cid):
            raise ValueError("Card IDs: 1-64 ASCII letters/digits/underscore/hyphen; start alphanumeric")
        # Filesystems may be case-insensitive; IDs also become output filenames.
        if cid.casefold() in seen:
            raise ValueError(f"Duplicate card ID: {cid}")
        seen.add(cid.casefold())
        card = {"id": cid}
        for side in ("front", "back"):
            raw = item.get(side) if side == "front" else item.get("back", doc.get("common_back"))
            if not isinstance(raw, str) or not raw.strip():
                raise ValueError(f"Missing {side} image for {cid}")
            source = (path.parent / raw).resolve()
            key = str(source)
            if key not in cache:
                cache[key] = read_asset(source, w, h, target, allow_low)
            card[side] = key
        cards.append(card)
    return (tw, th, bleed, target), cards, cache


def new_pdf(path, page, title):
    pdf = canvas.Canvas(str(path), pagesize=tuple(v * MM for v in page), pageCompression=1)
    pdf.setTitle(title)
    pdf.setAuthor("stars-card-design")
    return pdf


def line(pdf, page_h, x1, y1, x2, y2):
    pdf.line(x1 * MM, (page_h - y1) * MM, x2 * MM, (page_h - y2) * MM)


def crop_marks(pdf, page, x, y, w, h, bleed):
    pdf.saveState()
    pdf.setStrokeColorRGB(0, 0, 0)
    pdf.setLineWidth(0.2)
    for ty in (y + bleed, y + h - bleed):
        line(pdf, page[1], x - 3, ty, x - 1, ty)
        line(pdf, page[1], x + w + 1, ty, x + w + 3, ty)
    for tx in (x + bleed, x + w - bleed):
        line(pdf, page[1], tx, y - 3, tx, y - 1)
        line(pdf, page[1], tx, y + h + 1, tx, y + h + 3)
    pdf.restoreState()


def label(pdf, page, text, y=9):
    pdf.saveState()
    pdf.setFillColorRGB(0, 0, 0)
    pdf.setFont("Helvetica", 7)
    pdf.drawString(12 * MM, (page[1] - y) * MM, text)
    pdf.restoreState()


def draw_card(pdf, page, img, x, y, w, h, bleed):
    # No image mirroring, automatic cropping or rotation.
    pdf.drawImage(ImageReader(img), x * MM, (page[1] - y - h) * MM,
                  width=w * MM, height=h * MM)
    crop_marks(pdf, page, x, y, w, h, bleed)


def record_page(report, side, items):
    report["pages"].append({"page": len(report["pages"]) + 1, "side": side, "items": items})


def position_record(cid, side, x, y, w, h):
    return {"id": cid, "side": side, "bleed_rect_mm": [round(v, 5) for v in (x, y, w, h)]}


def compose(out, args, dims, cards, cache, report):
    tw, th, bleed, _ = dims
    w, h = tw + 2 * bleed, th + 2 * bleed
    if args.mode == "singles":
        page = (w + 2 * MARK, h + 2 * MARK)
        for card in cards:
            for side in ("front", "back"):
                name = f"{card['id']}-{side}.pdf"
                pdf = new_pdf(out / name, page, f"{card['id']} {side} RGB proof")
                pdf.setBleedBox(tuple(v * MM for v in (MARK, MARK, MARK + w, MARK + h)))
                pdf.setTrimBox(tuple(v * MM for v in (MARK + bleed, MARK + bleed,
                                                       MARK + w - bleed, MARK + h - bleed)))
                draw_card(pdf, page, cache[card[side]][0], MARK, MARK, w, h, bleed)
                pdf.save()
                report["files"].append(name)
                report["pages"].append({"file": name, "page": 1, "side": side,
                                        "items": [position_record(card['id'], side, MARK, MARK, w, h)]})
        return
    grid = slots(w, h)
    name = "a4-paste.pdf" if args.mode == "paste" else f"a4-duplex-{args.flip}.pdf"
    pdf = new_pdf(out / name, PAGE, f"{args.mode} RGB proof; 100 percent A4")
    count = 2 if args.mode == "paste" else 4
    for start in range(0, len(cards), count):
        chunk = cards[start:start + count]
        if args.mode == "paste":
            items = []
            for i, card in enumerate(chunk):
                for j, side in enumerate(("front", "back")):
                    x, y = grid[2 * i + j]
                    draw_card(pdf, PAGE, cache[card[side]][0], x, y, w, h, bleed)
                    items.append(position_record(card['id'], side, x, y, w, h))
            # Keep proof annotations inside the printable width even with 64-character IDs.
            pair_names = ", ".join(c['id'] if len(c['id']) <= 24 else c['id'][:17] + "~" +
                                   hashlib.sha256(c['id'].encode()).hexdigest()[:6] for c in chunk)
            label(pdf, PAGE, "RGB PROOF | PASTE - single-sided, 100% A4 | " + pair_names)
            record_page(report, "paste", items)
            pdf.showPage()
        else:
            for side in ("front", "back"):
                items = []
                for i, card in enumerate(chunk):
                    x, y = grid[i]
                    if side == "back":
                        x, y = back_position(x, y, w, h, args.flip, args.back_dx_mm, args.back_dy_mm)
                    draw_card(pdf, PAGE, cache[card[side]][0], x, y, w, h, bleed)
                    items.append(position_record(card['id'], side, x, y, w, h))
                label(pdf, PAGE, f"RGB PROOF | DUPLEX {args.flip.upper()} | {side.upper()} | SHEET {start // 4 + 1} | 100% A4")
                record_page(report, side, items)
                pdf.showPage()
    pdf.save()
    report["files"].append(name)


def calibration_tile(pdf, x, y, w, h, bleed, cid, side):
    crop_marks(pdf, PAGE, x, y, w, h, bleed)
    pdf.setLineWidth(0.5)
    pdf.rect((x + bleed) * MM, (PAGE[1] - y - h + bleed) * MM,
             (w - 2 * bleed) * MM, (h - 2 * bleed) * MM)
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawCentredString((x + w / 2) * MM, (PAGE[1] - y - 28) * MM, cid)
    pdf.setFont("Helvetica", 10)
    pdf.drawCentredString((x + w / 2) * MM, (PAGE[1] - y - 36) * MM, side.upper())
    # Up arrow and unique corner markers make orientation errors visible.
    line(pdf, PAGE[1], x + w / 2, y + 19, x + w / 2, y + 9)
    line(pdf, PAGE[1], x + w / 2, y + 9, x + w / 2 - 2, y + 12)
    line(pdf, PAGE[1], x + w / 2, y + 9, x + w / 2 + 2, y + 12)
    for n, (cx, cy) in enumerate(((x + 8, y + 8), (x + w - 8, y + 8),
                                  (x + 8, y + h - 8), (x + w - 8, y + h - 8))):
        line(pdf, PAGE[1], cx - 2, cy, cx + 2, cy)
        line(pdf, PAGE[1], cx, cy - 2, cx, cy + 2)
        pdf.setFont("Helvetica", 6)
        pdf.drawString((cx + 3) * MM, (PAGE[1] - cy) * MM, str(n + 1))
    pdf.circle((x + 8) * MM, (PAGE[1] - y - 15) * MM, 1 * MM, fill=1)


def calibration(out, args, report):
    w, h, bleed = 69.5, 94.9, 3
    grid = slots(w, h)
    name = f"calibration-{args.flip}.pdf"
    pdf = new_pdf(out / name, PAGE, f"A4 duplex calibration {args.flip}")
    for side in ("front", "back"):
        items = []
        for cid, (x, y) in zip(("A1", "A2", "B1", "B2"), grid):
            if side == "back":
                x, y = back_position(x, y, w, h, args.flip, args.back_dx_mm, args.back_dy_mm)
            calibration_tile(pdf, x, y, w, h, bleed, cid, side)
            items.append(position_record(cid, side, x, y, w, h))
        label(pdf, PAGE, f"CALIBRATION | {side.upper()} | {args.flip.upper()} EDGE | ACTUAL SIZE 100% | A4")
        line(pdf, PAGE[1], 80, 270, 130, 270)
        for tx in (80, 130):
            line(pdf, PAGE[1], tx, 268, tx, 272)
        pdf.setFont("Helvetica", 8)
        pdf.drawCentredString(105 * MM, 22 * MM, "50 mm - measure after printing")
        record_page(report, side, items)
        pdf.showPage()
    pdf.save()
    report["files"].append(name)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("job", nargs="?", type=Path)
    parser.add_argument("--mode", choices=("paste", "duplex", "singles", "calibration"), required=True)
    parser.add_argument("--flip", choices=("long", "short"), default="long")
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--back-dx-mm", type=float, default=0)
    parser.add_argument("--back-dy-mm", type=float, default=0)
    parser.add_argument("--allow-low-dpi", action="store_true")
    args = parser.parse_args(argv)
    try:
        if not all(math.isfinite(v) for v in (args.back_dx_mm, args.back_dy_mm)):
            raise ValueError("Back offsets must be finite")
        if args.mode not in ("duplex", "calibration") and (args.back_dx_mm or args.back_dy_mm):
            raise ValueError("Back offsets only apply to duplex/calibration")
        if args.mode == "calibration":
            if args.job:
                raise ValueError("calibration does not accept a job")
            dims, cards, cache = (63.5, 88.9, 3, 300), [], {}
        else:
            if not args.job:
                raise ValueError("This mode requires a job JSON")
            dims, cards, cache = read_job(args.job.resolve(), args.allow_low_dpi)
        tw, th, bleed, target = dims
        w, h = tw + 2 * bleed, th + 2 * bleed
        if args.mode != "singles":
            grid = slots(w, h)
            if args.mode in ("duplex", "calibration"):
                for x, y in grid:
                    bx, by = back_position(x, y, w, h, args.flip, args.back_dx_mm, args.back_dy_mm)
                    if not in_bounds(bx, by, w, h):
                        raise ValueError("Back offset moves artwork/marks outside the 10 mm printable margin")
        report = {
            "version": 1, "mode": args.mode, "trim_mm": [tw, th], "bleed_mm": bleed,
            "artwork_mm": [w, h], "target_ppi": target,
            "a4_mm": list(PAGE) if args.mode != "singles" else None,
            "flip": args.flip if args.mode in ("duplex", "calibration") else None,
            "back_offset_mm": [args.back_dx_mm, args.back_dy_mm],
            "color": "RGB desktop proof; source should be prepared in sRGB",
            "physical_registration": "NOT VERIFIED",
            "limitations": LIMITS, "assets": [v[1] for v in cache.values()],
            "files": [], "pages": [],
        }
        # Render in a temporary directory; no partial outputs on validation/render failure.
        with tempfile.TemporaryDirectory(prefix="sports-card-imposition-") as tmp:
            stage = Path(tmp)
            if args.mode == "calibration":
                calibration(stage, args, report)
            else:
                compose(stage, args, dims, cards, cache, report)
            report["files"].append("layout-report.json")
            (stage / "layout-report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
            if args.out.exists() and not args.out.is_dir():
                raise ValueError("Output path is not a directory")
            for name in report["files"]:
                if (args.out / name).exists():
                    raise ValueError(f"Refusing to overwrite: {args.out / name}")
            args.out.mkdir(parents=True, exist_ok=True)
            for name in report["files"]:
                # Exclusive creation is also safe against an output appearing after the check.
                with (args.out / name).open("xb") as dest:
                    dest.write((stage / name).read_bytes())
        print(f"Created {len(report['files']) - 1} PDF(s) and layout-report.json in {args.out.resolve()}")
        print("RGB PROOF ONLY. Physical duplex registration and production color are not verified.")
        return 0
    except (ValueError, OSError, TypeError, KeyError, Image.DecompressionBombError) as exc:
        parser.exit(2, f"Error: {exc}\n")


if __name__ == "__main__":
    raise SystemExit(main())
