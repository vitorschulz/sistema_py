from flask import Blueprint, render_template
from app.config import get_db_connection
from datetime import date

main = Blueprint("main", __name__)

@main.route("/")
def dashboard():

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    

    hoje = date.today()


    cursor.execute("""
        SELECT data_viagem 
        FROM viagens
        WHERE ativo = 1
    """)
    viagens = cursor.fetchall()

    datas_viagens = [v["data_viagem"].strftime("%Y-%m-%d") for v in viagens]

    cursor.execute("""
    SELECT 
        SUM(CASE 
            WHEN UPPER(vf.tipo) = 'GANHO' THEN COALESCE(vf.valor, 0)
            WHEN UPPER(vf.tipo) = 'CUSTO' THEN -COALESCE(vf.valor, 0)
            ELSE 0 
        END) AS saldo_total
    FROM viagem_financeiro vf
    JOIN viagens v ON v.id = vf.viagem_id
    WHERE v.ativo = 1
    """)

    resultado = cursor.fetchone()
    saldo_total = resultado['saldo_total'] or 0

    cursor.execute("""
        SELECT id, data_viagem, local, status
        FROM viagens
        WHERE data_viagem >= %s AND ativo = 1
        ORDER BY data_viagem ASC
        LIMIT 5
    """, (hoje,))
    proximas_viagens = cursor.fetchall()



    cursor.execute("SELECT COUNT(*) as total FROM clientes WHERE ativo = 1")
    total_clientes = cursor.fetchone()["total"]


    cursor.execute("""
        SELECT COUNT(*) as total 
        FROM viagens 
        WHERE data_viagem >= %s AND ativo = 1
    """, (hoje,))
    total_viagens = cursor.fetchone()["total"]



    cursor.execute("SELECT COUNT(*) as total FROM shopping WHERE ativo = 1")
    total_shoppings = cursor.fetchone()["total"]



    cursor.execute("SELECT COUNT(*) as total FROM lojas WHERE ativo = 1")
    total_lojas = cursor.fetchone()["total"]

    cursor.execute("""
    SELECT id, codigo, nome_destino, valor, data_vencimento
    FROM cheques
    WHERE status = 'PENDENTE' AND ativo = 1
    ORDER BY data_vencimento ASC
    LIMIT 5
    """)
    cheques_pendentes = cursor.fetchall()


    cursor.execute("""
    SELECT COUNT(*) as total
    FROM cheques
    WHERE status = 'PENDENTE' AND ativo = 1
    """)
    total_cheques_pendentes = cursor.fetchone()["total"]

    hoje = date.today()

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
        total_lojas=total_lojas,
        cheques_pendentes=cheques_pendentes,
        total_cheques_pendentes=total_cheques_pendentes,
        hoje=hoje,
        saldo_total=saldo_total
    )