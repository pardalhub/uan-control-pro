from datetime import datetime

from flask import send_file
from flask_login import login_required

from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

from . import main


@main.route("/relatorio/diario")
@login_required
def relatorio_diario():

    data_hoje = datetime.now()

    nome_arquivo = f"Relatorio_Diario_{data_hoje.strftime('%d-%m-%Y')}.pdf"

    pdf = SimpleDocTemplate(nome_arquivo, pagesize=A4)

    estilos = getSampleStyleSheet()

    elementos = []

    elementos.append(
        Paragraph("<b>UAN CONTROL PRO</b>", estilos["Title"])
    )

    elementos.append(
        Paragraph(
            f"Relatório Diário - {data_hoje.strftime('%d/%m/%Y')}",
            estilos["Heading2"]
        )
    )

    elementos.append(
        Paragraph(
            "Esta é a estrutura inicial do relatório diário.",
            estilos["BodyText"]
        )
    )

    pdf.build(elementos)

    return send_file(
        nome_arquivo,
        as_attachment=True
    )