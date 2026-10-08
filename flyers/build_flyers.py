"""
Flyers Remis à Neuf — A5 recto/verso, prêts pour l'imprimeur.

Produit quatre fichiers dans flyers/ :
  flyer-A5-impression.pdf  148x210 mm + 3 mm de fonds perdus + traits de coupe
  flyer-A5-apercu.pdf      148x210 mm net, sans repères (pour envoyer ou relire)
  apercu-recto.png         rendu 150 dpi
  apercu-verso.png

Pour mettre à jour les coordonnées : modifier le dictionnaire CONTACT ci-dessous
puis relancer  python flyers/build_flyers.py
"""

from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor, white
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os

# --------------------------------------------------------------------------
# Contenu variable
# --------------------------------------------------------------------------
CONTACT = {
    "telephone": "[ TÉLÉPHONE À RENSEIGNER ]",
    "email": "[ EMAIL À RENSEIGNER ]",
    "site": "amazing-sable-e931e5.netlify.app",
}

HERE = os.path.dirname(os.path.abspath(__file__))
A = os.path.join(HERE, "assets")
F = os.path.join(HERE, "fonts")

# --------------------------------------------------------------------------
# Format
# --------------------------------------------------------------------------
TW, TH = 148.0, 210.0          # format fini A5
BLEED = 3.0                    # fonds perdus
MARGIN = 14.0                  # marge de composition
COL = TW - 2 * MARGIN          # 120 mm de colonne utile

INK = HexColor("#171918")
SAND = HexColor("#C9B08A")
SAND_DEEP = HexColor("#A88F69")
PAPER = HexColor("#FAF8F5")
MUTED = HexColor("#6E716D")
ON_DARK = HexColor("#A8ABA6")
LINE_DARK = HexColor("#343836")
LINE = HexColor("#E0DCD3")

for name, file in (
    ("Manrope", "Manrope-Regular.ttf"),
    ("Manrope-Md", "Manrope-Medium.ttf"),
    ("Manrope-Sb", "Manrope-SemiBold.ttf"),
    ("Manrope-Bd", "Manrope-Bold.ttf"),
):
    pdfmetrics.registerFont(TTFont(name, os.path.join(F, file)))


class Sheet:
    """Repère en millimètres depuis le coin haut-gauche du format fini."""

    def __init__(self, c, bleed):
        self.c = c
        self.b = bleed

    def X(self, x):
        return (self.b + x) * mm

    def Y(self, y):
        return (self.b + TH - y) * mm

    # -- primitives --------------------------------------------------------
    def rect(self, x, y, w, h, color):
        self.c.setFillColor(color)
        self.c.rect(self.X(x), self.Y(y + h), w * mm, h * mm, stroke=0, fill=1)

    def bleed_rect(self, y, h, color):
        """Bandeau pleine largeur, débordant dans les fonds perdus."""
        self.rect(-self.b, y, TW + 2 * self.b, h, color)

    def line(self, x, y, w, color, weight=0.5):
        self.c.setStrokeColor(color)
        self.c.setLineWidth(weight)
        self.c.line(self.X(x), self.Y(y), self.X(x + w), self.Y(y))

    def text(self, x, y, s, font="Manrope", size=9, color=INK,
             track=0, align="l"):
        advance = pdfmetrics.stringWidth(s, font, size) + track * len(s)
        X = self.X(x)
        if align == "r":
            X -= advance
        elif align == "c":
            X -= advance / 2
        t = self.c.beginText()
        t.setTextOrigin(X, self.Y(y))
        t.setFont(font, size)
        t.setFillColor(color)
        t.setCharSpace(track)
        t.textOut(s)
        self.c.drawText(t)

    def width(self, s, font, size, track=0):
        return (pdfmetrics.stringWidth(s, font, size) + track * len(s)) / mm

    def wrap(self, x, y, s, w, font="Manrope", size=8, color=MUTED,
             leading=4.4, track=0):
        words, line_words, yy = s.split(), [], y
        for word in words:
            trial = " ".join(line_words + [word])
            if self.width(trial, font, size, track) > w and line_words:
                self.text(x, yy, " ".join(line_words), font, size, color, track)
                line_words, yy = [word], yy + leading
            else:
                line_words.append(word)
        if line_words:
            self.text(x, yy, " ".join(line_words), font, size, color, track)
            yy += leading
        return yy

    def eyebrow(self, x, y, s, color=SAND_DEEP, rule=True, rule_color=None):
        if rule:
            self.line(x, y - 1.1, 7, rule_color or color, 0.6)
            x += 10.5
        self.text(x, y, s.upper(), "Manrope-Bd", 6, color, track=1.5)

    def image(self, path, x, y, w, h, mask=None):
        self.c.drawImage(path, self.X(x), self.Y(y + h), w * mm, h * mm,
                         mask=mask, preserveAspectRatio=False)

    def crop_marks(self):
        if not self.b:
            return
        self.c.setStrokeColor(INK)
        self.c.setLineWidth(0.25)
        g, L = 1.2, self.b - 1.2 + 2.5
        for cx, sx in ((0, -1), (TW, 1)):
            for cy, sy in ((0, -1), (TH, 1)):
                X0, Y0 = self.X(cx), self.Y(cy)
                self.c.line(X0 + sx * g * mm, Y0, X0 + sx * (g + L) * mm, Y0)
                self.c.line(X0, Y0 - sy * g * mm, X0, Y0 - sy * (g + L) * mm)


