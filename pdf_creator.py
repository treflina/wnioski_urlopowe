from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.units import cm, inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Spacer, Paragraph
from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from io import BytesIO


stylesheet = getSampleStyleSheet()

pdfmetrics.registerFont(TTFont('Arial', 'Arial.ttf'))
pdfmetrics.registerFont(TTFont('TNR', 'times.ttf'))
pdfmetrics.registerFont(TTFont('TNRB', 'timesbd.ttf'))


def create_pdf(data, fileName, type, start_date, end_date, person, position):\

      pdf=SimpleDocTemplate(
            fileName,
            pagesize=landscape(A4),
            rightMargin=100,
            leftMargin=100,
            topMargin=50,
            bottomMargin=50
      )

      table=Table(data)
      elems=[]
      style = ParagraphStyle(
            name='Title',
            fontName='TNR',
            fontSize=12,
            alignment=TA_CENTER)
      style1 = ParagraphStyle(
            name='footer',
            fontName='TNR',
            fontSize=10,
            alignment=TA_CENTER)
      elems.append(Paragraph(f"Wnioski {type} w okresie od {start_date} do {end_date}", style=style))
      elems.append(Spacer(1, 16))
      elems.append(Paragraph(f"{person} (stanowisko: {position})" , style=style))
      elems.append(Spacer(1, 20))
      elems.append(table)
      style_table=TableStyle([('FONTNAME', (0, 0), (-1, -1), 'TNR'), ('FONTSIZE', (0, 0), (-1, -1), 12),('GRID',(0,0),(-1,-1),1,colors.black)])
      table.setStyle(style_table)
      elems.append(Spacer(1, 20))
      elems.append(Paragraph("Wygenerowano automatycznie z Wnioski urlopowe 1.0", style=style1))

      pdf.build(elems)

