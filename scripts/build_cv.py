"""Build an ATS-friendly CV (McKinsey-style layout) from the same data used by Jekyll.

Usage: python scripts/build_cv.py [--render]
Dependencies: reportlab, pypdf; optional pypdfium2 for visual QA.
"""
from math import acos, ceil, cos, hypot, pi, radians, sin, sqrt, tan
from pathlib import Path
from xml.sax.saxutils import escape
import json
import re
import shutil
import sys

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.graphics.shapes import Circle, Drawing, Group, Path as SvgPath, Rect
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    KeepTogether,
    Table,
    TableStyle,
    HRFlowable,
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen.canvas import Canvas
from pypdf import PdfReader


SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent if (SCRIPT_DIR.parent / "_data/cv.json").exists() else SCRIPT_DIR
DATA_PATH = PROJECT_ROOT / "_data/cv.json"
if not DATA_PATH.exists():
    raise FileNotFoundError(f"Could not find CV data at {DATA_PATH}")

data = json.loads(DATA_PATH.read_text(encoding="utf-8"))
out = PROJECT_ROOT / "output/pdf"
out.mkdir(parents=True, exist_ok=True)

font_candidates = [
    (Path("C:/Windows/Fonts/arial.ttf"), Path("C:/Windows/Fonts/arialbd.ttf")),
    (
        Path("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"),
        Path("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"),
    ),
]
regular, bold = next((pair for pair in font_candidates if all(p.exists() for p in pair)), (None, None))
if regular is None:
    raise RuntimeError("Install Arial or DejaVu Sans to build the CV.")

pdfmetrics.registerFont(TTFont("CV", str(regular)))
pdfmetrics.registerFont(TTFont("CV-Bold", str(bold)))
pdfmetrics.registerFontFamily("CV", normal="CV", bold="CV-Bold", italic="CV", boldItalic="CV-Bold")

# Mirrors assets/css/professional.css so the PDF and the website share one identity.
INK = colors.HexColor("#111111")
MUTED = colors.HexColor("#4A4A4A")
ACCENT = colors.HexColor("#08756a")
ACCENT_DARK = colors.HexColor("#05594f")
SURFACE = colors.white
RULE = ACCENT
ACCENT_HEX = "#08756a"
DATE_COL = 36 * mm

styles = {
    "name": ParagraphStyle(
        "name", fontName="CV-Bold", fontSize=15, leading=17.5, textColor=INK,
        alignment=TA_CENTER, spaceAfter=0
    ),
    "headline": ParagraphStyle(
        "headline", fontName="CV-Bold", fontSize=9.2, leading=11.5, textColor=ACCENT,
        alignment=TA_CENTER, spaceAfter=0
    ),
    "contact": ParagraphStyle(
        "contact", fontName="CV", fontSize=8.2, leading=10.8, textColor=MUTED,
        alignment=TA_CENTER, spaceAfter=0
    ),
    "section": ParagraphStyle(
        "section", fontName="CV-Bold", fontSize=9.2, leading=11, textColor=ACCENT,
        spaceBefore=0, spaceAfter=0, keepWithNext=True
    ),
    "org": ParagraphStyle(
        "org", fontName="CV-Bold", fontSize=9.0, leading=11.4, textColor=ACCENT_DARK,
        spaceAfter=0, keepWithNext=True
    ),
    "role": ParagraphStyle(
        "role", fontName="CV-Bold", fontSize=8.6, leading=11, textColor=INK,
        spaceAfter=0, keepWithNext=True
    ),
    "date": ParagraphStyle(
        "date", fontName="CV", fontSize=8.3, leading=11, textColor=INK,
        alignment=TA_RIGHT, spaceAfter=0, keepWithNext=True
    ),
    "body": ParagraphStyle(
        "body", fontName="CV", fontSize=8.4, leading=11.2, textColor=INK, spaceAfter=0
    ),
    "bullet": ParagraphStyle(
        "bullet", fontName="CV", fontSize=8.4, leading=11.2, textColor=INK,
        leftIndent=13, firstLineIndent=-9, spaceAfter=1.6
    ),
    "numbered": ParagraphStyle(
        "numbered", fontName="CV", fontSize=8.4, leading=11.2, textColor=INK,
        leftIndent=13, firstLineIndent=-13, spaceAfter=2.5
    ),
    "label": ParagraphStyle(
        "label", fontName="CV-Bold", fontSize=8.4, leading=11.2, textColor=INK, spaceAfter=0
    ),
}


