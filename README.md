# ✦ Y2K Art Archive

Two sister concept sites in one repo:

**Live:** https://ematkovichh.github.io/y2k-art-website/

## 1. Y2K Art Archive (root — `index.html`)

An experimental digital art gallery: a Windows-XP desktop intro, five scrolling
"rooms" (Crystal Dreams, Neon Memories, Digital Angels, Lost Y2K Archive,
Soft Fantasy), a liminal corridor, a cyber-shrine and a guestbook.
Self-contained page — all CSS/JS lives in `index.html`, photos in `img/`.
Design notes and photo-swap instructions: [`notes.txt`](notes.txt).

## 2. ÉTHÉRÉE — model agency concept (`agency/`)

A premium, photography-first concept with a dreamy, romantic softness —
clean, modern, and easy to navigate.

Pages: `agency/index.html` (Home) · `models.html` · `editorial.html` ·
`apply.html` · `about.html` · `contact.html`

### The look
- Palette: soft pinks, blush, cream, warm neutrals (CSS variables at the top of `agency/styles.css`)
- Type: *Cormorant Garamond* (editorial serif) + *Jost* (clean sans)
- Subtle only: gentle scroll-reveals, soft hover zooms, a fixed blend-mode nav

### Dropping in your own photos
Every image is a styled placeholder block: `<div class="ph" data-label="...">`.
To use a real photo, replace the block with an `<img>` inside a `ph` wrapper:

```html
<!-- before -->
<div class="ph grain" data-label="Portrait 900×1200"></div>

<!-- after -->
<div class="ph grain"><img src="images/anais.jpg" alt="Anaïs L."></div>
```

Keep the `data-label` dimensions as a crop guide. Suggested sizes:
- Hero: ~1600×2000 (portrait)
- Model portraits: 900×1200 (3:4)
- Editorial features: 1600×1000 · grid stories: 1000×1250

### Rename the agency
Search-and-replace `ÉTHÉRÉE` across `agency/*.html` (and the email domain
`etheree.com`) to use your own brand.

## Running locally

No build step. Open `index.html` in a browser, or serve the folder:

```
python3 -m http.server 8000
```

Both sites are static; the only network dependency is Google Fonts.
