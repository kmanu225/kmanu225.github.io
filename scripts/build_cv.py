"""Build the downloadable CV from the same data used by Jekyll.
Usage: python scripts/build_cv.py [--render]
Dependencies: reportlab, pypdf; optional pypdfium2 for visual QA.
"""
from pathlib import Path
from xml.sax.saxutils import escape
import json
import shutil
import sys
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, KeepTogether
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]
data = json.loads((ROOT / "_data/cv.json").read_text(encoding="utf-8"))
out = ROOT / "output/pdf"
out.mkdir(parents=True, exist_ok=True)
font_candidates = [
    (Path("C:/Windows/Fonts/arial.ttf"), Path("C:/Windows/Fonts/arialbd.ttf")),
    (Path("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"), Path("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf")),
]
regular, bold = next((pair for pair in font_candidates if all(p.exists() for p in pair)), (None, None))
if regular is None:
    raise RuntimeError("Install Arial or DejaVu Sans to build the CV.")
pdfmetrics.registerFont(TTFont("CV", str(regular)))
pdfmetrics.registerFont(TTFont("CV-Bold", str(bold)))
pdfmetrics.registerFontFamily("CV", normal="CV", bold="CV-Bold", italic="CV", boldItalic="CV-Bold")
ink, muted, accent = colors.HexColor("#14283b"), colors.HexColor("#526476"), colors.HexColor("#05594f")
styles = {
    "name": ParagraphStyle("name", fontName="CV-Bold", fontSize=28, leading=32, textColor=ink, spaceAfter=8),
    "subtitle": ParagraphStyle("subtitle", fontName="CV-Bold", fontSize=11, leading=15, textColor=accent, spaceAfter=12),
    "body": ParagraphStyle("body", fontName="CV", fontSize=9.3, leading=13.6, textColor=ink, spaceAfter=6),
    "small": ParagraphStyle("small", fontName="CV", fontSize=8.1, leading=11.5, textColor=muted, spaceAfter=7),
    "section": ParagraphStyle("section", fontName="CV-Bold", fontSize=10.5, leading=14, textColor=accent, spaceBefore=16, spaceAfter=9, keepWithNext=True),
    "entry": ParagraphStyle("entry", fontName="CV-Bold", fontSize=9.6, leading=13.2, textColor=ink, spaceAfter=4, keepWithNext=True),
    "bullet": ParagraphStyle("bullet", fontName="CV", fontSize=9.3, leading=13.6, textColor=ink, leftIndent=9, firstLineIndent=-9, spaceAfter=5),
}
def clean(text):
    return escape(text.replace("\u2014", "-").replace("–", "-").replace("\u2011", "-"))
def p(text, style="body"):
    return Paragraph(clean(text), styles[style])
def link(label, url):
    return Paragraph(f'<link href="{escape(url)}" color="#05594f">{clean(label)}</link>', styles["small"])
def heading(text):
    return p(text.upper(), "section")
story = [p(data["name"], "name"), p(data["headline"], "subtitle")]
story += [Paragraph(f'<link href="mailto:{data["email"]}" color="#05594f">{data["email"]}</link> | <link href="{data["website"]}" color="#05594f">kmanu225.github.io</link>', styles["small"]),
          Paragraph(f'<link href="{data["linkedin"]}" color="#05594f">LinkedIn: emmanuel-konan</link> | <link href="{data["github"]}" color="#05594f">GitHub: kmanu225</link>', styles["small"]),
          p(data["location"] + " | " + data["languages"], "small"),
          Spacer(1, 4), p(data["summary"])]
story.append(heading("Professional experience"))
for entry in data["experience"]:
    story += [p(entry["role"], "entry"), p(entry["organization"] + " | " + entry["period"], "small")]
    story += [p("- " + bullet, "bullet") for bullet in entry["bullets"]]
    story.append(Spacer(1, 5))
story += [heading("Public cryptography contribution"), p(data["contribution"]["title"], "entry"),
          p(data["contribution"]["text"]), link("IETF Datatracker: draft-eap-psk-256", data["contribution"]["url"])]
story.append(PageBreak())
story += [p(data["name"], "name"), p("Technical capabilities, education & leadership", "subtitle")]
story.append(heading("Technical capabilities"))
for item in data["skills"]:
    story.append(KeepTogether([p(item["title"], "entry"), p(item["text"])]))
story.append(heading("Education"))
for item in data["education"]:
    story.append(KeepTogether([p(item["title"], "entry"), p(item["organization"] + " | " + item["period"], "small"), p(item["text"])]))
story.append(heading("Certifications"))
story.append(p("  |  ".join(item["title"] + " (" + item["year"] + ")" for item in data["certifications"])))
story.append(heading("Leadership & community"))
for item in data["leadership"]:
    story.append(KeepTogether([p(item["title"], "entry"), p(item["period"], "small"), p(item["text"])]))
def footer(canvas, doc):
    canvas.setStrokeColor(colors.HexColor("#dce3e9"))
    canvas.line(43, 39, A4[0]-43, 39)
    canvas.setFont("CV", 7.3)
    canvas.setFillColor(muted)
    canvas.drawString(43, 26, "Emmanuel Konan | Cybersecurity & Applied Cryptography")
    canvas.drawRightString(A4[0]-43, 26, str(doc.page))
pdf_path = out / "emmanuel-konan-cv.pdf"
doc = SimpleDocTemplate(str(pdf_path), pagesize=A4, rightMargin=43, leftMargin=43, topMargin=39, bottomMargin=53,
                        title="Emmanuel Konan - Cybersecurity & Applied Cryptography", author="Emmanuel Konan")
doc.build(story, onFirstPage=footer, onLaterPages=footer)
reader = PdfReader(str(pdf_path))
assert len(reader.pages) == 2, f"CV must fit two pages, got {len(reader.pages)}"
text = "\n".join(page.extract_text() for page in reader.pages)
for expected in ("Emmanuel Konan", "PKCS#11", "EAP-PSK-256", "CentraleSup", "Visiting Student"):
    assert expected in text, expected
destination = ROOT / "files/emmanuel-konan-cv.pdf"
destination.parent.mkdir(exist_ok=True)
shutil.copyfile(pdf_path, destination)
if "--render" in sys.argv:
    import pypdfium2 as pdfium
    rendered = ROOT / "tmp/pdfs"
    rendered.mkdir(parents=True, exist_ok=True)
    pdf = pdfium.PdfDocument(str(pdf_path))
    for index in range(len(pdf)):
        page = pdf[index]
        page.render(scale=1.6).to_pil().save(rendered / f"cv-page-{index+1}.png")
print(f"Generated {destination}; verified {len(reader.pages)} pages and expected content.")
