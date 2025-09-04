from io import BytesIO
from docx import Document
from reportlab.pdfgen import canvas


def export_docx_bytes(text: str) -> bytes:
    doc = Document()
    for line in text.split("\n"):
        doc.add_paragraph(line)
    mem = BytesIO()
    doc.save(mem)
    mem.seek(0)
    return mem.read()


def export_pdf_bytes(text: str) -> bytes:
    mem = BytesIO()
    c = canvas.Canvas(mem)
    width, height = c._pagesize
    y = height - 50
    for line in text.split("\n"):
        c.drawString(50, y, line[:1000])
        y -= 18
        if y < 50:
            c.showPage()
            y = height - 50
    c.save()
    mem.seek(0)
    return mem.read()

