#!/usr/bin/env python3
from pathlib import Path
import sys

from PIL import Image, ImageDraw


def main() -> None:
    if len(sys.argv) != 3:
        raise SystemExit("usage: make_contact_sheets.py PAGE_DIR OUTPUT_DIR")

    page_dir = Path(sys.argv[1])
    output_dir = Path(sys.argv[2])
    output_dir.mkdir(parents=True, exist_ok=True)
    pages = sorted(page_dir.glob("page-*.jpg"))
    if not pages:
        raise SystemExit(f"no rendered pages found in {page_dir}")

    columns = 4
    rows = 4
    cell_width = 340
    cell_height = 500
    label_height = 28
    thumb_size = (300, 440)

    for sheet_index, start in enumerate(range(0, len(pages), columns * rows), start=1):
        sheet = Image.new("RGB", (columns * cell_width, rows * cell_height), "#dfe6e9")
        draw = ImageDraw.Draw(sheet)
        for offset, page_path in enumerate(pages[start : start + columns * rows]):
            row, column = divmod(offset, columns)
            with Image.open(page_path) as source:
                page = source.convert("RGB")
                page.thumbnail(thumb_size, Image.Resampling.LANCZOS)
            x = column * cell_width + (cell_width - page.width) // 2
            y = row * cell_height + label_height
            sheet.paste(page, (x, y))
            draw.text((column * cell_width + 14, row * cell_height + 7), page_path.stem, fill="#162438")
        sheet.save(output_dir / f"sheet-{sheet_index:02d}.jpg", quality=88, optimize=True)

    print(f"Created {(len(pages) + columns * rows - 1) // (columns * rows)} sheets for {len(pages)} pages")


if __name__ == "__main__":
    main()
