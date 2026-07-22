from flask import render_template

from . import main

from models import Produto


@main.route("/compras")
def compras():

    produtos = Produto.query.filter(
        Produto.estoque_atual <= Produto.estoque_minimo
    ).order_by(
        Produto.nome
    ).all()

    return render_template(
        "compras.html",
        produtos=produtos
    )