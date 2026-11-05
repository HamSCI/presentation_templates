# 2026-11-05: Adding the poster templates

## What came in

N. A. Frissell supplied two PowerPoint poster templates: `HamSCI Poster Template.pptx`
(blue, for everyone) and `HamSCI Scranton Poster Template.pptx` (purple, for Scranton authors).
Each was 69.7 MB. They differ only in accent color (`254160` vs `5F4A7A`, plus `accent1` vs
`accent4` theme colors in two places), the first affiliation ("Institution One" vs "University
of Scranton"), and the email domain. They share byte-identical media.

## Why they were 70 MB

`ppt/media/image1.png`, the rooftop silhouette banner, was 69.4 MB of the 69.7:
- 19355 × 2592 pixels, RGBA, shown 48 × 4.77 in
- the alpha channel was unused (every pixel opaque)
- PowerPoint's crop (`srcRect t=40.673% r=20.119%`) hid 59 % of the pixels, which were still stored
- it's a noisy photograph, which PNG can't compress well

## What was done

`poster/tools/shrink_pptx.py` bakes the crop into the pixels and clears it in the XML. It
drops alpha and saves a JPEG (q95, 4:4:4) at the full visible resolution, 15461 × 1538, about
322 dpi as printed. Result: 5.1 MB image, 5.4 MB file.

Quality checks:
- 1:1 side-by-side of the people and antenna region, and of a contrast-stretched sky region
  (looking for banding): no visible difference. PSNR of q95 vs the original pixels: 43.6 dB.
- LibreOffice renders of the original and shrunk files at 100 dpi: only 0.06 % of pixels differ
  by more than 8/255, all inside the banner. Text, layout, logos and colors are identical.
- Re-running the script on its own output does nothing.

Options considered: lossless crop + PNG gave 26 MB; JPEG q90 gave 2.6 MB (PSNR 42.6);
downsampling to 200 dpi + q95 gave 1.6 MB. We kept full resolution at q95, since 5 MB is easy
to keep in git and leaves room for very large prints.

## Open

- The shrunk files were checked in LibreOffice, not PowerPoint. Someone should open both in
  PowerPoint before relying on them.
- There's no Beamer or LaTeX poster version yet. CLAUDE.md says the PowerPoint file is the
  reference design for any future one.
- The banner photo is presumed to be the same KC2KRQ rooftop photograph credited for the oral
  template; confirm.
