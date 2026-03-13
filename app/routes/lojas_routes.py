from flask import Blueprint, render_template, request, redirect
from app.config import get_db_connection

lojas = Blueprint("lojas", __name__)

#listagem lojas tela normal
@lojas.route("/lojas")
def listar_lojas():

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT 
            lojas.id,
            lojas.nome,
            lojas.observacoes,
            shopping.nome AS shopping_nome
        FROM lojas
        LEFT JOIN shopping 
            ON lojas.shopping_id = shopping.id
        WHERE lojas.ativo = TRUE
        ORDER BY lojas.nome
    """)

    lojas_lista = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "lojas.html",
        lojas=lojas_lista
    )

#dropdown form e post form
@lojas.route("/lojas/novo", methods=["GET","POST"])
def nova_loja():

    shopping_preselecionado = request.args.get("shopping")
    shopping_nome = None

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT id, nome
        FROM shopping
        WHERE ativo = TRUE
        ORDER BY nome
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
    
        cursor.execute("""
        SELECT id FROM lojas
        WHERE nome=%s AND shopping_id=%s
        """, (nome, shopping_id))

        existe = cursor.fetchone()

        if not existe:

            cursor.execute("""
                INSERT INTO lojas
                (nome, shopping_id, observacoes)
                VALUES (%s,%s,%s)
            """, (nome, shopping_id, observacoes))

            conn.commit()

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

        cursor.execute("""
            UPDATE lojas
            SET nome=%s, shopping_id=%s, observacoes=%s
            WHERE id=%s
        """, (nome, shopping_id, observacoes, id))

        conn.commit()

        cursor.close()
        conn.close()

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

    shopping_origem = request.args.get("shopping")

    if shopping_origem:
        return redirect(f"/shopping/{shopping_origem}")

    return redirect("/lojas")

#get pra ir pros detalhes
@lojas.route("/lojas/<int:id>")
def ver_loja(id):

    shopping_id = request.args.get("shopping")

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
         SELECT 
            lojas.id,
            lojas.nome,
            lojas.observacoes,
            shopping.nome AS shopping_nome
        FROM lojas
        LEFT JOIN shopping ON lojas.shopping_id = shopping.id
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