# --- Vector icons -----------------------------------------------------------
# Path data copied verbatim from _includes/icon.html so the PDF and the site draw
# the same glyphs. Shape kinds: stroke/fill use the accent colour, "on" variants
# are knocked out in white on top of a filled accent shape.
ICONS = {
    "mail": [
        ("rect", 3, 5, 18, 14, 2),
        ("stroke", "m3 6 9 7 9-7"),
    ],
    "linkedin": [
        ("fill-rect", 2, 2, 20, 20, 2),
        ("on-stroke", "M6.5 10v8M11 18v-8m0 4a4 4 0 0 1 7 0v4", 2.0),
        ("on-circle", 6.5, 6.5, 1.2),
    ],
    "github": [
        ("fill", "M12 .8a11.2 11.2 0 0 0-3.54 21.83c.56.1.76-.24.76-.54v-2.1c-3.11.68-3.77-1.32-3.77-1.32"
                 "-.51-1.3-1.24-1.65-1.24-1.65-1.02-.7.08-.69.08-.69 1.12.08 1.71 1.15 1.71 1.15.99 1.7 2.6 1.21 3.24.93"
                 ".1-.73.39-1.21.71-1.49-2.48-.28-5.09-1.24-5.09-5.53 0-1.22.44-2.22 1.15-3-.12-.28-.5-1.42.11-2.96"
                 " 0 0 .94-.3 3.08 1.15a10.7 10.7 0 0 1 5.6 0c2.14-1.45 3.08-1.15 3.08-1.15.61 1.54.23 2.68.11 2.96"
                 ".71.78 1.15 1.78 1.15 3 0 4.3-2.61 5.24-5.1 5.52.4.35.76 1.03.76 2.08v3.1c0 .3.2.65.77.54A11.2 11.2 0 0 0 12 .8Z"),
    ],
    "arrow-up-right": [("stroke", "M7 17 17 7M7 7h10v10")],
    "factory": [("stroke", "M3 21V3h4v11l7-5v5l7-5v12ZM7 7H3M7 17h1m4 0h1m4 0h1")],
    "book": [("stroke", "M5 3h14v18H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2Zm-2 14h16M7 7h8M7 11h6")],
    "file": [("stroke", "M14 3H6a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V9Zm0 0v6h6M8 13h8M8 17h6")],
    "user": [
        ("circle", 12, 7, 4),
        ("stroke", "M4 21v-2a8 8 0 0 1 16 0v2"),
    ],
}

NUMBER = re.compile(r"[-+]?(?:\d*\.\d+|\d+\.?\d*)(?:[eE][-+]?\d+)?")
COMMAND = re.compile(r"[MmLlHhVvCcAaZz]")


