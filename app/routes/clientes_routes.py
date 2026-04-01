from flask import Blueprint, render_template, request, redirect, flash
from app.routes.main_routes import login_required
from app.config import get_db_connection

clientes = Blueprint("clientes", __name__)

#get do id pra ir pra telas de detalhe
@clientes.route("/clientes/<int:id>")
@login_required
def ver_cliente(id):

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM clientes WHERE id = %s", (id,))
    cliente = cursor.fetchone()
    
    cursor.execute("""
        SELECT 
            v.id,
            v.local,
            v.data_viagem,
            v.status,
            COUNT(p.id) AS total_tarefas
        FROM viagens v

        LEFT JOIN pedidos p 
            ON p.viagem_id = v.id
            AND p.cliente_id = %s

        LEFT JOIN viagem_clientes vc
            ON vc.viagem_id = v.id
            AND vc.cliente_id = %s

        WHERE vc.cliente_id IS NOT NULL
        OR p.cliente_id IS NOT NULL

        GROUP BY v.id, v.local, v.data_viagem, v.status
        ORDER BY v.data_viagem DESC
    """, (id, id))

    viagens = cursor.fetchall()

    return render_template("cliente_detalhe.html", cliente=cliente, viagens=viagens)

#listagem de cliente
@clientes.route("/clientes")
@login_required
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
@login_required
def novo_cliente():

    if request.method == "POST":

        nome = request.form["nome"]
        cpf_cnpj = request.form["cpf_cnpj"]
        telefone = request.form["telefone"]
        endereco = request.form["endereco"]
        observacoes = request.form["observacoes"]

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO clientes
            (nome, cpf_cnpj, telefone, endereco, observacoes)
            VALUES (%s,%s,%s,%s,%s)
        """, (nome, cpf_cnpj, telefone, endereco, observacoes))

        conn.commit()

        cursor.close()
        conn.close()

        flash("Cliente criado com sucesso!", "success")

        return redirect("/clientes")

    return render_template("novo_cliente.html")

#botao editar
@clientes.route("/clientes/<int:id>/editar", methods=["GET", "POST"])
@login_required
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
        endereco = request.form["endereco"]
        observacoes = request.form["observacoes"]

        cursor.execute("""
            UPDATE clientes
            SET nome=%s, cpf_cnpj=%s, telefone=%s, endereco=%s, observacoes=%s
            WHERE id=%s
        """, (nome, cpf_cnpj, telefone, endereco, observacoes, id))

        conn.commit()

        cursor.close()
        conn.close()

        flash("Cliente atualizado com sucesso!", "success")

        return redirect("/clientes")

    cursor.close()
    conn.close()

    return render_template(
        "novo_cliente.html",
        cliente=cliente
    )

#botao excluir
@clientes.route("/clientes/<int:id>/excluir")
@login_required
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

    flash("Cliente excluído com sucesso!", "success")

    return redirect("/clientes")