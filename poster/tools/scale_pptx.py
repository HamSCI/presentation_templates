#!/usr/bin/env python3
"""Scale a PowerPoint poster to a new width, keeping its layout and aspect ratio exactly.

Why: AGU requires posters no more than 44 in wide (AGU26, 2026). The HamSCI poster template
is 48 x 36 in. Scaling everything on the slide by 44/48 gives a 44 x 33 in poster that
looks exactly like the original, line breaks included, because positions, sizes, font sizes,
indents, text insets and line widths all shrink by the same factor. Use it to make the
44 in template versions, or to convert a poster already built on the 48 in template.

What is scaled, in the slide size and in every slide, layout and master:
  - shape positions and sizes      <a:off>, <a:ext>, <a:chOff>, <a:chExt>  (x, y, cx, cy)
  - font sizes and kerning limits  sz, kern
  - paragraph indents and margins  marL, marR, indent, defTabSz
  - text box insets                lIns, tIns, rIns, bIns
  - character spacing              spc on run properties
  - line spacing given in points   <a:spcPts val>
  - outline widths                 <a:ln w>
Relative quantities (percentages, picture crops, shape adjustments, colours) are unchanged.
Font sizes are kept to the hundredth of a point, as PowerPoint stores them, so a 72 pt
title becomes 66 pt and a 28 pt body becomes 25.67 pt.

Usage:
    python3 scale_pptx.py IN.pptx OUT.pptx [--width 44]

Only the standard library is needed. Check the result by opening it in PowerPoint.
"""
import argparse
import re
import zipfile

EMU_PER_INCH = 914400

# Attributes holding a length (EMU) or a size in hundredths of a point, which scale linearly.
SCALED_ATTRS = ('x', 'y', 'cx', 'cy', 'sz', 'kern', 'marL', 'marR', 'indent', 'defTabSz',
                'lIns', 'tIns', 'rIns', 'bIns')
# Elements whose x/y/cx/cy are geometry (x/y appear nowhere else in DrawingML text we touch,
# but restrict them anyway).
GEOM_TAGS = ('a:off', 'a:ext', 'a:chOff', 'a:chExt', 'p:sldSz')
SCALED_PARTS = re.compile(r'^ppt/(slides|slideLayouts|slideMasters)/[^/]+\.xml$')

TAG_RE = re.compile(r'<([A-Za-z0-9]+:[A-Za-z0-9]+)(\s[^<>]*?)(/?)>')
ATTR_RE = re.compile(r'(\s)([A-Za-z]+)="(-?\d+)"')


def scale_tag(m, k):
    tag, attrs, close = m.group(1), m.group(2), m.group(3)

    def sub(am):
        name, val = am.group(2), int(am.group(3))
        scale = False
        if name in ('x', 'y', 'cx', 'cy'):
            scale = tag in GEOM_TAGS
        elif name in SCALED_ATTRS:
            scale = True
        elif name == 'spc':
            scale = tag in ('a:rPr', 'a:defRPr', 'a:endParaRPr')
        elif name == 'val':
            scale = tag == 'a:spcPts'
        elif name == 'w':
            scale = tag == 'a:ln'
        if not scale:
            return am.group(0)
        return f'{am.group(1)}{name}="{round(val * k)}"'

    return f'<{tag}{ATTR_RE.sub(sub, attrs)}{close}>'


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('src')
    ap.add_argument('dst')
    ap.add_argument('--width', type=float, default=44.0,
                    help='new slide width in inches (default 44); height follows')
    args = ap.parse_args()

    zin = zipfile.ZipFile(args.src)
    pres = zin.read('ppt/presentation.xml').decode('utf8')
    cx, cy = (int(v) for v in re.search(r'<p:sldSz cx="(\d+)" cy="(\d+)"', pres).groups())
    k = args.width * EMU_PER_INCH / cx

    with zipfile.ZipFile(args.dst, 'w', zipfile.ZIP_DEFLATED) as zout:
        for info in zin.infolist():
            data = zin.read(info.filename)
            if info.filename == 'ppt/presentation.xml' or SCALED_PARTS.match(info.filename):
                text = data.decode('utf8')
                if info.filename == 'ppt/presentation.xml':
                    # Only the slide size; the notes page size stays as it was.
                    text = re.sub(r'<p:sldSz [^>]*>', lambda m: scale_tag(TAG_RE.match(m.group(0)), k), text)
                else:
                    text = TAG_RE.sub(lambda m: scale_tag(m, k), text)
                data = text.encode('utf8')
            zout.writestr(info, data)

    print(f'{args.src}: {cx / EMU_PER_INCH:g} x {cy / EMU_PER_INCH:g} in -> '
          f'{args.dst}: {cx * k / EMU_PER_INCH:g} x {cy * k / EMU_PER_INCH:g} in '
          f'(scale {k:.4f})')


if __name__ == '__main__':
    main()
