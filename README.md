# y2k archive Website Concept

A premium, photography-first concept inspired by the dreamy, romantic softness of the *Agora Hills* era — clean, modern, and easy to navigate.

https://ematkovichh.github.io/y2k-art-website/

## Pages
`index.html` (Home) · `models.html` · `editorial.html` · `apply.html` · `about.html` · `contact.html`

Open `index.html` in any browser to start.

## The look
- Palette: soft pinks, blush, cream, warm neutrals (defined as CSS variables at the top of `styles.css`)
- Type: *Cormorant Garamond* (editorial serif) + *Jost* (clean sans)
- Subtle only: gentle scroll-reveals, soft hover zooms, a fixed blend-mode nav. No particles or heavy effects.

## Dropping in your own photos
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

## Rename the agency
Search-and-replace `ÉTHÉRÉE` across the `.html` files (and the email domain `etheree.com`) to use your own brand.
