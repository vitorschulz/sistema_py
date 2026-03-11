from flask import Blueprint, render_template

shopping = Blueprint("shopping", __name__)

@shopping.route("/shopping")
def listar_shopping():
    return render_template("shoppings.html")

@shopping.route("/shopping/novo")
def novo_shopping():
    return render_template("novo_shopping.html")