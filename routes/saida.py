from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import flash

from . import main

from models import Produto

from services.saida_service import registrar_saida


@main.route("/saida", methods=["GET", "POST"])
def saida():

    produtos = Produto.query.order_by(Produto.nome).all()

    if request.method == "POST":

        try:

            registrar_saida(

                produto_id=int(request.form["produto"]),

                quantidade=float(request.form["quantidade"]),

                responsavel=request.form["responsavel"],

                observacao=request.form["observacao"]

            )

            flash("Saída registrada com sucesso!", "success")

            return redirect(url_for("main.saida"))

        except Exception as erro:

            flash(str(erro), "danger")

    return render_template(

        "saida.html",

        produtos=produtos

    )