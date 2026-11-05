# HamSCI Poster Template

The HamSCI poster design, a 48 × 36 in (landscape) PowerPoint template, in two versions:

| File | For | Accent color |
|---|---|---|
| [`pptx/hamsci_poster_template.pptx`](pptx/hamsci_poster_template.pptx) | everyone | HamSCI blue `#254160` |
| [`pptx/hamsci_scranton_poster_template.pptx`](pptx/hamsci_scranton_poster_template.pptx) | University of Scranton authors | Scranton purple `#5F4A7A` |

![The two poster templates: HamSCI blue (left) and Scranton purple (right)](preview.png)

The layout is the same in both: the rooftop-silhouette banner with the title, an author and
affiliation bar, three rounded columns (Abstract and Introduction; Method/Experiment and Data
and Analysis; Conclusion, References and Acknowledgements), and a footer with the contact
email, partner logos and conference name. The Scranton version fills in "University of
Scranton" as the first affiliation and a `@scranton.edu` email.

## Using it

Open the template for your group and save a copy under your poster's name. Replace the
placeholder text, and keep "Data and Analysis" the largest section. The slide is 48 × 36 in
(4 × 3 ft); a printer can scale it to any other 4:3 size. For a different shape, change the slide
size before adding content.

## Keeping the file small

The templates are about 5 MB. As first made they were about 70 MB, almost all of it one
picture: the banner photo, stored as a 19355 × 2592 PNG with an unused transparency channel,
59 % of it hidden by PowerPoint's crop. [`tools/shrink_pptx.py`](tools/shrink_pptx.py) trims
the hidden part, drops the unused channel, and saves the photo as a quality-95 JPEG at full
resolution (about 320 dpi as printed). That shows no visible difference, including in the sky
gradient.

Your poster's own large pictures can bloat it the same way. If a poster grows past a few tens of
MB, run:

```bash
python3 poster/tools/shrink_pptx.py my_poster.pptx my_poster_small.pptx
```

It only touches PNGs over 2 MB that have no transparency, and it leaves everything else alone.
`--max-dpi 200` also downsamples images shown above 200 dpi, which is still plenty for a
poster. Open the result in PowerPoint and check it before you print. The script needs Python 3
and Pillow (`pip install pillow`).

## Images

As in the oral template, the rooftop silhouette photograph is by Ann Marie
Rogalcheck-Frissell, KC2KRQ, and the partner logos belong to their institutions. They are not covered by the MIT license; use
them for HamSCI posters.
