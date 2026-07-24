from sqlalchemy import func

from flask import render_template

from . import main

from models import db
from models import Produto
from models import Movimentacao
from models import Lote


@main.route("/")
def dashboard():

    total_produtos = Produto.query.count()

    estoque_baixo = Produto.query.filter(
        Produto.estoque_atual <= Produto.estoque_minimo
    ).count()

    valor_total = 0

    produtos = Produto.query.all()

    for produto in produtos:

        ultima = (
            Movimentacao.query.filter_by(produto_id=produto.id)
            .order_by(Movimentacao.data.desc())
            .first()
        )

        if ultima and ultima.valor_unitario:
            valor_total += (
                produto.estoque_atual *
                ultima.valor_unitario
            )

    vencidos = Lote.query.filter(
        Lote.validade < db.func.current_date()
    ).count()

    produtos_baixo = (
        Produto.query
        .filter(Produto.estoque_atual <= Produto.estoque_minimo)
        .order_by(Produto.nome)
        .all()
    )

    movimentacoes = (
        Movimentacao.query
        .order_by(Movimentacao.data.desc())
        .limit(10)
        .all()
    )

    entradas = db.session.query(
        func.sum(Movimentacao.quantidade)
    ).filter(
        Movimentacao.tipo == "ENTRADA"
    ).scalar() or 0

    saidas = db.session.query(
        func.sum(Movimentacao.quantidade)
    ).filter(
        Movimentacao.tipo == "SAIDA"
    ).scalar() or 0

    return render_template(
        "dashboard.html",
        total_produtos=total_produtos,
        estoque_baixo=estoque_baixo,
        valor_total=valor_total,
        vencidos=vencidos,
        movimentacoes=movimentacoes,
        produtos_baixo=produtos_baixo,
        entradas=entradas,
        saidas=saidas
    )