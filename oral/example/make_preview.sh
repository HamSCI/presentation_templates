#!/usr/bin/env bash
# Rebuild the example talk and tile its slides into preview.png for the README.
# Needs latexmk, pdftoppm (poppler) and montage (ImageMagick).
set -euo pipefail
cd "$(dirname "$0")"
latexmk -quiet hamsci_example_talk.tex
tmp="$(mktemp -d)"
trap 'rm -r "$tmp"' EXIT
pdftoppm -r 72 -png hamsci_example_talk.pdf "$tmp/slide"
montage "$tmp"/slide-*.png -tile 3x -geometry +4+4 -background '#c8c8c8' preview.png
