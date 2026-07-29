from flask import render_template
from flask_login import login_required
from datetime import date

from . import main
from models import Produto, Lote, Movimentacao


@main.route("/ia")
@login_required
def ia():

    produtos = Produto.query.all()

    abaixo = [
        p for p in produtos
        if p.estoque_atual <= p.estoque_minimo
    ]

    vencidos = Lote.query.filter(
        Lote.validade < date.today()
    ).count()

    proximos = Lote.query.filter(
        Lote.validade >= date.today()
    ).count()

    entradas = Movimentacao.query.filter_by(
        tipo="ENTRADA"
    ).count()

    saidas = Movimentacao.query.filter_by(
        tipo="SAIDA"
    ).count()

    analise = []

    if abaixo:
        analise.append({
            "titulo":"⚠ Estoque",
            "texto":f"Existem {len(abaixo)} produtos abaixo do estoque mínimo."
        })
    else:
        analise.append({
            "titulo":"✅ Estoque",
            "texto":"Nenhum produto está abaixo do estoque mínimo."
        })

    if vencidos:
        analise.append({
            "titulo":"🚨 Validade",
            "texto":f"Foram encontrados {vencidos} lotes vencidos."
        })
    else:
        analise.append({
            "titulo":"✅ Validade",
            "texto":"Nenhum lote vencido foi encontrado."
        })

    analise.append({
        "titulo":"📈 Movimentações",
        "texto":f"Foram registradas {entradas} entradas e {saidas} saídas."
    })

    if saidas > entradas:
        analise.append({
            "titulo":"🧠 Recomendação",
            "texto":"O consumo está maior que a reposição. Recomenda-se revisar o planejamento de compras."
        })

    return render_template(
        "ia.html",
        analise=analise
    )