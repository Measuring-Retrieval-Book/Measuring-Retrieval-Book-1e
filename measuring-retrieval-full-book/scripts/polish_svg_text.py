#!/usr/bin/env python3
"""Apply the book's direct-prose rules to visible SVG text."""

from pathlib import Path
import re


root = Path(__file__).resolve().parents[1]
diagram_dir = root / "assets" / "diagrams"

exact = {
    "Why not just fill those in?": "Why leave those fields open?",
    "a natural extension rather than a published result": "a natural extension from the published result",
    "precision as though": "precision with",
    "rather than letting the line continue": "and reset the historical line",
    "The ranking is correct though.": "The ranking is correct.",
    "Correct but ungrounded.": "Correct and ungrounded.",
    "Correct-but-ungrounded": "Correct and ungrounded",
    "necessity, not just presence": "citation necessity",
    "Effect size and confidence interval, not just p": "Effect size and confidence interval",
    "good published answer to online RAG evaluation yet": "published answer to online RAG evaluation",
    "JUDGE DRIFT PROTOCOL (no published metric yet)": "JUDGE DRIFT PROTOCOL",
    "...but every rank metric needs to know": "...every rank metric needs to know",
    "But B might have been relevant!": "B might have been relevant!",
    "But the same documents were retrieved.": "The same documents were retrieved.",
}

patterns = [
    (re.compile(r"\bvs\.\b", re.I), "and"),
    (re.compile(r"\bvs\b", re.I), "and"),
    (re.compile(r"\bversus\b", re.I), "and"),
    (re.compile(r"\bnot just\b", re.I), ""),
    (re.compile(r"\brather than\b", re.I), "using"),
    (re.compile(r"\bas though\b", re.I), "with"),
    (re.compile(r"\bhowever\b,?", re.I), ""),
    (re.compile(r"\bbut\b", re.I), "and"),
    (re.compile(r"\bthough\b", re.I), ""),
    (re.compile(r"\byet\b", re.I), ""),
]

changed = 0
for path in sorted(diagram_dir.glob("*.svg")):
    text = path.read_text(encoding="utf-8")
    revised = text
    for old, new in exact.items():
        revised = revised.replace(old, new)
    for pattern, replacement in patterns:
        revised = pattern.sub(replacement, revised)
    if revised != text:
        path.write_text(revised, encoding="utf-8")
        changed += 1

print(f"Polished visible text in {changed} SVG files")
