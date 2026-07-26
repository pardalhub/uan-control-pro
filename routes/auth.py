from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required

from . import main
from models import Usuario


@main.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        senha = request.form["senha"]

        print("================================")
        print("Email digitado:", email)

        usuario = Usuario.query.filter_by(email=email).first()

        if usuario:

            print("Usuário encontrado:", usuario.nome)
            print("Hash salvo:", usuario.senha)
            print("Senha válida:", usuario.verificar_senha(senha))

            if usuario.verificar_senha(senha):

                print("LOGIN EFETUADO!")

                login_user(usuario)

                return redirect(url_for("main.dashboard"))

        else:

            print("Usuário NÃO encontrado.")

        print("================================")

        flash("E-mail ou senha incorretos.", "danger")

    return render_template("login.html")

@main.route("/logout")
@login_required
def logout():

    logout_user()

    return redirect(url_for("main.login"))