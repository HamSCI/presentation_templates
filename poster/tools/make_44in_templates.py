#!/usr/bin/env python3
"""Make the AGU-compliant 44 x 36 in poster templates from the 48 x 36 in ones.

Why: AGU requires posters no more than 44 in wide (AGU26, 2026). This re-lays the template
out 4 in narrower and changes nothing vertically, so the height (36 in), every font size and
every vertical position stay as in the 48 in design:
  - the banner photo keeps its height and loses 4 in of plain sky at its right edge
    (a PowerPoint crop, so the photo is not squashed and the pixels are untouched);
  - the title box, the author bar, the footer bar and the conference-name box move or
    shrink with the right edge;
  - the three columns keep their outer margins and the gaps between them and narrow from
    15.33 in to 14.00 in each;
  - the partner-logo strip stays centred on the slide, as it is in the 48 in version;
  - layout and master placeholders (used only for slides added later) are scaled
    horizontally by 44/48.

Shapes are found by their names in the 48 in template, so this script is tied to that
template. After editing a 48 in template, re-run it and check the 44 in result in PowerPoint:

    python3 poster/tools/make_44in_templates.py

Only the standard library is needed.
"""
import pathlib
import re
import zipfile

EMU = 914400
OLD_W, NEW_W = 48 * EMU, 44 * EMU
DW = NEW_W - OLD_W                       # -4 in

PPTX = pathlib.Path(__file__).resolve().parent.parent / 'pptx'
TEMPLATES = ['hamsci_poster_template', 'hamsci_scranton_poster_template']


def shape_span(xml, name, nth=0):
    """Return (start, end) of the nth <p:sp>/<p:pic>/<p:grpSp> element whose cNvPr has this name."""
    i = -1
    for _ in range(nth + 1):
        i = xml.index(f'name="{name}"', i + 1)
    start = max(xml.rfind(t, 0, i) for t in ('<p:sp>', '<p:pic>', '<p:grpSp>'))
    tag = xml[start + 1:xml.index('>', start)]
    depth = 0
    for m in re.finditer(rf'<{tag}>|</{tag}>', xml[start:]):
        depth += -1 if m.group(0)[1] == '/' else 1
        if depth == 0:
            return start, start + m.end()
    raise ValueError(name)


XFRM = re.compile(r'<a:off x="(-?\d+)" y="(-?\d+)"/><a:ext cx="(\d+)" cy="(\d+)"/>')


def get_xfrm(xml, name, nth=0):
    """(x, y, cx, cy) of the nth shape called `name` (its own, top-level transform)."""
    start, end = shape_span(xml, name, nth)
    return tuple(map(int, XFRM.search(xml, start, end).groups()))


def edit_xfrm(xml, name, nth=0, x=None, dx=0, cx=None, dcx=0, extra=None):
    """Change the x offset and/or width of the nth shape called `name`."""
    start, end = shape_span(xml, name, nth)
    el = xml[start:end]
    m = XFRM.search(el)
    ox, oy, ocx, ocy = map(int, m.groups())
    nx = (ox if x is None else x) + dx
    ncx = (ocx if cx is None else cx) + dcx
    el = el[:m.start()] + f'<a:off x="{nx}" y="{oy}"/><a:ext cx="{ncx}" cy="{ocy}"/>' + el[m.end():]
    if extra:
        el = extra(el)
    return xml[:start] + el + xml[end:]


def relayout_slide(xml):
    # Full-width bars.
    for name in ('Rectangle 21', 'Rectangle 3'):
        xml = edit_xfrm(xml, name, dcx=DW)
    # Banner photo: crop the right 4 in instead of squashing it.
    crop = round(-DW / OLD_W * 100000)
    xml = edit_xfrm(xml, 'Picture 11', dcx=DW,
                    extra=lambda el: el.replace('<a:srcRect/>', f'<a:srcRect r="{crop}"/>', 1))
    # Title box keeps its left edge and its offset from the right edge.
    xml = edit_xfrm(xml, 'TextBox 12', dcx=DW)
    # Conference name (right-aligned) follows the right edge.
    xml = edit_xfrm(xml, 'TextBox 36', dx=DW)
    # Three columns: keep the left margin and the gap between columns, narrow the columns.
    cols = ('Rounded Rectangle 25', 'Rounded Rectangle 56', 'Rounded Rectangle 57')
    (x0, _, w0, _), (x1, _, _, _) = get_xfrm(xml, cols[0]), get_xfrm(xml, cols[1])
    margin, gap = x0, x1 - (x0 + w0)
    col_w = (NEW_W - 2 * margin - 2 * gap) // 3
    for k, name in enumerate(cols):
        xml = edit_xfrm(xml, name, x=margin + k * (col_w + gap), cx=col_w)
    # Partner-logo strip: all the logos are in one group, centred on the slide. Keep it centred.
    x, _, cx, _ = get_xfrm(xml, 'Group 1')
    xml = edit_xfrm(xml, 'Group 1', x=(NEW_W - cx) // 2)   # children follow (chOff unchanged)
    return xml


def scale_x(xml, k):
    """Scale horizontal geometry of layout/master placeholders by k."""
    xml = re.sub(r'<a:off x="(-?\d+)"', lambda m: f'<a:off x="{round(int(m.group(1)) * k)}"', xml)
    return re.sub(r'<a:ext cx="(\d+)"', lambda m: f'<a:ext cx="{round(int(m.group(1)) * k)}"', xml)


def convert(src, dst):
    zin = zipfile.ZipFile(src)
    with zipfile.ZipFile(dst, 'w', zipfile.ZIP_DEFLATED) as zout:
        for info in zin.infolist():
            data = zin.read(info.filename)
            n = info.filename
            if n == 'ppt/presentation.xml':
                t = data.decode('utf8')
                assert f'<p:sldSz cx="{OLD_W}"' in t, f'{src} is not 48 in wide'
                data = t.replace(f'<p:sldSz cx="{OLD_W}"', f'<p:sldSz cx="{NEW_W}"', 1).encode('utf8')
            elif n == 'ppt/slides/slide1.xml':
                data = relayout_slide(data.decode('utf8')).encode('utf8')
            elif re.match(r'ppt/(slideLayouts|slideMasters)/[^/]+\.xml$', n):
                data = scale_x(data.decode('utf8'), NEW_W / OLD_W).encode('utf8')
            zout.writestr(info, data)
    print(f'{src.name} -> {dst.name}')


if __name__ == '__main__':
    for t in TEMPLATES:
        convert(PPTX / f'{t}.pptx', PPTX / f'{t}_44in.pptx')
