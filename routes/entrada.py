from datetime import datetime
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import flash

from . import main

from models import Produto

from services.entrada_service import registrar_entrada


@main.route("/entrada", methods=["GET", "POST"])
def entrada():

    produtos = Produto.query.order_by(Produto.nome).all()

    if request.method == "POST":

        try:

            registrar_entrada(

                produto_id=int(request.form["produto"]),

                quantidade=float(request.form["quantidade"]),

                lote=request.form["lote"],

                validade=datetime.strptime(
                    request.form["validade"],
                    "%Y-%m-%d"
                ).date(),

                fornecedor=request.form["fornecedor"],

                nota_fiscal=request.form["nota_fiscal"],

                valor_unitario=float(
                    request.form["valor_unitario"] or 0
                ),

                responsavel=request.form["responsavel"],

                observacao=request.form["observacao"]

            )

            flash("Entrada registrada com sucesso!", "success")

            return redirect(url_for("main.entrada"))

        except Exception as erro:

            flash(str(erro), "danger")

    return render_template(
        "entrada.html",
        produtos=produtos
    )