#!/usr/bin/env python3
"""Generate per-article OG images for Die Zukunft news posts.

Reads the wireframe Swiss cross from the favicon SVG and composes a 1200x630
PNG with the brandmark, article title, and date. Renders via Inkscape so the
local Clash Display / Switzer fonts are picked up.

Usage:
    gen_article_og.py <slug> <out_dir> --de "Title DE" --fr "Title FR" \\
                      --it "Title IT" --en "Title EN" --date 2026-05-01
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FAVICON = ROOT / "avenir" / "static" / "favicon.svg"

W, H = 1200, 630
BRANDMARK = {
    "de": "die zukunft.",
    "fr": "le futur.",
    "it": "il futuro.",
    "en": "the future.",
}
NEWS_LABEL = {
    "de": "Aktuelles",
    "fr": "Actualités",
    "it": "Attualità",
    "en": "News",
}


def read_lines() -> list[tuple[float, float, float, float]]:
    """Parse <line> elements from the favicon SVG."""
    text = FAVICON.read_text()
    pat = re.compile(
        r'<line\s+x1="([-0-9.]+)"\s+y1="([-0-9.]+)"\s+x2="([-0-9.]+)"\s+y2="([-0-9.]+)"'
    )
    return [tuple(map(float, m.groups())) for m in pat.finditer(text)]


def xml_escape(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace(
        '"', "&quot;"
    ).replace("'", "&apos;")


def wrap_title(title: str, max_chars: int = 28) -> list[str]:
    words = title.split()
    lines: list[str] = []
    cur = ""
    for w in words:
        candidate = (cur + " " + w).strip()
        if len(candidate) <= max_chars:
            cur = candidate
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines[:4]


def format_date(iso: str, lang: str) -> str:
    y, m, d = iso.split("-")
    if lang == "en":
        months = ["", "January", "February", "March", "April", "May", "June",
                  "July", "August", "September", "October", "November", "December"]
        return f"{months[int(m)]} {int(d)}, {y}"
    return f"{int(d):02d}.{int(m):02d}.{y}"


def build_svg(title: str, date_iso: str, lang: str) -> str:
    lines = read_lines()
    # Cross watermark — center it behind text, scale it large, fade it.
    scale = 26
    cx, cy = W / 2, H / 2 + 30
    cross_lines = "\n".join(
        f'    <line x1="{x1*scale:.1f}" y1="{y1*scale:.1f}" x2="{x2*scale:.1f}" y2="{y2*scale:.1f}"/>'
        for (x1, y1, x2, y2) in lines
    )
    title_lines = wrap_title(title)
    line_h = 78
    n = len(title_lines)
    title_block_h = n * line_h
    title_top = (H - title_block_h) / 2 + 60
    title_tspans = "\n".join(
        f'      <tspan x="80" y="{title_top + i*line_h:.0f}">{xml_escape(t)}</tspan>'
        for i, t in enumerate(title_lines)
    )
    brandmark = BRANDMARK[lang]
    label = NEWS_LABEL[lang].upper()
    date_str = format_date(date_iso, lang)

    return f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <defs>
    <linearGradient id="g" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#a855f7"/>
      <stop offset="50%" stop-color="#3b82f6"/>
      <stop offset="100%" stop-color="#06b6d4"/>
    </linearGradient>
  </defs>
  <rect width="{W}" height="{H}" fill="#ffffff"/>
  <g fill="none" stroke="url(#g)" stroke-width="1.4" stroke-linecap="round" opacity="0.18" transform="translate({cx},{cy})">
{cross_lines}
  </g>
  <text x="80" y="92" font-family="Clash Display, ClashDisplay" font-weight="700" font-size="42" fill="url(#g)">{xml_escape(brandmark)}</text>
  <text x="80" y="138" font-family="Switzer" font-weight="500" font-size="22" fill="#6b7280" letter-spacing="3">{xml_escape(label)}</text>
  <text font-family="Clash Display, ClashDisplay" font-weight="700" font-size="64" fill="#0f172a">
{title_tspans}
  </text>
  <rect x="80" y="{H-110}" width="80" height="4" fill="url(#g)" rx="2"/>
  <text x="80" y="{H-70}" font-family="Switzer" font-weight="500" font-size="24" fill="#475569">{xml_escape(date_str)}</text>
  <text x="{W-80}" y="{H-70}" text-anchor="end" font-family="Switzer" font-weight="500" font-size="22" fill="#94a3b8">die-zukunft.ch</text>
</svg>
'''


def render(svg_path: Path, png_path: Path) -> None:
    subprocess.run(
        ["inkscape", str(svg_path), "--export-type=png",
         f"--export-filename={png_path}", f"--export-width={W}", f"--export-height={H}"],
        check=True, capture_output=True,
    )


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("slug")
    p.add_argument("out_dir")
    p.add_argument("--date", required=True)
    p.add_argument("--de", required=True)
    p.add_argument("--fr", required=True)
    p.add_argument("--it", required=True)
    p.add_argument("--en", required=True)
    p.add_argument("--keep-svg", action="store_true")
    args = p.parse_args()

    titles = {"de": args.de, "fr": args.fr, "it": args.it, "en": args.en}
    out = Path(args.out_dir)
    out.mkdir(parents=True, exist_ok=True)

    for lang, title in titles.items():
        svg = build_svg(title, args.date, lang)
        svg_path = out / f"{args.slug}.{lang}.svg"
        png_path = out / f"{args.slug}.{lang}.png"
        svg_path.write_text(svg)
        render(svg_path, png_path)
        if not args.keep_svg:
            svg_path.unlink()
        print(f"  → {png_path}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
