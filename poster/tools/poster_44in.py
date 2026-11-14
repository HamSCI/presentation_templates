#!/usr/bin/env python3
"""Re-lay a finished 48 x 36 in HamSCI poster out at 44 x 36 in, keeping every font size.

Why: AGU limits posters to 44 in wide in 2026. This repository ships 44 x 36 in
templates (make_44in_templates.py) and an even-shrink tool (scale_pptx.py, 44 x 33 in, fonts at
11/12). This script gives a finished poster the same geometry as the 44 in template, without
shrinking fonts or the height:

  - the slide becomes 44 in wide; nothing moves vertically;
  - the full-width bars (Rectangle 21, Rectangle 3) shrink to 44 in;
  - a full-width banner photo (Picture 11) keeps its height and loses 4 in at its right edge
    (a crop, as in the template); a banner that is not full width is mapped like content;
  - everything between the 0.59 in side margins is mapped linearly from [0.59, 47.41] to
    [0.59, 43.41] in (factor 0.9146), which puts the three template columns exactly where the
    44 in template has them (left edges 0.59, 15.00, 29.41 in; width 14.00 in);
  - pictures, charts and groups scale evenly about their centre (no distortion); text boxes
    and panels get the new left edge and width and keep their height;
  - fonts, indents and fixed line spacing inside the content scale by the same factor, so every
    text box wraps exactly as it did at 48 in and nothing overflows (a 28 pt font becomes
    25.6 pt). The title, author bar and footer keep their fonts. --keep-fonts turns this off,
    for a poster you will re-flow by hand;
  - a title box with no banner photo behind it (TextBox 12 on a poster without a full-width
    Picture 11) widens to the slide's margins instead, so it keeps its font and line count;
  - the footer: the email box stays, the conference-name box follows the right edge, and the
    other footer items (y > 34.4 in) keep their order and gaps from the left, shifted as
    --footer-shift says (default: centred, -2 in).

Only top-level shapes are moved; children of a group follow the group.

Usage:
    python3 poster/tools/poster_44in.py IN.pptx OUT.pptx [--footer-shift -2] [--keep-fonts]

Standard library only. Open the result in PowerPoint and check it before printing.
"""
import argparse
import re
import zipfile

EMU = 914400
OLD_W, NEW_W = 48 * EMU, 44 * EMU
M = round(0.59 * EMU)                       # side margin kept
K = (NEW_W - 2 * M) / (OLD_W - 2 * M)        # content factor
FOOTER_Y = round(34.4 * EMU)

XFRM = re.compile(r'(<a:off x=")(-?\d+)(" y=")(-?\d+)("/><a:ext cx=")(\d+)(" cy=")(\d+)("/>)')
TOP = re.compile(r'<(p:sp|p:pic|p:grpSp|p:cxnSp|p:graphicFrame)>')


def top_level_shapes(xml):
    """Yield (start, end, tag) of each top-level shape in the slide's spTree."""
    tree_start = xml.index('<p:spTree>')
    tree_end = xml.rindex('</p:spTree>')
    i = xml.index('</p:grpSpPr>', tree_start) + len('</p:grpSpPr>')
    while True:
        m = TOP.search(xml, i, tree_end)
        if not m:
            return
        tag = m.group(1)
        depth, j = 0, m.start()
        for t in re.finditer(rf'<{tag}>|</{tag}>', xml[m.start():tree_end]):
            depth += -1 if t.group(0)[1] == '/' else 1
            if depth == 0:
                j = m.start() + t.end()
                break
        yield m.start(), j, tag
        i = j


def name_of(el):
    m = re.search(r'<p:cNvPr id="\d+" name="([^"]*)"', el)
    return m.group(1) if m else ''


def mapx(x):
    return round(M + (x - M) * K)


SZ = re.compile(r'(<a:(?:rPr|defRPr|endParaRPr)\b[^>]*?\bsz=")(\d+)(")')
MARL = re.compile(r'(<a:(?:pPr|lvl\dpPr)\b[^>]*?\bmarL=")(-?\d+)(")')
INDENT = re.compile(r'(<a:(?:pPr|lvl\dpPr)\b[^>]*?\bindent=")(-?\d+)(")')
SPC = re.compile(r'(<a:spcPts val=")(\d+)(")')


def scale_fonts(el, k):
    el = SZ.sub(lambda m: f'{m.group(1)}{max(100, round(int(m.group(2)) * k))}{m.group(3)}', el)
    for rx in (MARL, INDENT):
        el = rx.sub(lambda m: f'{m.group(1)}{round(int(m.group(2)) * k)}{m.group(3)}', el)
    return SPC.sub(lambda m: f'{m.group(1)}{round(int(m.group(2)) * k)}{m.group(3)}', el)