def _arc_to_curves(x0, y0, rx, ry, rotation, large_arc, sweep, x1, y1):
    """Convert an SVG elliptical arc into cubic Bezier segments (SVG spec F.6)."""
    if rx == 0 or ry == 0:
        return [("line", x1, y1)]
    phi = radians(rotation)
    cos_phi, sin_phi = cos(phi), sin(phi)
    dx, dy = (x0 - x1) / 2, (y0 - y1) / 2
    xp = cos_phi * dx + sin_phi * dy
    yp = -sin_phi * dx + cos_phi * dy
    rx, ry = abs(rx), abs(ry)
    oversize = (xp * xp) / (rx * rx) + (yp * yp) / (ry * ry)
    if oversize > 1:
        scale = sqrt(oversize)
        rx, ry = rx * scale, ry * scale
    denominator = rx * rx * yp * yp + ry * ry * xp * xp
    numerator = rx * rx * ry * ry - denominator
    factor = sqrt(max(0.0, numerator / denominator)) if denominator else 0.0
    if large_arc == sweep:
        factor = -factor
    cxp = factor * rx * yp / ry
    cyp = -factor * ry * xp / rx
    cx = cos_phi * cxp - sin_phi * cyp + (x0 + x1) / 2
    cy = sin_phi * cxp + cos_phi * cyp + (y0 + y1) / 2

    def angle(ux, uy, vx, vy):
        norm = hypot(ux, uy) * hypot(vx, vy)
        if not norm:
            return 0.0
        value = acos(max(-1.0, min(1.0, (ux * vx + uy * vy) / norm)))
        return -value if ux * vy - uy * vx < 0 else value

    ux, uy = (xp - cxp) / rx, (yp - cyp) / ry
    vx, vy = (-xp - cxp) / rx, (-yp - cyp) / ry
    theta = angle(1, 0, ux, uy)
    sweep_angle = angle(ux, uy, vx, vy)
    if not sweep and sweep_angle > 0:
        sweep_angle -= 2 * pi
    elif sweep and sweep_angle < 0:
        sweep_angle += 2 * pi

    segments = max(1, ceil(abs(sweep_angle) / (pi / 2)))
    delta = sweep_angle / segments
    # Bezier control-point distance that best approximates a circular arc of `delta`.
    alpha = 4 / 3 * tan(delta / 4)
    curves = []
    for index in range(segments):
        start = theta + index * delta
        end = start + delta
        cos_s, sin_s, cos_e, sin_e = cos(start), sin(start), cos(end), sin(end)

        def point(c, s):
            return (
                cx + rx * cos_phi * c - ry * sin_phi * s,
                cy + rx * sin_phi * c + ry * cos_phi * s,
            )

        px0, py0 = point(cos_s, sin_s)
        px1, py1 = point(cos_e, sin_e)
        dx0 = -rx * cos_phi * sin_s - ry * sin_phi * cos_s
        dy0 = -rx * sin_phi * sin_s + ry * cos_phi * cos_s
        dx1 = -rx * cos_phi * sin_e - ry * sin_phi * cos_e
        dy1 = -rx * sin_phi * sin_e + ry * cos_phi * cos_e
        curves.append((
            "curve",
            px0 + alpha * dx0, py0 + alpha * dy0,
            px1 - alpha * dx1, py1 - alpha * dy1,
            px1, py1,
        ))
    return curves


def _parse_path(data):
    """Turn an SVG `d` attribute into reportlab Path operations."""
    tokens = []
    position = 0
    while position < len(data):
        command = COMMAND.match(data, position)
        if command:
            tokens.append(command.group())
            position = command.end()
            continue
        number = NUMBER.match(data, position)
        if number:
            tokens.append(float(number.group()))
            position = number.end()
            continue
        position += 1

    operations = []
    x = y = start_x = start_y = 0.0
    command = None
    index = 0
    while index < len(tokens):
        if isinstance(tokens[index], str):
            command = tokens[index]
            index += 1
            if command in "Zz":
                operations.append(("close",))
                x, y = start_x, start_y
                continue
        elif command in ("M", "m"):
            # Extra coordinate pairs after a moveto are implicit linetos.
            command = "L" if command == "M" else "l"
        relative = command.islower()
        kind = command.upper()
        take = {"M": 2, "L": 2, "H": 1, "V": 1, "C": 6, "A": 7}[kind]
        args = tokens[index:index + take]
        index += take
        if kind in ("M", "L"):
            nx, ny = args
            nx, ny = (x + nx, y + ny) if relative else (nx, ny)
            operations.append(("move" if kind == "M" else "line", nx, ny))
            if kind == "M":
                start_x, start_y = nx, ny
            x, y = nx, ny
        elif kind == "H":
            x = x + args[0] if relative else args[0]
            operations.append(("line", x, y))
        elif kind == "V":
            y = y + args[0] if relative else args[0]
            operations.append(("line", x, y))
        elif kind == "C":
            points = [(x + args[i] if relative else args[i], y + args[i + 1] if relative else args[i + 1])
                      for i in (0, 2, 4)]
            operations.append(("curve", *points[0], *points[1], *points[2]))
            x, y = points[2]
        else:
            rx, ry, rotation, large_arc, sweep, dx, dy = args
            nx, ny = (x + dx, y + dy) if relative else (dx, dy)
            operations.extend(_arc_to_curves(x, y, rx, ry, rotation, int(large_arc), int(sweep), nx, ny))
            x, y = nx, ny
    return operations


