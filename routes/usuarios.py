from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required

from . import main
from models import Usuario, db


@main.route("/usuarios")
@login_required
def usuarios():

    usuarios = Usuario.query.order_by(Usuario.nome).all()

    return render_template(
        "usuarios.html",
        usuarios=usuarios
    )


@main.route("/usuarios/novo", methods=["GET", "POST"])
@login_required
def novo_usuario():

    if request.method == "POST":

        # Verifica se já existe usuário com esse e-mail
        existe = Usuario.query.filter_by(
            email=request.form["email"]
        ).first()

        if existe:
            flash("Já existe um usuário com esse e-mail.", "danger")
            return redirect(url_for("main.novo_usuario"))

        usuario = Usuario(
            nome=request.form["nome"],
            email=request.form["email"],
            perfil=request.form["perfil"],
            ativo="ativo" in request.form
        )

        usuario.set_senha(request.form["senha"])

        db.session.add(usuario)
        db.session.commit()

        flash("Usuário cadastrado com sucesso!", "success")

        return redirect(url_for("main.usuarios"))

    return render_template("usuario_form.html")

@main.route("/usuarios/<int:id>/editar", methods=["GET", "POST"])
@login_required
def editar_usuario(id):

    usuario = Usuario.query.get_or_404(id)

    if request.method == "POST":

        usuario.nome = request.form["nome"]
        usuario.email = request.form["email"]
        usuario.perfil = request.form["perfil"]
        usuario.ativo = "ativo" in request.form

        db.session.commit()

        flash("Usuário atualizado com sucesso!", "success")

        return redirect(url_for("main.usuarios"))

    return render_template(
        "usuario_form.html",
        usuario=usuario
    )