def crop_right(el, frac):
    """Hide a further `frac` of the picture's visible width at its right edge, keeping any crop."""
    m = re.search(r'<a:srcRect\b([^>]*)/>', el)
    attrs = dict(re.findall(r'(\w+)="(-?\d+)"', m.group(1))) if m else {}
    l, r = int(attrs.get('l', 0)), int(attrs.get('r', 0))
    attrs['r'] = str(round(r + (100000 - l - r) * frac))
    tag = '<a:srcRect ' + ' '.join(f'{k}="{v}"' for k, v in attrs.items()) + '/>'
    if m:
        return el[:m.start()] + tag + el[m.end():]
    return el.replace('<a:stretch>', tag + '<a:stretch>', 1)


def relayout(xml, footer_shift, fonts=True):
    banner = any(name_of(xml[s:e]) == 'Picture 11' and
                 int(XFRM.search(xml[s:e]).group(6)) >= OLD_W - EMU // 100
                 for s, e, _ in top_level_shapes(xml) if XFRM.search(xml[s:e]))
    out, last = [], 0
    for s, e, tag in top_level_shapes(xml):
        el = xml[s:e]
        m = XFRM.search(el)
        if not m:
            continue
        x, y, cx, cy = int(m.group(2)), int(m.group(4)), int(m.group(6)), int(m.group(8))
        name = name_of(el)
        nx, ny, ncx, ncy = x, y, cx, cy
        crop_banner = False
        full_width = cx >= OLD_W - EMU // 100
        if name in ('Rectangle 21', 'Rectangle 3') and full_width:
            ncx = cx - (OLD_W - NEW_W)
        elif name == 'Picture 11' and full_width:
            ncx = cx - (OLD_W - NEW_W)
            crop_banner = True
        elif name == 'TextBox 12' and not banner:
            nx, ncx = M, NEW_W - 2 * M                 # no banner: title spans the margins
        elif name == 'TextBox 12':
            ncx = cx - (OLD_W - NEW_W)                 # title keeps its left edge
        elif name == 'TextBox 36':
            nx = x - (OLD_W - NEW_W)                   # conference name follows the right edge
        elif name == 'TextBox 66':
            pass                                       # email stays at the left
        elif y >= FOOTER_Y:
            nx = x + round(footer_shift * EMU)         # footer logos
        elif tag in ('p:sp', 'p:cxnSp') and '<p:txBody>' in el or tag == 'p:cxnSp':
            nx, ncx = mapx(x), round(cx * K)           # text keeps its height
            if fonts:
                el = scale_fonts(el, K)
        else:                                          # pictures, charts, groups, shapes
            ncx, ncy = round(cx * K), round(cy * K)
            cxm = mapx(x + cx / 2)
            nx, ny = round(cxm - ncx / 2), round(y + (cy - ncy) / 2)
            if fonts:
                el = scale_fonts(el, K)
        el = el[:m.start()] + f'{m.group(1)}{nx}{m.group(3)}{ny}{m.group(5)}{ncx}{m.group(7)}{ncy}{m.group(9)}' + el[m.end():]
        if crop_banner:
            el = crop_right(el, (OLD_W - NEW_W) / OLD_W)
        out.append(xml[last:s])
        out.append(el)
        last = e
    out.append(xml[last:])
    return ''.join(out)


def scale_x(xml, k):
    xml = re.sub(r'<a:off x="(-?\d+)"', lambda m: f'<a:off x="{round(int(m.group(1)) * k)}"', xml)
    return re.sub(r'<a:ext cx="(\d+)"', lambda m: f'<a:ext cx="{round(int(m.group(1)) * k)}"', xml)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('src')
    ap.add_argument('dst')
    ap.add_argument('--footer-shift', type=float, default=-2.0, help='inches; default centres')
    ap.add_argument('--keep-fonts', action='store_true', help='do not scale content fonts')
    a = ap.parse_args()
    zin = zipfile.ZipFile(a.src)
    with zipfile.ZipFile(a.dst, 'w', zipfile.ZIP_DEFLATED) as zout:
        for info in zin.infolist():
            data = zin.read(info.filename)
            n = info.filename
            if n == 'ppt/presentation.xml':
                t = data.decode('utf8')
                assert f'<p:sldSz cx="{OLD_W}"' in t, 'not a 48 in wide poster'
                data = t.replace(f'<p:sldSz cx="{OLD_W}"', f'<p:sldSz cx="{NEW_W}"', 1).encode('utf8')
            elif re.match(r'ppt/slides/slide\d+\.xml$', n):
                data = relayout(data.decode('utf8'), a.footer_shift, not a.keep_fonts).encode('utf8')
            elif re.match(r'ppt/(slideLayouts|slideMasters)/[^/]+\.xml$', n):
                data = scale_x(data.decode('utf8'), NEW_W / OLD_W).encode('utf8')
            zout.writestr(info, data)


if __name__ == '__main__':
    main()
