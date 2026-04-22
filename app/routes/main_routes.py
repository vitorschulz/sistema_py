from flask import request, Blueprint, render_template, redirect, session, flash
from app.config import get_db_connection
from datetime import date
from functools import wraps
from werkzeug.security import check_password_hash

main = Blueprint("main", __name__)

def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if "user_id" not in session:
            return redirect("/login")
        return f(*args, **kwargs)
    return wrapper


#autorizacao
@main.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        senha = request.form["senha"]

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM usuarios WHERE username = %s", (username,))
        user = cursor.fetchone()

        cursor.close()
        conn.close()

        if user and check_password_hash(user["password_hash"], senha):
            session["user_id"] = user["id"]
            return redirect("/")

        flash("Usuário ou senha inválidos!", "error")
        return redirect("/login")

    return render_template("login.html")

#dashboard e seus dados
@main.route("/")
@login_required
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

    datas_viagens = [
        v["data_viagem"].strftime("%Y-%m-%d")
        for v in viagens if v["data_viagem"]
    ]

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
    WHERE ativo = 1
    AND status NOT IN ('Finalizada', 'Cancelada')
    AND (
        (data_viagem >= %s AND status = 'Planejada')
        OR status = 'Em andamento'
    )
    ORDER BY 
        CASE 
            WHEN status = 'Em andamento' THEN 0
            ELSE 1
        END,
        data_viagem ASC
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

    sort = request.args.get("sort")
    order = request.args.get("order")

    colunas_permitidas = {
        "codigo": "codigo",
        "nome_destino": "nome_destino",
        "data_vencimento": "data_vencimento",
        "valor": "valor"
    }

    if order not in ["asc", "desc"]:
        order = None

    sort_col = colunas_permitidas.get(sort)

    if order is None:
        sort_col = None

    query_cheques = """
    SELECT id, codigo, nome_destino, valor, data_vencimento
    FROM cheques
    WHERE status = 'PENDENTE' AND ativo = 1
    """

    if sort_col and order:
        query_cheques += f" ORDER BY {sort_col} {order.upper()}"
    else:
        query_cheques += " ORDER BY data_vencimento ASC"

    query_cheques += " LIMIT 5"

    cursor.execute(query_cheques)
    cheques_pendentes = cursor.fetchall()

    cursor.execute("""
    SELECT COUNT(*) as total
    FROM cheques
    WHERE status = 'PENDENTE' AND ativo = 1
    """)
    total_cheques_pendentes = cursor.fetchone()["total"]

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
        saldo_total=saldo_total,

        # ordenação
        proxima_ordem_codigo=proxima_ordem("codigo"),
        proxima_ordem_destino=proxima_ordem("nome_destino"),
        proxima_ordem_vencimento=proxima_ordem("data_vencimento"),
        proxima_ordem_valor=proxima_ordem("valor"),
    )