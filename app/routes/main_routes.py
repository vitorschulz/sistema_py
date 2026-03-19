from flask import Blueprint, render_template
from app.config import get_db_connection
from datetime import date

main = Blueprint("main", __name__)

@main.route("/")
def dashboard():

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    

    hoje = date.today()

    # 📅 DATAS PRA AGENDA
    cursor.execute("""
        SELECT data_viagem 
        FROM viagens
        WHERE ativo = 1
    """)
    viagens = cursor.fetchall()

    datas_viagens = [v["data_viagem"].strftime("%Y-%m-%d") for v in viagens]


    # 🚗 PRÓXIMAS VIAGENS (limita tipo 5)
    cursor.execute("""
        SELECT id, data_viagem, local, status
        FROM viagens
        WHERE data_viagem >= %s AND ativo = 1
        ORDER BY data_viagem ASC
        LIMIT 5
    """, (hoje,))
    proximas_viagens = cursor.fetchall()


    # 👥 CLIENTES
    cursor.execute("SELECT COUNT(*) as total FROM clientes WHERE ativo = 1")
    total_clientes = cursor.fetchone()["total"]


    # ✈️ VIAGENS FUTURAS
    cursor.execute("""
        SELECT COUNT(*) as total 
        FROM viagens 
        WHERE data_viagem >= %s AND ativo = 1
    """, (hoje,))
    total_viagens = cursor.fetchone()["total"]


    # 🏬 SHOPPINGS
    cursor.execute("SELECT COUNT(*) as total FROM shopping WHERE ativo = 1")
    total_shoppings = cursor.fetchone()["total"]


    # 🏪 LOJAS
    cursor.execute("SELECT COUNT(*) as total FROM lojas WHERE ativo = 1")
    total_lojas = cursor.fetchone()["total"]


    cursor.close()
    conn.close()

    datas_viagens = [
        v["data_viagem"].strftime("%Y-%m-%d")
        for v in viagens if v["data_viagem"]
    ]

    return render_template(
        "index.html",
        datas_viagens=datas_viagens,
        proximas_viagens=proximas_viagens,
        total_clientes=total_clientes,
        total_viagens=total_viagens,
        total_shoppings=total_shoppings,
        total_lojas=total_lojas
    )