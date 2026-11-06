# Trajectory Labs app page template

A plain static site (no build step) for one app, deployable to GitHub Pages as-is.
HamPrep is the first instance. Copy the whole folder for the next app and work through this file.

## Files

| File | What it is | Change per app? |
|---|---|---|
| `index.html` | Landing page. Every editable block is marked with an HTML comment starting `SLOT:` or `============`. | Yes |
| `privacy.html` | Privacy policy in the same chrome. | Yes (the legal text) |
| `support.html` | Support page with FAQ cards. | Yes |
| `assets/app-page.css` | Shared stylesheet: Trajectory Labs tokens, chrome, components, light and dark mode. | Only the `--accent*` block |
| `assets/app-icon.webp` | 256px rounded icon used in the nav crumb and hero. | Yes |
| `assets/hero-phone.webp` | 760px wide phone crop for the hero. | Yes |
| `assets/shot-*.webp` | 520px wide phone crops for the gallery. | Yes |
| `assets/og-card.jpg` | 1200x630 Open Graph and Twitter card image. | Yes |
| `assets/app-store-badge-black.svg` | Apple's official badge. Never edit, recolor or crop it. | No |
| `icon.png` | 512px square icon at the site root. The trajectorylabs.io homepage hotlinks `https://<app>.trajectorylabs.io/icon.png`, so keep this path. | Yes |
| `favicon.png`, `favicon-192.png`, `apple-touch-icon.png` | Favicon family generated from the icon. | Yes |
| `tools/prep_images.py` | Image prep script (phone crops, icon family, OG card, badge copy). Plain Python, no secrets: fine to deploy with the site or exclude it, nothing links to it. | No |
| `CNAME` | The custom domain, one line, no trailing newline needed. | Yes |
| `.nojekyll` | Empty. Tells GitHub Pages to serve files as-is. | No |

## Variables and slots to change

1. **Store state** (top of `index.html`): `<html data-store="soon">` or `data-store="live"`.
   `soon` shows the "Coming soon" pill and hides every Apple badge, store link and the Apple trademark line.
   `live` shows Apple's badge linking to the App Store, the Apple trademark line in the footer, and hides the coming-soon copy.
   Both variants are already in the markup (classes `store-soon` and `store-live`), so flipping the attribute is the whole switch.
   Also set the attribute on `privacy.html` and `support.html` for consistency (they carry no store CTA, so it is harmless either way).
