#!/usr/bin/env python3
"""Image prep for a Trajectory Labs app page. Needs Pillow with WebP support.

    python3 tools/prep_images.py --site . --icon path/to/icon-1024.png \
        --shots path/to/appstore-frames/ --hero m-1-home.png \
        --fonts path/to/fonts/ --name HamPrep --label "TRAJECTORY LABS  ·  IPHONE" \
        --headline "Pass your ham radio exam." --headline2 "Understand it too." \
        --lead "Technician and General prep, every one of|832 questions explained. One-time purchase,|no subscription." \
        --og-shot m-2-explanation.png --badge path/to/apple-badge-black.svg

What it does
  1. Crops the phone out of each 1320x2868 App Store marketing frame (near-black bezel detected),
     takes the alpha from a flood fill of the frame background (needs a closed dark bezel ring), exports WebP: shot-<name>.webp at 520px
     and hero-phone.webp at 760px. Output names come from the frame file names: "m-1-home.png" -> "shot-home.webp".
  2. Builds the icon family: icon.png (512, square, hotlinked by the parent site), apple-touch-icon.png (180),
     favicon.png (64, rounded), favicon-192.png (192, rounded), assets/app-icon.webp (256, rounded).
  3. Renders assets/og-card.jpg (1200x630). Fonts: Manrope-800.ttf, Manrope-500.ttf, JetBrainsMono.ttf in --fonts
     (static TTFs from Google Fonts). Falls back to DejaVu if missing, which looks off-brand, so get the fonts.
  4. Copies the Apple badge unchanged to assets/app-store-badge-black.svg when --badge is given.

The tools/ folder is plain Python with no secrets, so it is fine to deploy with the site, or exclude it; nothing links to it.
"""
import argparse, os, re, shutil, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter

INSET = 1          # px trimmed inside the detected bezel box, kills the anti-aliased frame fringe
ACCENT = (242, 115, 26)  # used only for the OG glow; override with --accent "r,g,b"


def is_dark(px):
    return max(px[:3]) < 60


def phone_box(im):
    """Bounding box of the near-black device bezel inside a colored marketing frame."""
    w, h = im.size
    px = im.load()
    xs, ys = [], []
    step = 4
    for y in range(0, h, step):
        for x in range(0, w, step):
            if is_dark(px[x, y]):
                xs.append(x); ys.append(y)
    if not xs:
        raise SystemExit("no dark bezel found; is this a marketing frame with a black device?")
    x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)

    def first(rng, test):
        for v in rng:
            if test(v):
                return v
        return rng[0]

    x0 = first(range(max(0, x0 - step), x0 + step + 1), lambda x: any(is_dark(px[x, y]) for y in range(y0, y1, 3)))
    x1 = first(range(min(w - 1, x1 + step), x1 - step - 1, -1), lambda x: any(is_dark(px[x, y]) for y in range(y0, y1, 3)))
    y0 = first(range(max(0, y0 - step), y0 + step + 1), lambda y: any(is_dark(px[x, y]) for x in range(x0, x1, 3)))
    y1 = first(range(min(h - 1, y1 + step), y1 - step - 1, -1), lambda y: any(is_dark(px[x, y]) for x in range(x0, x1, 3)))
    return x0, y0, x1 + 1, y1 + 1


def corner_radius(im, box):
    """Informational only (logged): rows from the top until the dark bezel reaches the left edge."""
    x0, y0, x1, y1 = box
    px = im.load()
    for y in range(y0, y0 + (y1 - y0) // 4):
        if is_dark(px[x0 + 1, y]):
            return max(8, y - y0)
    return 80


def crop_phone(src, out_path, width):
    im = Image.open(src).convert("RGB")
    box = phone_box(im)
    r = corner_radius(im, box)
    x0, y0, x1, y1 = box
    box_in = (x0 + INSET, y0 + INSET, x1 - INSET, y1 - INSET)
    phone = im.crop(box_in).convert("RGBA")
    # The bezel corner is a squircle, so a drawn rounded rectangle never matches it. Instead take the
    # alpha from the frame itself: flood-fill the non-bezel background from each corner, everything the
    # fill reaches is outside the phone. Then erode one pixel so no anti-aliased frame color survives.
    px = phone.convert("RGB").load()
    wall = Image.new("L", phone.size, 0)
    wp = wall.load()
    for y in range(phone.size[1]):
        for x in range(phone.size[0]):
            if is_dark(px[x, y]):
                wp[x, y] = 255
    w2, h2 = phone.size
    for seed in ((0, 0), (w2 - 1, 0), (0, h2 - 1), (w2 - 1, h2 - 1)):
        if wp[seed] == 0:
            ImageDraw.floodfill(wall, seed, 128)
    mask = wall.point(lambda v: 0 if v == 128 else 255)
    mask = mask.filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(0.5))
    phone.putalpha(mask)
    ratio = width / phone.size[0]
    out = phone.resize((width, round(phone.size[1] * ratio)), Image.LANCZOS)
    out.save(out_path, "WEBP", quality=82, method=6)
    print(f"{os.path.basename(out_path)}: box={box} r={r} -> {out.size} {os.path.getsize(out_path)//1024} KB")
    return out.size


def rounded(im, size, path, fmt="PNG", radius_ratio=0.2237):
    im2 = im.resize((size, size), Image.LANCZOS).convert("RGBA")
    mask = Image.new("L", (size, size), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, size - 1, size - 1], radius=round(size * radius_ratio), fill=255)
    im2.putalpha(mask)
    im2.save(path, fmt, **({"quality": 90, "method": 6} if fmt == "WEBP" else {"optimize": True}))
    print(f"{os.path.basename(path)}: {size}px {os.path.getsize(path)//1024} KB")


