#!/usr/bin/env python3
"""Shrink a PowerPoint file by re-encoding oversized opaque PNG images as cropped JPEGs.

Why: the HamSCI poster templates arrived at ~70 MB each because the banner photo was stored
as a 19355 x 2592 RGBA PNG (~69 MB). PNG is lossless and barely compresses a photograph,
the alpha channel was unused (fully opaque), and PowerPoint's crop hid 59 % of the pixels
without removing them from the file. This script fixes all three, so the file is ~5 MB
with no visible change.

For every PNG in ppt/media/ larger than --min-mb that is fully opaque:
  1. If every picture that uses it applies the same crop (<a:srcRect>), bake that crop
     into the pixels and clear the crop in the XML, so the slide looks the same.
  2. Drop the alpha channel and save as JPEG (default quality 95, 4:4:4 chroma, i.e. no
     colour subsampling) at full resolution, unless --max-dpi asks for downsampling.
  3. Point every relationship at the new .jpeg and register the jpeg content type.

Images with real transparency, and small images, are left untouched. Run it again after
re-saving a template in PowerPoint if the file has grown.

Usage:
    python3 shrink_pptx.py IN.pptx OUT.pptx [--quality 95] [--min-mb 2] [--max-dpi 0]

Requires Pillow. Check the result by opening it in PowerPoint.
"""
import argparse
import io
import posixpath
import re
import zipfile

from PIL import Image

Image.MAX_IMAGE_PIXELS = None
EMU_PER_INCH = 914400


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('src')
    ap.add_argument('dst')
    ap.add_argument('--quality', type=int, default=95, help='JPEG quality (default 95)')
    ap.add_argument('--min-mb', type=float, default=2.0,
                    help='only re-encode PNGs larger than this (default 2 MB)')
    ap.add_argument('--max-dpi', type=float, default=0,
                    help='downsample images shown above this resolution (default 0 = never)')
    args = ap.parse_args()

    zin = zipfile.ZipFile(args.src)
    names = zin.namelist()
    texts = {n: zin.read(n).decode('utf8') for n in names if n.endswith(('.xml', '.rels'))}

    replaced = {}  # media path -> new media path
    new_media = {}
    for media in names:
        if not (media.startswith('ppt/media/') and media.lower().endswith('.png')):
            continue
        if zin.getinfo(media).file_size < args.min_mb * 1e6:
            continue
        im = Image.open(io.BytesIO(zin.read(media)))
        if im.mode in ('RGBA', 'LA') and im.getchannel('A').getextrema()[0] < 255:
            print(f'skip {media}: uses transparency')
            continue
        if im.mode == 'P' and 'transparency' in im.info:
            print(f'skip {media}: uses transparency')
            continue

        # Every (part, rId) that points at this image, and every <p:pic> using it.
        uses = []
        for rels_name, rels in texts.items():
            if not rels_name.endswith('.rels'):
                continue
            part_dir = posixpath.dirname(posixpath.dirname(rels_name))
            part = posixpath.join(part_dir, posixpath.basename(rels_name)[:-5])
            for rid, target in re.findall(r'Id="(rId\d+)"[^>]*?Target="([^"]+)"', rels):
                if posixpath.normpath(posixpath.join(part_dir, target)) == media:
                    for pic in re.findall(r'<p:pic>.*?</p:pic>', texts.get(part, ''), re.S):
                        if f'r:embed="{rid}"' in pic:
                            uses.append((part, pic))

        crops = {(re.search(r'<a:srcRect[^>]*>', pic) or [''])[0] for _, pic in uses}
        W, H = im.size
        box = (0, 0, W, H)
        if len(crops) == 1 and uses:
            crop = {k: int(v) / 1e5 for k, v in re.findall(r'\b([ltrb])="(-?\d+)"', crops.pop())}
            if all(v >= 0 for v in crop.values()):
                box = (round(W * crop.get('l', 0)), round(H * crop.get('t', 0)),
                       round(W * (1 - crop.get('r', 0))), round(H * (1 - crop.get('b', 0))))
        out = im.convert('RGB').crop(box)

        if args.max_dpi and uses:
            widest = max(int(re.search(r'<a:ext cx="(\d+)"', p).group(1)) for _, p in uses)
            dpi = out.width / (widest / EMU_PER_INCH)
            if dpi > args.max_dpi:
                scale = args.max_dpi / dpi
                out = out.resize((round(out.width * scale), round(out.height * scale)),
                                 Image.LANCZOS)

        buf = io.BytesIO()
        out.save(buf, 'JPEG', quality=args.quality, subsampling=0, optimize=True)
        new_name = media[:-4] + '.jpeg'
        while new_name in names or new_name in new_media:
            new_name = new_name[:-5] + '_s.jpeg'
        new_media[new_name] = buf.getvalue()
        replaced[media] = new_name

        if box != (0, 0, W, H):  # crop is now in the pixels; clear it in the XML
            for part, pic in uses:
                texts[part] = texts[part].replace(
                    pic, re.sub(r'<a:srcRect[^>]*/>', '<a:srcRect/>', pic))
        print(f'{media}: {W}x{H} {im.mode} {zin.getinfo(media).file_size / 1e6:.1f} MB -> '
              f'{new_name}: {out.width}x{out.height} RGB {len(buf.getvalue()) / 1e6:.1f} MB '
              f'({len(uses)} use(s))')

    if not replaced:
        print('nothing to shrink')
    for rels_name in [n for n in texts if n.endswith('.rels')]:
        for old, new in replaced.items():
            texts[rels_name] = texts[rels_name].replace(
                posixpath.basename(old) + '"', posixpath.basename(new) + '"')
    ct = texts['[Content_Types].xml']
    if replaced and 'Extension="jpeg"' not in ct:
        texts['[Content_Types].xml'] = ct.replace(
            '<Default ', '<Default Extension="jpeg" ContentType="image/jpeg"/><Default ', 1)

    with zipfile.ZipFile(args.dst, 'w') as zout:
        for name in names:
            if name in replaced:
                zout.writestr(replaced[name], new_media[replaced[name]], zipfile.ZIP_STORED)
                continue
            data = texts[name].encode('utf8') if name in texts else zin.read(name)
            method = zipfile.ZIP_STORED if name.startswith('ppt/media/') else zipfile.ZIP_DEFLATED
            zout.writestr(name, data, method)


if __name__ == '__main__':
    main()
