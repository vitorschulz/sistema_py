from flask import Blueprint, render_template, request, redirect
from app.config import get_db_connection

clientes = Blueprint("clientes", __name__)

@clientes.route("/clientes/<int:id>")
def ver_cliente(id):

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM clientes WHERE id = %s", (id,))
    cliente = cursor.fetchone()
    

    return render_template("cliente_detalhe.html", cliente=cliente)

@clientes.route("/clientes")
def listar_clientes():

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT * FROM clientes
        WHERE ativo = TRUE
        ORDER BY nome
    """)

    clientes_lista = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("clientes.html", clientes=clientes_lista)


@clientes.route("/clientes/novo", methods=["GET", "POST"])
def novo_cliente():

    if request.method == "POST":

        nome = request.form["nome"]
        cpf_cnpj = request.form["cpf_cnpj"]
        telefone = request.form["telefone"]
        email = request.form["email"]
        observacoes = request.form["observacoes"]

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO clientes
            (nome, cpf_cnpj, telefone, email, observacoes)
            VALUES (%s,%s,%s,%s,%s)
        """, (nome, cpf_cnpj, telefone, email, observacoes))

        conn.commit()

        cursor.close()
        conn.close()

        return redirect("/clientes")

    return render_template("novo_cliente.html")