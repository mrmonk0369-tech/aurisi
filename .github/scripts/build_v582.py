#!/usr/bin/env python3
# AURISI v58.2: new gold-A logo (aurisi-logo-source.png) everywhere.
# - Replaces the embedded AURISI_LOGO_DATA_URL (448x448 PNG) used by splash,
#   login, brand, drawer, favicon and dynamic manifest.
# - Regenerates repo icons: icon-192.png, icon-512.png,
#   icon-maskable-512.png (80% safe zone), apple-touch-icon.png.
# Base: AURISI.html v58.1. Idempotent: no-op if already v58.2.
import sys, io, re, base64

from PIL import Image

LOGO_URL = "https://github.com/mrmonk0369-tech/aurisi/releases/download/v57.0.0/aurisi-logo-source.png"
LOGO_SHA256 = "46137905bc21c3728d75d98daafd23d60e666b037de8a9db273782b3d31b72e1"
LOGO_SIZE = 1702227

BASE = sys.argv[1] if len(sys.argv) > 1 else "AURISI.html"
OUT = sys.argv[2] if len(sys.argv) > 2 else "AURISI_new.html"
LOGO = sys.argv[3] if len(sys.argv) > 3 else "logo.png"
ICONDIR = sys.argv[4] if len(sys.argv) > 4 else "."

h = io.open(BASE, encoding="utf-8").read()

if 'APP_VERSION="58.2"' in h:
    io.open(OUT, "w", encoding="utf-8").write(h)
    print("already v58.2 - no-op")
    sys.exit(0)

assert 'APP_VERSION="58.1"' in h, "base must be v58.1"

# --- verify logo source integrity ---
import hashlib
raw = open(LOGO, "rb").read()
assert len(raw) == LOGO_SIZE, "logo size mismatch: %d" % len(raw)
assert hashlib.sha256(raw).hexdigest() == LOGO_SHA256, "logo sha256 mismatch"

img = Image.open(LOGO).convert("RGB")

# --- 448x448 main embedded logo ---
im448 = img.resize((448, 448), Image.LANCZOS)
buf = io.BytesIO()
im448.save(buf, "PNG", optimize=True)
b64 = base64.b64encode(buf.getvalue()).decode("ascii")
new_const = 'const AURISI_LOGO_DATA_URL="data:image/png;base64,' + b64 + '"'

BS = chr(92)
pat = re.compile("const AURISI_LOGO_DATA_URL=" + BS + '"data:image/png' + BS + ";base64,[A-Za-z0-9+/=]+" + BS + '"')
found = pat.findall(h)
assert len(found) == 1, "expected exactly 1 logo constant, found %d" % len(found)
m = pat.search(h)
h = h[:m.start()] + new_const + h[m.end():]

# --- version bump ---
old_v = 'var APP_VERSION="58.1"'
new_v = 'var APP_VERSION="58.2"'
assert h.count(old_v) == 1
h = h.replace(old_v, new_v)

io.open(OUT, "w", encoding="utf-8").write(h)

# --- repo icons ---
def save_icon(size, path, maskable=False):
    im = img.resize((size, size), Image.LANCZOS)
    if maskable:
        # 80% logo centered on cream background for the maskable safe zone
        bg = im.resize((1, 1), Image.LANCZOS).getpixel((0, 0))
        canvas = Image.new("RGB", (size, size), bg)
        inner = size * 80 // 100
        im2 = img.resize((inner, inner), Image.LANCZOS)
        off = (size - inner) // 2
        canvas.paste(im2, (off, off))
        im = canvas
    im.save(path, "PNG", optimize=True)

save_icon(192, ICONDIR + "/icon-192.png")
save_icon(512, ICONDIR + "/icon-512.png")
save_icon(512, ICONDIR + "/icon-maskable-512.png", maskable=True)
save_icon(180, ICONDIR + "/apple-touch-icon.png")

print("applied logo patches, size: %d bytes" % len(h.encode("utf-8")))
