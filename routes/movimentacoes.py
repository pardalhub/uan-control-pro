from flask import render_template

from . import main

from models import Movimentacao


@main.route("/movimentacoes")
def movimentacoes():

    lista = Movimentacao.query.order_by(
        Movimentacao.data.desc()
    ).all()

    return render_template(
        "movimentacoes.html",
        movimentacoes=lista
    )