# --------------------------------------------------------------------------
# Recto
# --------------------------------------------------------------------------
def recto(s):
    s.bleed_rect(-s.b, TH + 2 * s.b, white)

    # En-tête : logo et localisation
    logo_h = 14.0
    from PIL import Image
    lw, lh = Image.open(os.path.join(A, "logo-print.png")).size
    s.image(os.path.join(A, "logo-print.png"),
            MARGIN, 16, logo_h * lw / lh, logo_h, mask="auto")
    s.text(MARGIN + logo_h * lw / lh + 4.5, 25.4, "Remis à Neuf",
           "Manrope-Sb", 12.5, INK, track=-0.35)
    s.text(TW - MARGIN, 25, "NICE · CÔTE D’AZUR", "Manrope-Bd", 6,
           HexColor("#9A9C98"), track=1.5, align="r")

    # Photographie pleine largeur
    s.image(os.path.join(A, "photo-recto.jpg"), -s.b, 44, TW + 2 * s.b, 94)

    # Accroche
    s.eyebrow(MARGIN, 153, "Rénovation d’appartements")

    s.text(MARGIN, 168, "Votre intérieur,", "Manrope-Md", 26, INK, track=-1.05)
    s.text(MARGIN, 180.5, "remis à neuf.", "Manrope-Md", 26, INK, track=-1.05)
    s.line(MARGIN, 182.6, s.width("remis à neuf.", "Manrope-Md", 26, -1.05),
           SAND, 1.1)

    s.wrap(MARGIN, 191.5,
           "Tous corps d’état, un interlocuteur unique "
           "et un budget lisible au mètre carré.",
           COL - 6, "Manrope", 9, MUTED, leading=4.8)

    # Bandeau d’action en pied de page
    s.bleed_rect(198, 12 + s.b, INK)
    s.text(MARGIN, 205.2, "Estimation sur simple demande",
           "Manrope-Sb", 8.5, white, track=-0.1)
    s.text(TW - MARGIN, 205.2, CONTACT["site"], "Manrope", 7.5, SAND,
           align="r")


# --------------------------------------------------------------------------
# Verso
# --------------------------------------------------------------------------
STEPS = [
    ("01 — Échanger", "Comprendre votre projet",
     "Le logement, les attentes, le périmètre."),
    ("02 — Chiffrer", "Cadrer le budget",
     "Une estimation au m², après étude du bien."),
    ("03 — Réaliser", "Conduire les travaux",
     "Un seul interlocuteur sur le chantier."),
    ("04 — Livrer", "Remettre les clés",
     "Finitions contrôlées, intérieur prêt à vivre."),
]

TRADES = ("Démolition · Électricité · Plomberie · Plâtrerie · Cloisons · "
          "Peinture · Revêtements de sol · Salle de bains · Cuisine · "
          "Menuiserie · Finitions")


