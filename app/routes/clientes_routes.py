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

    sort = request.args.get("sort")
    order = request.args.get("order")

    colunas_permitidas = ["nome", "cpf_cnpj", "telefone", "endereco"]

    if sort not in colunas_permitidas:
        sort = None

    if order not in ["asc", "desc"]:
        order = None

    query = """
        SELECT * FROM clientes
        WHERE ativo = TRUE
    """

    if sort and order:
        query += f" ORDER BY {sort} {order.upper()}"
    elif sort and order is None:
        query += " ORDER BY nome ASC"
    else:
        query += " ORDER BY nome ASC"

    cursor.execute(query)
    clientes_lista = cursor.fetchall()

    def proxima_ordem(coluna):
        if sort != coluna:
            return "asc"   
        elif order == "asc":
            return "desc"       
        elif order == "desc":
            return None        
        return "asc"
    
    cursor.close()
    conn.close()

    return render_template("clientes.html",
    clientes=clientes_lista,
    proxima_ordem_nome=proxima_ordem("nome"),
    proxima_ordem_cpf=proxima_ordem("cpf_cnpj"),
    proxima_ordem_telefone=proxima_ordem("telefone"),
    proxima_ordem_endereco=proxima_ordem("endereco"),)


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

        next_url = request.form.get("next") or request.args.get("next") or "/clientes"
        return redirect(next_url)

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

    sort = request.args.get("sort")
    order = request.args.get("order")

    return redirect(f"/clientes?sort={sort}&order={order}")