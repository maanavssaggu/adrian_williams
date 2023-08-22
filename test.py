from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


def generate_basic_pdf(file_path):
    print("i am downloading the pdf")
    c = canvas.Canvas(file_path, pagesize=letter)
    width, height = letter
    c.drawString(width / 2.5, height / 2, "test")
    c.save()

generate_basic_pdf("test.pdf")