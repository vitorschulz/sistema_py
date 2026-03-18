from flask import Blueprint, render_template, request, redirect, flash
from app.config import get_db_connection

shopping = Blueprint("shopping", __name__)

#listagem
@shopping.route("/shopping")
def listar_shopping():
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
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
        ORDER BY shopping.local, shopping.nome
    """)

    shoppings = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("shoppings.html", shoppings=shoppings)


#get pra ir pra pag especifica do shop
@shopping.route("/shopping/<int:id>")
def ver_shopping(id):

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT * FROM shopping
        WHERE id = %s
    """, (id,))
    
    shopping_dados = cursor.fetchone()

    cursor.execute("""
        SELECT * FROM lojas
        WHERE shopping_id = %s
        AND ativo = TRUE
        ORDER BY nome
    """, (id,))

    lojas = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "shopping_detalhe.html",
        shopping=shopping_dados,
        lojas=lojas
    )


#funcao pra criar shopping post form
@shopping.route("/shopping/novo", methods=["GET","POST"])
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