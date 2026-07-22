from flask import render_template

from . import main

from services.validade_service import listar_validade


@main.route("/validade")
def validade():

    vencidos, proximos = listar_validade()

    return render_template(
        "validade.html",
        vencidos=vencidos,
        proximos=proximos
    )