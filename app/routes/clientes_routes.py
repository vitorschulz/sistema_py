from flask import Blueprint, render_template, request, redirect
from app.config import get_db_connection

clientes = Blueprint("clientes", __name__)

#get do id pra ir pra telas de detalhe
@clientes.route("/clientes/<int:id>")
def ver_cliente(id):

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM clientes WHERE id = %s", (id,))
    cliente = cursor.fetchone()
    

    return render_template("cliente_detalhe.html", cliente=cliente)

#listagem de cliente
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


#funcao pro post do form
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

#botao editar
@clientes.route("/clientes/<int:id>/editar", methods=["GET", "POST"])
def editar_cliente(id):

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT * FROM clientes
        WHERE id = %s
    """, (id,))
    cliente = cursor.fetchone()

    if request.method == "POST":

        nome = request.form["nome"]
        cpf_cnpj = request.form["cpf_cnpj"]
        telefone = request.form["telefone"]
        email = request.form["email"]
        observacoes = request.form["observacoes"]

        cursor.execute("""
            UPDATE clientes
            SET nome=%s, cpf_cnpj=%s, telefone=%s, email=%s, observacoes=%s
            WHERE id=%s
        """, (nome, cpf_cnpj, telefone, email, observacoes, id))

        conn.commit()

        cursor.close()
        conn.close()

        return redirect("/clientes")

    cursor.close()
    conn.close()

    return render_template(
        "novo_cliente.html",
        cliente=cliente
    )

#botao excluir
@clientes.route("/clientes/<int:id>/excluir")
def excluir_cliente(id):

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE clientes
        SET ativo = FALSE
        WHERE id = %s
    """, (id,))

    conn.commit()

    cursor.close()
    conn.close()

    return redirect("/clientes")