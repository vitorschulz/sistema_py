from flask import Blueprint, render_template, request, redirect
from app.config import get_db_connection

viagens = Blueprint("viagens", __name__)

# listar
@viagens.route("/viagens")
def listar_viagens():
    return render_template("viagens.html")


# nova viagem
@viagens.route("/viagens/nova", methods=["GET","POST"])
def nova_viagem():

    if request.method == "POST":

        nome = request.form["nome"].strip()
        data_viagem = request.form["data_viagem"]
        observacoes = request.form["observacoes"].strip()

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO viagens
            (nome, data_viagem, observacoes)
            VALUES (%s,%s,%s)
        """, (nome, data_viagem, observacoes))

        conn.commit()

        cursor.close()
        conn.close()

        return redirect("/viagens")

    return render_template("nova_viagem.html")