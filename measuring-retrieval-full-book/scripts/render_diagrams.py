#!/usr/bin/env python3
from pathlib import Path
import shutil
import subprocess
import sys

root = Path(__file__).resolve().parents[1]
inkscape = shutil.which("inkscape") or "/Applications/Inkscape.app/Contents/MacOS/inkscape"
if not Path(inkscape).exists():
    raise SystemExit("Inkscape is required to render diagram PNG files.")

svgs = sorted((root / "assets" / "diagrams").glob("*.svg"))
for index, svg in enumerate(svgs, start=1):
    png = svg.with_suffix(".png")
    command = [inkscape, str(svg), "--export-type=png", f"--export-filename={png}", "--export-dpi=220"]
    subprocess.run(command, check=True, stdout=subprocess.DEVNULL)
    if index % 25 == 0 or index == len(svgs):
        print(f"Rendered {index}/{len(svgs)} diagrams")
