"""Génère les variantes du logo info·faillite (SVG vectorisés + PNG + favicon)."""
import subprocess, sys, shutil
from pathlib import Path
import uharfbuzz as hb
from PIL import Image

FONT = Path(sys.argv[1])
OUT = Path(sys.argv[2])
TMP = Path(sys.argv[3])
CHROME = r"C:/Program Files/Google/Chrome/Application/chrome.exe"

YALE, ORANGE, BONDI, GREEN, GRAPHITE = "#2e4057", "#f18f01", "#048ba8", "#99c24d", "#2f2d2e"
WHITE, BLACK = "#ffffff", "#000000"

blob = hb.Blob.from_file_path(str(FONT))
face = hb.Face(blob)
UPEM = face.upem


def hb_font(wght):
    f = hb.Font(face)
    f.set_variations({"wght": wght})
    return f


class Pen:
    def __init__(self, dx, dy, s):
        self.d, self.dx, self.dy, self.s = [], dx, dy, s
    def _p(self, x, y):
        return f"{self.dx + x * self.s:.2f} {self.dy - y * self.s:.2f}"
    def moveTo(self, p): self.d.append("M" + self._p(*p))
    def lineTo(self, p): self.d.append("L" + self._p(*p))
    def curveTo(self, a, b, c): self.d.append("C" + " ".join(self._p(*q) for q in (a, b, c)))
    def qCurveTo(self, *pts):
        # TrueType : points implicites entre contrôles consécutifs
        pts = list(pts)
        while len(pts) > 2:
            a, b = pts[0], pts[1]
            mid = ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)
            self.d.append("Q" + self._p(*a) + " " + self._p(*mid))
            pts = pts[1:]
        self.d.append("Q" + self._p(*pts[0]) + " " + self._p(*pts[1]))
    def closePath(self): self.d.append("Z")
    endPath = closePath


def shape(text, wght, size, tracking_em=0.0, extra_track=0.0):
    """Retourne [(index caractère, path d)], (xmin, ymin, xmax, ymax) en px, origine ligne de base 0."""
    f = hb_font(wght)
    buf = hb.Buffer()
    buf.add_str(text)
    buf.guess_segment_properties()
    hb.shape(f, buf, {"kern": True, "liga": True})
    s = size / UPEM
    x = 0.0
    glyphs, box = [], [1e9, 1e9, -1e9, -1e9]
    for info, pos in zip(buf.glyph_infos, buf.glyph_positions):
        pen = Pen(x + pos.x_offset * s, -pos.y_offset * s, s)
        f.draw_glyph_with_pen(info.codepoint, pen)
        ext = f.get_glyph_extents(info.codepoint)
        if ext and ext.width:
            x0 = x + ext.x_bearing * s
            x1 = x0 + ext.width * s
            y0 = -ext.y_bearing * s          # haut (y SVG)
            y1 = y0 - ext.height * s         # bas
            box = [min(box[0], x0), min(box[1], y0), max(box[2], x1), max(box[3], y1)]
        glyphs.append((info.cluster, " ".join(pen.d)))
        x += pos.x_advance * s + tracking_em * size + extra_track
    return glyphs, box


def paths(glyphs, color_of, dx=0, dy=0):
    out = []
    for cl, d in glyphs:
        if d:
            out.append(f'<path transform="translate({dx:.2f} {dy:.2f})" fill="{color_of(cl)}" d="{d}"/>')
    return "\n  ".join(out)


def svg(w, h, body, bg=None, rx=0, title="info·faillite"):
    rect = f'<rect width="{w:.2f}" height="{h:.2f}" rx="{rx:.2f}" fill="{bg}"/>\n  ' if bg else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:.2f} {h:.2f}" '
            f'width="{w:.0f}" height="{h:.0f}" role="img" aria-label="{title}">\n  '
            f'<title>{title}</title>\n  {rect}{body}\n</svg>\n')


WORD = "info·faillite"
DOT = WORD.index("·")
TAG = "GUIDE DE LA FAILLITE EN BELGIQUE"

# --- Logotype ---------------------------------------------------------------
SIZE = 100
wg, wb = shape(WORD, 800, SIZE, -0.03)
PAD = 14


def logotype(text_c, dot_c, bg=None):
    w = wb[2] - wb[0] + 2 * PAD
    h = wb[3] - wb[1] + 2 * PAD
    body = paths(wg, lambda c: dot_c if c == DOT else text_c, PAD - wb[0], PAD - wb[1])
    return svg(w, h, body, bg)


# --- Signature : logotype + ligne de base -------------------------------------
TSIZE = 15.5
tg0, tb0 = shape(TAG, 600, TSIZE)
target = wb[2] - wb[0]
extra = (target - (tb0[2] - tb0[0])) / (len(TAG) - 1)
tg, tb = shape(TAG, 600, TSIZE, 0, extra)
GAP = 16


def signature(text_c, dot_c, tag_c, bg=None):
    w = target + 2 * PAD
    top = PAD - wb[1]
    tag_y = top + wb[3] + GAP - tb[1]
    h = tag_y + tb[3] + PAD
    body = paths(wg, lambda c: dot_c if c == DOT else text_c, PAD - wb[0], top)
    body += "\n  " + paths(tg, lambda c: tag_c, PAD - wb[0] + (wb[0] - tb[0]), tag_y)
    return svg(w, h, body, bg)


# --- Monogramme "i·f" -------------------------------------------------------
MONO = "i·f"
mg, mb = shape(MONO, 800, 390, -0.02)


