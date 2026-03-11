from flask import Blueprint, render_template

clientes = Blueprint("clientes", __name__)

@clientes.route("/clientes")
def listar_clientes():
    return render_template("clientes.html")

@clientes.route("/clientes/novo")
def novo_cliente():
    return render_template("novo_cliente.html")