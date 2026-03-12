from flask import Blueprint, render_template

lojas = Blueprint("lojas", __name__)

@lojas.route("/lojas")
def listar_lojas():
    return render_template("lojas.html")

@lojas.route("/lojas/novo")
def nova_loja():
    return render_template("nova_loja.html")