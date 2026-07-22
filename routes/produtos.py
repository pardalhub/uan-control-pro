from flask import render_template
from flask import request
from flask import redirect
from flask import url_for

from . import main

from models import db
from models import Produto


# ============================
# LISTAGEM
# ============================

@main.route("/produtos")
def produtos():

    busca = request.args.get("q", "")

    if busca:

        lista = Produto.query.filter(
            Produto.nome.contains(busca)
        ).order_by(
            Produto.nome
        ).all()

    else:

        lista = Produto.query.order_by(
            Produto.nome
        ).all()

    return render_template(
        "produtos.html",
        produtos=lista,
        busca=busca
    )


# ============================
# NOVO
# ============================

@main.route("/produtos/novo", methods=["GET", "POST"])
def novo_produto():

    if request.method == "POST":

        produto = Produto(

            nome=request.form["nome"],

            categoria=request.form["categoria"],

            unidade=request.form["unidade"],

            codigo_barras=request.form["codigo_barras"],

            fornecedor=request.form["fornecedor"],

            localizacao=request.form["localizacao"],

            estoque_minimo=float(request.form["estoque_minimo"]),

            estoque_maximo=float(request.form["estoque_maximo"]),

            observacao=request.form["observacao"]

        )

        db.session.add(produto)

        db.session.commit()

        return redirect(url_for("main.produtos"))

    return render_template(
        "produto_form.html",
        produto=None
    )


# ============================
# EDITAR
# ============================

@main.route("/produtos/<int:id>/editar", methods=["GET", "POST"])
def editar_produto(id):

    produto = Produto.query.get_or_404(id)

    if request.method == "POST":

        produto.nome = request.form["nome"]

        produto.categoria = request.form["categoria"]

        produto.unidade = request.form["unidade"]

        produto.codigo_barras = request.form["codigo_barras"]

        produto.fornecedor = request.form["fornecedor"]

        produto.localizacao = request.form["localizacao"]

        produto.estoque_minimo = float(request.form["estoque_minimo"])

        produto.estoque_maximo = float(request.form["estoque_maximo"])

        produto.observacao = request.form["observacao"]

        db.session.commit()

        return redirect(url_for("main.produtos"))

    return render_template(
        "produto_form.html",
        produto=produto
    )


# ============================
# EXCLUIR
# ============================

@main.route("/produtos/<int:id>/excluir")
def excluir_produto(id):

    produto = Produto.query.get_or_404(id)

    db.session.delete(produto)

    db.session.commit()

    return redirect(url_for("main.produtos"))