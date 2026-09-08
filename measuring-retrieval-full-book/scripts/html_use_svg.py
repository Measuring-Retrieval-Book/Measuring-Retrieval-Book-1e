#!/usr/bin/env python3
"""Point the HTML edition at the SVG diagram masters.

The PDF build needs rasterized PNGs, and a browser is better served by the vector
originals: they stay sharp at any zoom and the whole set is 828K rather than 31M.
Only assets/diagrams/ is switched, since the slide plates are genuine raster images.
"""
import re
import sys
from pathlib import Path

for name in sys.argv[1:]:
    path = Path(name)
    html = path.read_text(encoding="utf-8")
    swapped, count = re.subn(
        r'(src="assets/diagrams/[^"]+?)\.png(")',
        r"\1.svg\2",
        html,
    )
    path.write_text(swapped, encoding="utf-8")
    print(f"{path.name}: {count} diagram references switched to SVG")