def _build_path(data, **kwargs):
    path = SvgPath(**kwargs)
    for operation in _parse_path(data):
        if operation[0] == "move":
            path.moveTo(*operation[1:])
        elif operation[0] == "line":
            path.lineTo(*operation[1:])
        elif operation[0] == "curve":
            path.curveTo(*operation[1:])
        else:
            path.closePath()
    return path


def icon(name, size=9.0, color=ACCENT):
    """Render a site icon as a vector Drawing, flipping the SVG's y-down axis."""
    scale = size / 24.0
    stroke = dict(strokeColor=color, fillColor=None, strokeWidth=1.8,
                  strokeLineCap=1, strokeLineJoin=1)
    group = Group()
    for shape in ICONS[name]:
        kind = shape[0]
        if kind == "stroke":
            group.add(_build_path(shape[1], **stroke))
        elif kind == "fill":
            group.add(_build_path(shape[1], strokeColor=None, fillColor=color))
        elif kind == "on-stroke":
            group.add(_build_path(shape[1], **{**stroke, "strokeColor": SURFACE, "strokeWidth": shape[2]}))
        elif kind == "rect":
            _, rx, ry, width, height, radius = shape
            group.add(Rect(rx, ry, width, height, rx=radius, ry=radius, **stroke))
        elif kind == "fill-rect":
            _, rx, ry, width, height, radius = shape
            group.add(Rect(rx, ry, width, height, rx=radius, ry=radius,
                           strokeColor=None, fillColor=color))
        elif kind == "circle":
            group.add(Circle(shape[1], shape[2], shape[3], **stroke))
        else:
            group.add(Circle(shape[1], shape[2], shape[3], strokeColor=None, fillColor=SURFACE))
    group.transform = (scale, 0, 0, -scale, 0, size)
    drawing = Drawing(size, size)
    drawing.add(group)
    return drawing


def icon_row(pairs, style, gap=3.0, separator=None, align="LEFT"):
    """Lay out [icon, text] pairs on one line with widths measured, not guessed."""
    cells, widths = [], []
    text_style = styles[style]
    for index, (name, markup, plain) in enumerate(pairs):
        if index and separator:
            cells.append(Paragraph(separator, text_style))
            widths.append(pdfmetrics.stringWidth(" | ", text_style.fontName, text_style.fontSize))
        if name:
            cells.append(icon(name, size=text_style.fontSize * 1.15))
            widths.append(text_style.fontSize * 1.15 + gap)
        cells.append(Paragraph(markup, text_style))
        widths.append(pdfmetrics.stringWidth(plain, text_style.fontName, text_style.fontSize) + 1.5)
    table = Table([cells], colWidths=widths, hAlign=align)
    table.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
    ]))
    return table


def clean(text):
    """Escape user data while normalizing dash characters for reliable PDF rendering."""
    return escape(str(text).replace("\u2014", "-").replace("\u2013", "-").replace("\u2011", "-"))


def p(text, style="body"):
    return Paragraph(clean(text), styles[style])


def rich(text, style="body"):
    """Create a paragraph from markup assembled only by this script."""
    return Paragraph(text, styles[style])


def link_markup(label, url):
    return f'<link href="{escape(str(url))}" color="{ACCENT_HEX}">{clean(label)}</link>'


def section_heading(text, icon_name, *follow):
    """All-caps heading over a full-width rule - the McKinsey scanning anchor.

    Any `follow` flowables are glued to the heading so it never strands at a page bottom.
    """
    label = text.upper()
    return KeepTogether([
        Spacer(1, 7),
        icon_row([(icon_name, clean(label), label)], "section"),
        HRFlowable(width="100%", thickness=0.7, color=RULE, spaceBefore=1.5, spaceAfter=4),
        *follow,
    ])


