from io import BytesIO
from flask import send_file
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

from . import main
from models import Produto


@main.route("/relatorio/pdf")
def relatorio_pdf():

    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer, pagesize=A4)

    styles = getSampleStyleSheet()

    elementos = []

    elementos.append(
        Paragraph("<b>UAN CONTROL PRO</b>", styles["Title"])
    )

    elementos.append(
        Paragraph("Relatório Geral do Estoque", styles["Heading2"])
    )

    dados = [
        ["Produto", "Categoria", "Estoque", "Mínimo"]
    ]

    produtos = Produto.query.order_by(Produto.nome).all()

    for p in produtos:

        dados.append([
            p.nome,
            p.categoria,
            str(p.estoque_atual),
            str(p.estoque_minimo)
        ])

    tabela = Table(dados)

    tabela.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#198754")),
        ("TEXTCOLOR",(0,0),(-1,0),colors.white),
        ("GRID",(0,0),(-1,-1),1,colors.grey),
        ("BACKGROUND",(0,1),(-1,-1),colors.beige),
        ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),
        ("BOTTOMPADDING",(0,0),(-1,0),10),
    ]))

    elementos.append(tabela)

    doc.build(elementos)

    buffer.seek(0)

    return send_file(
        buffer,
        as_attachment=True,
        download_name="Relatorio_UAN_Control_Pro.pdf",
        mimetype="application/pdf",
    )