def font(fonts_dir, name, size):
    p = os.path.join(fonts_dir or "", name)
    if fonts_dir and os.path.exists(p):
        return ImageFont.truetype(p, size)
    for fb in ("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"):
        if os.path.exists(fb):
            print(f"warning: {name} not found in --fonts, using DejaVu", file=sys.stderr)
            return ImageFont.truetype(fb, size)
    return ImageFont.load_default()


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--site", required=True, help="site folder (index.html lives here)")
    ap.add_argument("--icon", required=True, help="1024px App Store icon PNG")
    ap.add_argument("--shots", required=True, help="folder of App Store marketing frames (PNG)")
    ap.add_argument("--hero", required=True, help="file name inside --shots to use for hero-phone.webp")
    ap.add_argument("--og-shot", help="file name inside --shots to show on the OG card (defaults to --hero)")
    ap.add_argument("--badge", help="Apple badge SVG to copy unchanged")
    ap.add_argument("--fonts", help="folder with Manrope-800.ttf, Manrope-500.ttf, JetBrainsMono.ttf")
    ap.add_argument("--name", required=True)
    ap.add_argument("--label", default="TRAJECTORY LABS  ·  IPHONE")
    ap.add_argument("--headline", required=True, help="first headline line (ink)")
    ap.add_argument("--headline2", default="", help="second headline line (accent color)")
    ap.add_argument("--lead", default="", help="lead text, lines separated by |")
    ap.add_argument("--accent", default="242,115,26", help="r,g,b of the app accent for the OG glow")
    ap.add_argument("--accent-ink", default="#b04e00", help="hex accent text color for the OG headline2")
    a = ap.parse_args()

    assets = os.path.join(a.site, "assets")
    os.makedirs(assets, exist_ok=True)
    accent = tuple(int(v) for v in a.accent.split(","))

    # 1. phones
    frames = sorted(f for f in os.listdir(a.shots) if f.lower().endswith(".png"))
    for f in frames:
        slug = re.sub(r"^m-\d+-", "", os.path.splitext(f)[0])
        crop_phone(os.path.join(a.shots, f), os.path.join(assets, f"shot-{slug}.webp"), 520)
    crop_phone(os.path.join(a.shots, a.hero), os.path.join(assets, "hero-phone.webp"), 760)

    # 2. icons
    icon = Image.open(a.icon).convert("RGB")
    icon.resize((512, 512), Image.LANCZOS).save(os.path.join(a.site, "icon.png"), "PNG", optimize=True)
    icon.resize((180, 180), Image.LANCZOS).save(os.path.join(a.site, "apple-touch-icon.png"), "PNG", optimize=True)
    rounded(icon, 64, os.path.join(a.site, "favicon.png"))
    rounded(icon, 192, os.path.join(a.site, "favicon-192.png"))
    rounded(icon, 256, os.path.join(assets, "app-icon.webp"), fmt="WEBP")

    # 3. OG card
    W, H = 1200, 630
    og = Image.new("RGB", (W, H), "#f5f9f7")
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(glow).ellipse([720, -220, 1420, 480], fill=accent + (70,))
    glow = glow.filter(ImageFilter.GaussianBlur(90))
    og.paste(glow, (0, 0), glow)
    d = ImageDraw.Draw(og)
    ic = icon.resize((150, 150), Image.LANCZOS).convert("RGBA")
    m = Image.new("L", ic.size, 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, 149, 149], radius=34, fill=255); ic.putalpha(m)
    og.paste(ic, (84, 84), ic)
    f_label = font(a.fonts, "JetBrainsMono.ttf", 21)
    f_h = font(a.fonts, "Manrope-800.ttf", 57)
    f_name = font(a.fonts, "Manrope-800.ttf", 70)
    f_p = font(a.fonts, "Manrope-500.ttf", 27)
    d.text((262, 104), a.label, font=f_label, fill="#006f66")
    d.text((258, 136), a.name, font=f_name, fill="#0f1c1a")
    d.text((84, 306), a.headline, font=f_h, fill="#0f1c1a")
    if a.headline2:
        d.text((84, 372), a.headline2, font=f_h, fill=a.accent_ink)
    for i, line in enumerate([l for l in a.lead.split("|") if l]):
        d.text((84, 478 + 36 * i), line, font=f_p, fill="#4d5f5b")
    og_src = os.path.join(a.shots, a.og_shot or a.hero)
    slug = re.sub(r"^m-\d+-", "", os.path.splitext(os.path.basename(og_src))[0])
    ph = Image.open(os.path.join(assets, f"shot-{slug}.webp")).convert("RGBA")
    ph = ph.resize((270, round(ph.size[1] * 270 / ph.size[0])), Image.LANCZOS)
    og.paste(ph, (W - 300, 110), ph)
    og.save(os.path.join(assets, "og-card.jpg"), "JPEG", quality=84, optimize=True, progressive=True)
    print("og-card.jpg:", os.path.getsize(os.path.join(assets, "og-card.jpg")) // 1024, "KB")

    # 4. badge
    if a.badge:
        shutil.copy(a.badge, os.path.join(assets, "app-store-badge-black.svg"))
        print("badge copied unchanged")


if __name__ == "__main__":
    main()
