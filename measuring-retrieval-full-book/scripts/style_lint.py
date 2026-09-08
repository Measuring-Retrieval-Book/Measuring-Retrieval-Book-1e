#!/usr/bin/env python3
from pathlib import Path
import re
import sys

root = Path(__file__).resolve().parents[1]
files = sorted((root / "chapters").glob("*.md")) + sorted((root / "appendices").glob("*.md"))
files += sorted((root / "assets" / "diagrams").glob("*.svg"))
rules = {
    "unicode dash": re.compile(r"[\u2010\u2011\u2013\u2014\u2212]"),
}
hits = []
for path in files:
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        visible = re.sub(r"\]\([^)]*\)", "]", line) if path.suffix == ".md" else line
        for label, rule in rules.items():
            if rule.search(visible):
                hits.append((path.relative_to(root), number, label, visible.strip()))
for hit in hits:
    print(f"{hit[0]}:{hit[1]}: {hit[2]}: {hit[3]}")
print(f"Style findings: {len(hits)}")
sys.exit(1 if hits else 0)