def verso(s):
    s.bleed_rect(-s.b, TH + 2 * s.b, INK)
    s.image(os.path.join(A, "photo-verso.jpg"), -s.b, -s.b, TW + 2 * s.b, 42 + s.b)

    # Tarification
    s.eyebrow(MARGIN, 53, "Tarification", SAND, rule_color=SAND)
    s.text(MARGIN, 64, "Un prix au m².", "Manrope-Md", 16, white, track=-0.65)
    s.text(MARGIN, 72.5, "Une vision claire du budget.", "Manrope-Md", 16,
           white, track=-0.65)
    s.wrap(MARGIN, 81,
           "Surface, niveau de rénovation, prestations et matériaux : "
           "chaque estimation est établie sur mesure, après étude de "
           "votre appartement.",
           COL - 8, "Manrope", 7.6, ON_DARK, leading=4.1)

    s.line(MARGIN, 91, COL, LINE_DARK, 0.5)

    # Méthode
    s.eyebrow(MARGIN, 97, "La méthode", SAND, rule_color=SAND)
    for i, (label, title, desc) in enumerate(STEPS):
        x = MARGIN + (i % 2) * (COL / 2 + 3)
        y = 106 + (i // 2) * 21
        s.text(x, y, label.upper(), "Manrope-Bd", 6, SAND, track=1.2)
        s.text(x, y + 6, title, "Manrope-Md", 9.3, white, track=-0.3)
        s.wrap(x, y + 11, desc, COL / 2 - 4, "Manrope", 6.7, ON_DARK,
               leading=3.5)

    s.line(MARGIN, 144, COL, LINE_DARK, 0.5)

    # Corps d’état
    s.eyebrow(MARGIN, 150, "Tous corps d’état", SAND, rule_color=SAND)
    s.wrap(MARGIN, 157, TRADES, COL, "Manrope", 7.2, ON_DARK, leading=4.4)

    # Pied de page clair : coordonnées et QR
    s.bleed_rect(167, TH - 167 + s.b, PAPER)

    from PIL import Image
    lw, lh = Image.open(os.path.join(A, "logo-print.png")).size
    logo_h = 12.0
    s.image(os.path.join(A, "logo-print.png"),
            MARGIN, 174, logo_h * lw / lh, logo_h, mask="auto")
    s.text(MARGIN + logo_h * lw / lh + 4, 182.6, "Remis à Neuf",
           "Manrope-Sb", 11, INK, track=-0.3)

    s.text(MARGIN, 193.5, "Demandez votre estimation", "Manrope-Sb", 9,
           INK, track=-0.2)
    s.text(MARGIN, 200, CONTACT["telephone"], "Manrope-Md", 8.5, INK)
    s.text(MARGIN, 205.5, CONTACT["email"], "Manrope-Md", 8.5, INK)

    qr = 24.0
    s.image(os.path.join(A, "qr.png"), TW - MARGIN - qr, 173, qr, qr)
    s.text(TW - MARGIN - qr / 2, 202, "Estimation en ligne", "Manrope-Bd",
           5.6, SAND_DEEP, track=0.8, align="c")


# --------------------------------------------------------------------------
def build(path, bleed):
    w, h = (TW + 2 * bleed) * mm, (TH + 2 * bleed) * mm
    c = canvas.Canvas(path, pagesize=(w, h))
    c.setTitle("Remis à Neuf — flyer A5")
    c.setAuthor("Remis à Neuf")

    for page in (recto, verso):
        s = Sheet(c, bleed)
        page(s)
        s.crop_marks()
        c.showPage()
    c.save()
    print("écrit :", os.path.basename(path))


def previews(pdf):
    import pymupdf
    doc = pymupdf.open(pdf)
    for i, label in enumerate(("recto", "verso")):
        pix = doc[i].get_pixmap(dpi=150)
        out = os.path.join(HERE, f"apercu-{label}.png")
        pix.save(out)
        print("écrit :", os.path.basename(out), pix.width, "x", pix.height)


if __name__ == "__main__":
    build(os.path.join(HERE, "flyer-A5-impression.pdf"), BLEED)
    build(os.path.join(HERE, "flyer-A5-apercu.pdf"), 0.0)
    previews(os.path.join(HERE, "flyer-A5-apercu.pdf"))
