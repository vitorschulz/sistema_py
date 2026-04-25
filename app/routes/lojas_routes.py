from flask import Blueprint, render_template, request, redirect, flash
from app.routes.main_routes import login_required
from app.config import get_db_connection

lojas = Blueprint("lojas", __name__)

#listagem lojas tela normal
@lojas.route("/lojas")
@login_required
def listar_lojas():

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    sort = request.args.get("sort")
    order = request.args.get("order")

    if order not in ["asc", "desc"]:
        order = None

    colunas_permitidas = {
        "nome": "lojas.nome",
        "shopping_nome": "shopping.nome",
        "contato": "lojas.contato",
        "observacoes": "lojas.observacoes"
    }

    sort_col = colunas_permitidas.get(sort)

    if order is None:
        sort_col = None

    query = """
        SELECT 
            lojas.id,
            lojas.nome,
            lojas.observacoes,
            lojas.contato,
            shopping.nome AS shopping_nome
        FROM lojas
        LEFT JOIN shopping 
            ON lojas.shopping_id = shopping.id
            AND shopping.ativo = TRUE
        WHERE lojas.ativo = TRUE
    """

    if sort_col and order:
        query += f" ORDER BY {sort_col} {order.upper()}"
    else:
        query += " ORDER BY shopping.nome ASC"

    cursor.execute(query)
    lojas_lista = cursor.fetchall()

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
        "lojas.html",
        lojas=lojas_lista,
        proxima_ordem_nome=proxima_ordem("nome"),
        proxima_ordem_shopping=proxima_ordem("shopping_nome"),
        proxima_ordem_contato=proxima_ordem("contato"),
        proxima_ordem_observacao=proxima_ordem("observacoes"),
    )

#dropdown form e post form
@lojas.route("/lojas/novo", methods=["GET","POST"])
@login_required
def nova_loja():

    shopping_preselecionado = request.args.get("shopping")
    shopping_nome = None

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT id, nome
        FROM shopping
        WHERE ativo = TRUE
        ORDER BY LOWER(nome) ASC
    """)

    shoppings = cursor.fetchall()

    if shopping_preselecionado:

        cursor.execute("""
            SELECT nome
            FROM shopping
            WHERE id = %s
        """, (shopping_preselecionado,))

        resultado = cursor.fetchone()

        if resultado:
            shopping_nome = resultado["nome"]

    if request.method == "POST":

        nome = request.form["nome"]
        shopping_id = request.form["shopping_id"]
        observacoes = request.form["observacoes"]
        contato = request.form["contato"]
    
        cursor.execute("""
        SELECT id FROM lojas
        WHERE nome=%s AND shopping_id=%s AND ativo = TRUE
        """, (nome, shopping_id))

        existe = cursor.fetchone()

        if not existe:

            cursor.execute("""
                INSERT INTO lojas
                (nome, contato, shopping_id, observacoes)
                VALUES (%s,%s,%s,%s)
            """, (nome, contato, shopping_id, observacoes))

            conn.commit()

            flash("Loja criada com sucesso!", "success")
        else:
            flash("Essa loja já existe nesse shopping!", "error")

        cursor.close()
        conn.close()

        if shopping_preselecionado:
            return redirect(f"/shopping/{shopping_preselecionado}")

        return redirect("/lojas")

    cursor.close()
    conn.close()
    

    return render_template(
        "nova_loja.html",
        shoppings=shoppings,
        shopping_preselecionado=shopping_preselecionado,
        shopping_nome=shopping_nome
    )

#editar botao
@lojas.route("/lojas/<int:id>/editar", methods=["GET","POST"])
@login_required
def editar_loja(id):

    shopping_origem = request.args.get("shopping")

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)


    cursor.execute("""
        SELECT id, nome
        FROM shopping
        WHERE ativo = TRUE
        ORDER BY nome
    """)
    shoppings = cursor.fetchall()


    cursor.execute("""
        SELECT * FROM lojas
        WHERE id = %s
    """, (id,))
    loja = cursor.fetchone()

    if request.method == "POST":

        nome = request.form["nome"]
        shopping_id = request.form["shopping_id"]
        observacoes = request.form["observacoes"]
        contato = request.form["contato"]

        cursor.execute("""
            UPDATE lojas
            SET nome=%s, contato=%s, shopping_id=%s, observacoes=%s
            WHERE id=%s
        """, (nome, contato, shopping_id, observacoes, id))

        conn.commit()

        cursor.close()
        conn.close()

        flash("Loja atualizada com sucesso!", "success")

        next_url = request.form.get("next") or request.args.get("next")

        if next_url:
            return redirect(next_url)

        if shopping_origem:
            return redirect(f"/shopping/{shopping_origem}")

        return redirect("/lojas")

    cursor.close()
    conn.close()

    return render_template(
        "nova_loja.html",
        loja=loja,
        shoppings=shoppings,
        shopping_preselecionado=shopping_origem
    )

#excluir pelo botao
@lojas.route("/lojas/<int:id>/excluir")
@login_required
def excluir_loja(id):

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE lojas
        SET ativo = FALSE
        WHERE id = %s
        """, (id,))

    conn.commit()

    cursor.close()
    conn.close()

    flash("Loja excluída com sucesso!", "success")

    next_url = request.args.get("next")

    if next_url:
        return redirect(next_url)

    shopping_origem = request.args.get("shopping")

    if shopping_origem:
        return redirect(f"/shopping/{shopping_origem}")

    return redirect("/lojas")

#get pra ir pros detalhes
@lojas.route("/lojas/<int:id>")
@login_required
def ver_loja(id):

    shopping_id = request.args.get("shopping")

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
         SELECT 
            lojas.id,
            lojas.nome,
            lojas.observacoes,
            lojas.contato,
            shopping.nome AS shopping_nome
        FROM lojas
        LEFT JOIN shopping ON lojas.shopping_id = shopping.id
        AND shopping.ativo = TRUE
        WHERE lojas.id = %s
    """, (id,))

    loja = cursor.fetchone()

    cursor.close()
    conn.close()

    return render_template(
        "loja_detalhe.html",
        loja=loja,
        shopping_id=shopping_id
    )