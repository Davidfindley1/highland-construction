# Highland Construction

Website for Highland Construction, a general construction company serving Northern Indiana and Southern Michigan. Founded by Derek Findley and led by brothers Derek and David Findley. Roofing is the lead work on the site, with a specialty in stone-coated metal shingles. General residential and commercial construction remains part of the offer.

**Live site:** https://myhighlandbuild.com/

**Email:** [info@myhighlandbuild.com](mailto:info@myhighlandbuild.com) · Derek: [derek@myhighlandbuild.com](mailto:derek@myhighlandbuild.com) · David: [david@myhighlandbuild.com](mailto:david@myhighlandbuild.com)

## Brand

- Teal: `#0F7462`
- Light blue: `#94CCF6`
- Typeface: [Josefin Sans](https://fonts.google.com/specimen/Josefin+Sans)
- Tagline: Building Excellence Every Day

## Pages

- [Home](https://myhighlandbuild.com/)
- [Stone-coated metal roofing](https://myhighlandbuild.com/roofing.html)
- [Financing](https://myhighlandbuild.com/financing.html)
- [Blog](https://myhighlandbuild.com/blog/)

Product research used to write the roofing pages lives in `_research/research-roofing.md` (not published on the live site). Photo licenses are in `CREDITS.md`. Photos in Our Work are from Highland Construction projects. Decorative stock photographs used as illustrations elsewhere are not Highland jobs and are captioned that way.

To add more project photos, drop files in `/workspace/highland-incoming/`, add captions in `scripts/work-photos.json`, and run `python3 scripts/process-work-photos.py` from the site root. The script strips EXIF/GPS, resizes, and compresses images for the gallery.

## Local preview

Open `index.html` in a browser, or serve the folder:

```bash
python3 -m http.server 8080
```