def date_row(left, period, left_style):
    """Title on the left, dates flush right on the same baseline."""
    row = Table(
        [[p(left, left_style) if isinstance(left, str) else left, p(period, "date")]],
        colWidths=[None, DATE_COL],
        hAlign="LEFT",
    )
    row.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "BOTTOM"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
    ]))
    return row


def bullet_markup(markup):
    # Numeric entity avoids font/encoding surprises while retaining a true bullet glyph.
    return Paragraph(f"&#8226;&nbsp;&nbsp;{markup}", styles["bullet"])


def bullet(text):
    return bullet_markup(clean(text))


def span_period(periods):
    """Collapse several role periods into the employer-level range (latest start -> newest end)."""
    if len(periods) == 1:
        return periods[0]
    parts = [re.split(r"\s*[-\u2010-\u2015]\s*", period) for period in periods]
    start = parts[-1][0]
    end = parts[0][-1]
    return f"{start} - {end}"


def labelled_rows(rows):
    """Bold labels in their own column so wrapped text aligns instead of running on."""
    label_style = styles["label"]
    width = max(
        pdfmetrics.stringWidth(f"{label}:  ", label_style.fontName, label_style.fontSize)
        for label, _ in rows
    )
    table = Table(
        [[p(f"{label}:", "label"), value if isinstance(value, list) else rich(value, "body")]
         for label, value in rows],
        colWidths=[width, None],
        hAlign="LEFT",
    )
    table.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    return table


def group_by_employer(entries):
    """The template lists one employer heading with its successive titles nested beneath."""
    groups = []
    for entry in entries:
        if groups and groups[-1]["organization"] == entry["organization"]:
            groups[-1]["roles"].append(entry)
        else:
            groups.append({"organization": entry["organization"], "roles": [entry]})
    return groups


# --- Document story ---------------------------------------------------------
story = []

# Heading block: centred identity, then a single pipe-separated contact line.
story.extend([
    p(data["name"].upper(), "name"),
    Spacer(1, 1.5),
    p(data["headline"], "headline"),
    Spacer(1, 4),
    # Icons identify each channel, so the labels stay short and the line stays on one row.
    icon_row(
        [
            ("mail", link_markup(data["email"], f'mailto:{data["email"]}'), data["email"]),
            ("arrow-up-right", link_markup("kmanu225.github.io", data["website"]), "kmanu225.github.io"),
            ("linkedin", link_markup("emmanuel-konan", data["linkedin"]), "emmanuel-konan"),
            ("github", link_markup("kmanu225", data["github"]), "kmanu225"),
        ],
        "contact",
        separator="|",
        align="CENTER",
    ),
    Spacer(1, 7),
    p(data["summary"], "body"),
])

story.append(section_heading("Relevant professional experience", "factory"))
employers = group_by_employer(data["experience"])
for group_index, group in enumerate(employers):
    periods = [role["period"] for role in group["roles"]]
    story.append(date_row(group["organization"], span_period(periods), "org"))
    single_role = len(group["roles"]) == 1
    for role in group["roles"]:
        story.append(Spacer(1, 3))
        # A lone title inherits the employer's dates, so repeating them adds only noise.
        story.append(p(role["role"], "role") if single_role
                     else date_row(role["role"], role["period"], "role"))
        if role.get("summary"):
            story.append(Spacer(1, 1.5))
            story.append(p(role["summary"], "body"))
        story.append(Spacer(1, 2.5))
        story.extend(bullet(item) for item in role["bullets"])
    if group_index != len(employers) - 1:
        story.append(Spacer(1, 5))

for index, item in enumerate(data["education"]):
    parts = [
        p(item["organization"], "org"),
        Spacer(1, 1.5),
        date_row(item["title"], item["period"], "role"),
        Spacer(1, 1.5),
        p(item["text"], "body"),
    ]
    # Nesting KeepTogether inside KeepTogether makes reportlab overestimate the block,
    # so the heading absorbs the first entry's parts directly instead.
    story.append(section_heading("Education", "book", *parts) if index == 0 else KeepTogether(parts))
    if index != len(data["education"]) - 1:
        story.append(Spacer(1, 4))

