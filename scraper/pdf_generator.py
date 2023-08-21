from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors

def generate_pdf(properties, file_path):
    pdf = SimpleDocTemplate(file_path, pagesize=letter)
    data = [["Property ID", "Address", "Price", "Date Sold", "Link"]]

    for property in properties:
        row = [property['property_id'],
               f"{property['adress_line1']} {property['address_line2']}",
               f"${property['price_string']}" + ("*" if property['approx_price'] else ""),
               property['sold_status_date'],
               property['property_url']]
        data.append(row)

    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))

    pdf.build([table])