2. **App Store link**: search `apps.apple.com/app/id` in `index.html` (two places) and replace the id.
3. **Smart banner**: the commented `apple-itunes-app` meta in the head of `index.html`. Uncomment it once the app is live.
4. **Accent colors** in `assets/app-page.css`, section 2 ("per-app accent") and the two dark-mode blocks:
   - `--accent`: the brand fill. Dark ink (`--on-accent`) sits on it, so it can be a bright color.
   - `--accent-ink`: text version for light mode. Must reach 4.5:1 against `--bg` (#f5f9f7). For orange that meant darkening #f2731a to #b04e00.
   - `--accent-ink` in dark mode: a lighter tint that reaches 4.5:1 against #0b1513 (#ff9a52 for orange).
   - `--accent-soft`: tinted background for chips and the coming-soon pill, light and dark values.
   - `--accent-glow`: translucent accent for the hero blob.
   - `--accent-shadow`: translucent accent for the icon's drop shadow in the hero.
   Those are the only app-specific colors in the shared stylesheet; grep it for the old app's hex values before you ship.
5. **Head meta** (`SLOT: page meta` in each page): title, description, canonical, OG and Twitter tags, og:image dimensions and alt.
6. **Nav crumb** (`SLOT: app crumb`): the app name beside the Trajectory Labs wordmark.
7. **Hero**: label (category, platform), app name and tagline, headline (keep the accent span for the second sentence), lead, CTA notes.
8. **Stats strip**: four numbers. Only claim what you can back up; no ratings, user counts or pass rates.
9. **Screenshots**: five `figure.shot` blocks. Each needs a real alt text describing the screen, and a bold caption plus one line.
10. **Features**: six cards. Keep the `idx` numbers.
11. **Pricing**: the free list and the plan cards. The `plan.best` card gets the "Best value" chip.
12. **Privacy strip**: three cards summarising the App Privacy label. Link to `privacy.html`.
13. **Second CTA** and the **contact band**: copy only; the email stays `support@trajectorylabs.io` unless the app has its own.
14. **Footer legal line**: the data-source and non-affiliation line, plus Apple's trademark line (required when the badge is shown).

Shared chrome (nav, logo SVG, footer layout, contact band, buttons, cards) stays the same across apps so the family reads as one.

## Image prep

`tools/prep_images.py` does all of this with Pillow. Run it from the site folder, for example:

```
python3 tools/prep_images.py --site . --icon ../brief/app-icon-1024.png \
  --shots ../brief/appstore-screenshots --hero m-1-home.png --og-shot m-2-explanation.png \
  --badge ../brief/apple-badge-black.svg --fonts ../fonts \
  --name HamPrep --headline "Pass your ham radio exam." --headline2 "Understand it too." \
  --lead "Technician and General prep, every one of|832 questions explained. One-time purchase,|no subscription."
```

`--fonts` points at a folder with `Manrope-800.ttf`, `Manrope-500.ttf` and `JetBrainsMono.ttf` (static TTFs from Google Fonts). `--accent r,g,b` and `--accent-ink #hex` set the OG card colors for a different app. `python3 tools/prep_images.py --help` lists everything. Steps it performs:

1. **Phone crops**: from the 1320x2868 App Store marketing frames, detect the near-black device bezel and crop to it. The alpha channel is taken from the frame itself (the background is flood-filled from the corners and eroded one pixel), because the bezel corner is a squircle that no drawn rounded rectangle matches. Export WebP (quality 82): 520px wide for the gallery, 760px wide for the hero. Zoom a corner to 4x and confirm no frame color survives.
2. **Icon family** from the 1024px App Store icon: `icon.png` 512px square (no rounding, it is hotlinked by the parent site), `apple-touch-icon.png` 180px square, `favicon.png` 64px and `favicon-192.png` 192px with iOS-style rounded corners, `assets/app-icon.webp` 256px rounded.
3. **OG card** 1200x630 JPEG: page background, soft accent glow, icon, label, app name, headline in Manrope 800 and a phone peeking in on the right. Keep the headline inside the left 60% so it never collides with the phone.
4. Copy `apple-badge-black.svg` unchanged.

Budget: aim for under 600 KB for `index.html` plus everything it loads. HamPrep lands around 330 KB: about 260 KB of local files plus roughly 50 KB of web fonts.

## Apple badge rules (live state)

- Use the official artwork as provided, never recolored, stretched, cropped or re-drawn.
- Minimum height 40px (the template uses 56px).
- Clear space around it of at least one quarter of its height (the `.store-badge` padding handles this).
- Keep Apple's trademark attribution in the footer legal line (it is wrapped in `.store-live`, so it appears with the badge).
- Never show the badge before the app is downloadable, which is what the `soon` state is for.

## Checklist before publishing

- [ ] `data-store` set correctly on all three pages; smart banner meta uncommented only if live.
- [ ] App Store id correct in both links.
- [ ] Every fact on the page matches the app's current facts file and App Store listing (pools, prices, bundle, feature names).
- [ ] No em dashes anywhere in user-facing copy (search for the character).
- [ ] No invented testimonials, ratings, user counts or pass-rate claims, and no promises about unreleased platforms or versions.
- [ ] Privacy and support pages keep their legal wording; only layout changed.
- [ ] `icon.png` present at the root, 512px or larger.
- [ ] `CNAME` holds the right domain, `.nojekyll` exists.
- [ ] Canonical URLs, OG URLs and og:image are absolute `https://` URLs on the app's domain.
- [ ] Accent text colors pass 4.5:1 in both modes (check `--accent-ink` against `--bg`).
- [ ] Render at 360px, 390px, 768px, 1024px and 1280px in light and dark; confirm no horizontal scroll, images load, pricing cards line up, the screenshot scroller starts with the gutter visible, alt texts read well.
- [ ] Click every link once: parent site, More apps, privacy, support, mailto, store link (live only).