contribution = data["contribution"]
story.append(section_heading("Publications & standards contributions", "file", rich(
    f'1.&nbsp;&nbsp;<b>{clean(contribution["title"])}</b> '
    f'IETF Internet-Draft, {clean(contribution["period"])}. {clean(contribution["text"])} '
    f'{link_markup("datatracker.ietf.org/doc/draft-eap-psk-256", contribution["url"])}',
    "numbered",
)))

def community_entry(item):
    """Leadership titles read 'Organization - Role'; the PDF leads with the role and links the org."""
    organization, separator, role = item["title"].partition(" - ")
    if not separator:
        organization, role = item["title"], None
    name = link_markup(organization, item["url"]) if item.get("url") else clean(organization)
    lead = f"{clean(role)}, {name}" if role else name
    return f'{lead} ({clean(item["period"])})'


# Short, scannable values: the detail lives in the sections above, so these stay one line each.
story.append(section_heading("Skills & interests", "user", labelled_rows([
    (
        "Certifications",
        "; ".join(f'{clean(item["title"])} ({clean(item["year"])})' for item in data["certifications"]),
    ),
    ("Languages", clean(data["languages"]).rstrip(".")),
    ("Core strengths", "; ".join(clean(item["title"]) for item in data["skills"])),
    (
        "Community",
        [bullet_markup(community_entry(item)) for item in data["leadership"]],
    ),
])))


class NumberedCanvas(Canvas):
    """Two-pass canvas so the footer can show 'Page X of Y'."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_states = []

    def showPage(self):
        self._saved_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        total = len(self._saved_states)
        for state in self._saved_states:
            self.__dict__.update(state)
            self._draw_footer(total)
            super().showPage()
        super().save()

    def _draw_footer(self, total):
        self.saveState()
        x0, x1 = 16 * mm, A4[0] - 16 * mm
        self.setFont("CV", 7.2)
        self.setFillColor(MUTED)
        self.drawString(x0, 11 * mm, "Emmanuel Konan  |  Cybersecurity & Applied Cryptography")
        self.drawRightString(x1, 11 * mm, f"Page {self._pageNumber} of {total}")
        self.restoreState()


pdf_path = out / "emmanuel-konan-cv.pdf"
doc = SimpleDocTemplate(
    str(pdf_path),
    pagesize=A4,
    rightMargin=16 * mm,
    leftMargin=16 * mm,
    topMargin=14 * mm,
    bottomMargin=16 * mm,
    title="Emmanuel Konan - Cybersecurity & Applied Cryptography",
    author="Emmanuel Konan",
)
doc.build(story, canvasmaker=NumberedCanvas)

# Structural QA: keep the CV short and verify important technical keywords survived rendering.
reader = PdfReader(str(pdf_path))
assert len(reader.pages) <= 2, f"CV must fit two pages, got {len(reader.pages)}"
text = "\n".join(page.extract_text() or "" for page in reader.pages)
for expected in ("EMMANUEL KONAN", "PKCS#11", "EAP-PSK-256", "CentraleSup", "Advanced Hardware Security"):
    assert expected in text, expected

destination = PROJECT_ROOT / "files/emmanuel-konan-cv.pdf"
destination.parent.mkdir(exist_ok=True)
shutil.copyfile(pdf_path, destination)

if "--render" in sys.argv:
    import pypdfium2 as pdfium

    rendered = PROJECT_ROOT / "tmp/pdfs"
    rendered.mkdir(parents=True, exist_ok=True)
    pdf = pdfium.PdfDocument(str(pdf_path))
    for index in range(len(pdf)):
        page = pdf[index]
        page.render(scale=1.7).to_pil().save(rendered / f"cv-page-{index + 1}.png")

print(f"Generated {destination}; verified {len(reader.pages)} pages and expected content.")
