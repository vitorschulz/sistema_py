from flask import Blueprint, render_template, request, redirect
from app.config import get_db_connection

shopping = Blueprint("shopping", __name__)

@shopping.route("/shopping")
def listar_shopping():

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT * FROM shopping
        WHERE ativo = TRUE
        ORDER BY nome
    """)

    shoppings = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("shoppings.html", shoppings=shoppings)


@shopping.route("/shopping/novo", methods=["GET","POST"])
def novo_shopping():

    if request.method == "POST":

        nome = request.form["nome"].strip()
        cidade = request.form["cidade"].strip()
        endereco = request.form["endereco"].strip()
        observacoes = request.form["observacoes"].strip()


        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO shopping
            (nome, cidade, endereco, observacoes)
            VALUES (%s,%s,%s,%s)
        """, (nome, cidade, endereco, observacoes))

        conn.commit()

        cursor.close()
        conn.close()

        return redirect("/shopping")

    return render_template("novo_shopping.html")