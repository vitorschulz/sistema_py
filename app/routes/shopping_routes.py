from flask import Blueprint, render_template, request, redirect, flash
from app.routes.main_routes import login_required
from app.config import get_db_connection

shopping = Blueprint("shopping", __name__)

#listagem
@shopping.route("/shopping")
@login_required
def listar_shopping():
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    sort = request.args.get("sort")
    order = request.args.get("order")

    if order not in ["asc", "desc"]:
        order = None

    colunas_permitidas = {
        "nome": "shopping.nome",
        "local": "shopping.local",
        "contato": "shopping.contato",
        "endereco": "shopping.endereco"
    }

    sort_col = colunas_permitidas.get(sort)

    if order is None:
        sort_col = None

    query = """
        SELECT 
            shopping.id,
            shopping.nome,
            shopping.local,
            shopping.endereco,
            shopping.contato,
            COUNT(lojas.id) AS total_lojas
        FROM shopping
        LEFT JOIN lojas 
            ON lojas.shopping_id = shopping.id 
            AND lojas.ativo = TRUE
        WHERE shopping.ativo = TRUE
        GROUP BY shopping.id
    """

    if sort_col and order:
        query += f" ORDER BY {sort_col} {order.upper()}"
    else:
        query += " ORDER BY shopping.local ASC, shopping.nome ASC"

    cursor.execute(query)
    shoppings = cursor.fetchall()

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

    return render_template(
        "shoppings.html",
        shoppings=shoppings,
        proxima_ordem_nome=proxima_ordem("nome"),
        proxima_ordem_local=proxima_ordem("local"),
        proxima_ordem_contato=proxima_ordem("contato"),
        proxima_ordem_endereco=proxima_ordem("endereco"),
    )


#get pra ir pra pag especifica do shop
@shopping.route("/shopping/<int:id>")
@login_required
def ver_shopping(id):

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT * FROM shopping
        WHERE id = %s
    """, (id,))
    
    shopping_dados = cursor.fetchone()

    sort = request.args.get("sort")
    order = request.args.get("order")

    if order not in ["asc", "desc"]:
        order = None

    colunas_permitidas = {
        "nome": "nome",
        "contato": "contato",
        "observacoes": "observacoes"
    }

    sort_col = colunas_permitidas.get(sort)

    if order is None:
        sort_col = None

    query = """
        SELECT *
        FROM lojas
        WHERE shopping_id = %s
        AND ativo = TRUE
    """

    if sort_col and order:
        query += f" ORDER BY {sort_col} {order.upper()}"
    else:
        query += " ORDER BY nome ASC"

    cursor.execute(query, (id,))
    lojas = cursor.fetchall()

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

    return render_template(
        "shopping_detalhe.html",
        shopping=shopping_dados,
        lojas=lojas,

        proxima_ordem_nome=proxima_ordem("nome"),
        proxima_ordem_contato=proxima_ordem("contato"),
        proxima_ordem_observacao=proxima_ordem("observacoes"),
    )


#funcao pra criar shopping post form
@shopping.route("/shopping/novo", methods=["GET","POST"])
@login_required
def novo_shopping():

    if request.method == "POST":

        nome = request.form["nome"].strip()
        local = request.form["local"].strip()
        endereco = request.form["endereco"].strip()
        contato = request.form["contato"].strip()
        observacoes = request.form["observacoes"].strip()


        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO shopping
            (nome, local, endereco, contato, observacoes)
            VALUES (%s,%s,%s,%s,%s)
        """, (nome, local, endereco, contato, observacoes))

        conn.commit()

        cursor.close()
        conn.close()

        flash("Shopping criado com sucesso!", "success")

        return redirect("/shopping")

    return render_template("novo_shopping.html")

# editar botao do shopping
@shopping.route("/shopping/<int:id>/editar", methods=["GET","POST"])
@login_required
def editar_shopping(id):

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT * FROM shopping
        WHERE id = %s
    """, (id,))
    shopping_dados = cursor.fetchone()

    if request.method == "POST":

        nome = request.form["nome"].strip()
        local = request.form["local"].strip()
        endereco = request.form["endereco"].strip()
        contato = request.form["contato"].strip()
        observacoes = request.form["observacoes"].strip()

        cursor.execute("""
            UPDATE shopping
            SET nome=%s,
                local=%s,
                endereco=%s,
                contato=%s,
                observacoes=%s
            WHERE id=%s
        """, (nome, local, endereco, contato, observacoes, id))

        conn.commit()

        cursor.close()
        conn.close()

        flash("Shopping atualizado com sucesso!", "success")

        return redirect("/shopping")

    cursor.close()
    conn.close()

    return render_template(
        "novo_shopping.html",
        shopping=shopping_dados
    )

# botao excluir shopping
@shopping.route("/shopping/<int:id>/excluir")
@login_required
def excluir_shopping(id):

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE lojas
        SET shopping_id = NULL
        WHERE shopping_id = %s
    """, (id,))

    cursor.execute("""
        UPDATE shopping
        SET ativo = FALSE
        WHERE id = %s
    """, (id,))

    conn.commit()

    cursor.close()
    conn.close()

    flash("Shopping excluído com sucesso!", "success")

    return redirect("/shopping")