def monogramme(bg, text_c, dot_c, shape_="carre"):
    S = 512
    rx = {"carre": 112, "rond": 256, "plein": 0}[shape_]
    mw, mh = mb[2] - mb[0], mb[3] - mb[1]
    dx = (S - mw) / 2 - mb[0]
    dy = (S - mh) / 2 - mb[1]
    body = paths(mg, lambda c: dot_c if c == 1 else text_c, dx, dy)
    return svg(S, S, body, bg, rx)


# --- Écriture ---------------------------------------------------------------
# Seuls les sous-dossiers générés sont recréés (README.md et ce script restent).
for d in ("svg", "png", "favicon", "reseaux"):
    if (OUT / d).exists():
        shutil.rmtree(OUT / d)
    (OUT / d).mkdir(parents=True)

files = {
    "logotype-couleur": logotype(YALE, ORANGE),
    "logotype-inverse": logotype(WHITE, ORANGE),
    "logotype-yale": logotype(YALE, YALE),
    "logotype-noir": logotype(BLACK, BLACK),
    "logotype-blanc": logotype(WHITE, WHITE),
    "signature-couleur": signature(YALE, ORANGE, GRAPHITE),
    "signature-inverse": signature(WHITE, ORANGE, "#c9d2de"),
    "signature-noir": signature(BLACK, BLACK, BLACK),
    "signature-blanc": signature(WHITE, WHITE, WHITE),
    "monogramme-yale": monogramme(YALE, WHITE, ORANGE),
    "monogramme-orange": monogramme(ORANGE, WHITE, YALE),
    "monogramme-blanc": monogramme(WHITE, YALE, ORANGE),
    "monogramme-yale-rond": monogramme(YALE, WHITE, ORANGE, "rond"),
    "monogramme-transparent": monogramme(None, YALE, ORANGE),
}
for name, content in files.items():
    (OUT / "svg" / f"{name}.svg").write_text(content, encoding="utf-8")
(OUT / "favicon" / "favicon.svg").write_text(files["monogramme-yale"], encoding="utf-8")

# Image de partage (Open Graph) 1200 x 630 : signature inversée sur Yale
sig_w = target + 2 * PAD
sig_h = None
import re
m = re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', files["signature-inverse"])
sw, sh = float(m.group(1)), float(m.group(2))
scale = 760 / sw
inner = files["signature-inverse"].split("</title>", 1)[1].rsplit("</svg>", 1)[0]
og = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 630" width="1200" height="630">'
      f'<rect width="1200" height="630" fill="{YALE}"/>'
      f'<rect x="0" y="606" width="1200" height="24" fill="{ORANGE}"/>'
      f'<g transform="translate({(1200 - sw * scale) / 2:.2f} {(606 - sh * scale) / 2:.2f}) scale({scale:.4f})">{inner}</g></svg>')
(OUT / "reseaux" / "og-image.svg").write_text(og, encoding="utf-8")


# --- Rendu PNG via Chrome headless ----------------------------------------
TMP.mkdir(parents=True, exist_ok=True)


def render(svg_path, w, h):
    html = TMP / "r.html"
    html.write_text(
        f'<!doctype html><html><head><style>html,body{{margin:0;background:transparent}}'
        f'img{{display:block;width:{w}px;height:{h}px}}</style></head>'
        f'<body><img src="{svg_path.resolve().as_uri()}"></body></html>', encoding="utf-8")
    png = TMP / "r.png"
    if png.exists():
        png.unlink()
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--no-first-run",
                    f"--user-data-dir={TMP / 'prof'}", "--hide-scrollbars",
                    "--force-device-scale-factor=1", "--default-background-color=00000000",
                    f"--window-size={w},{h}", f"--screenshot={png}", html.resolve().as_uri()],
                   check=True, timeout=60, capture_output=True)
    return Image.open(png).convert("RGBA").crop((0, 0, w, h))


def png_sizes(name, widths):
    p = OUT / "svg" / f"{name}.svg"
    m = re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', p.read_text(encoding="utf-8"))
    vw, vh = float(m.group(1)), float(m.group(2))
    big_w = max(2400, max(widths))
    big = render(p, big_w, round(big_w * vh / vw))
    for w in widths:
        h = round(w * vh / vw)
        big.resize((w, h), Image.LANCZOS).save(OUT / "png" / f"{name}-{w}.png", optimize=True)
    return big


for name in files:
    widths = [512, 1024] if name.startswith("monogramme") else [400, 800, 1600]
    png_sizes(name, widths)

# Favicons
icon = render(OUT / "svg" / "monogramme-yale.svg", 1024, 1024)
for s in (16, 32, 48, 180, 192, 512):
    target_name = {180: "apple-touch-icon.png"}.get(s, f"icon-{s}.png")
    img = icon.resize((s, s), Image.LANCZOS)
    if s == 180:
        # iOS ignore la transparence : carré plein Yale
        full = render(OUT / "svg" / "monogramme-yale.svg", 1024, 1024)
        bgimg = Image.new("RGBA", (1024, 1024), YALE)
        bgimg.alpha_composite(full)
        img = bgimg.resize((180, 180), Image.LANCZOS).convert("RGB")
    img.save(OUT / "favicon" / target_name, optimize=True)
icon.save(OUT / "favicon" / "favicon.ico", sizes=[(16, 16), (32, 32), (48, 48)])

render(OUT / "reseaux" / "og-image.svg", 1200, 630).convert("RGB").save(OUT / "reseaux" / "og-image-1200x630.png", optimize=True)
render(OUT / "svg" / "monogramme-yale-rond.svg", 1024, 1024).resize((400, 400), Image.LANCZOS).save(OUT / "reseaux" / "avatar-400.png", optimize=True)
print("ok")
