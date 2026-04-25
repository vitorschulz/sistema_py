from flask import Blueprint, render_template, request, redirect, flash
from app.config import get_db_connection
from app.routes.main_routes import login_required

cheques = Blueprint('cheques', __name__, url_prefix='/cheques')

#listagem cheques
@cheques.route('', strict_slashes=False)
@login_required
def listar_cheques():

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    sort = request.args.get("sort")
    order = request.args.get("order")

    colunas_permitidas = [
        "codigo",
        "nome_destino",
        "data_vencimento",
        "valor",
        "status"
    ]

    if sort not in colunas_permitidas:
        sort = None

    if order not in ["asc", "desc"]:
        order = None

    if order is None:
        sort = None

    query = """
        SELECT *
        FROM cheques
        WHERE ativo = TRUE
    """

    if sort and order:
        query += f" ORDER BY {sort} {order.upper()}"
    else:
        query += " ORDER BY criado_em DESC"

    cursor.execute(query)
    lista = cursor.fetchall()

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
        "cheques.html",
        cheques=lista,
        proxima_ordem_codigo=proxima_ordem("codigo"),
        proxima_ordem_destino=proxima_ordem("nome_destino"),
        proxima_ordem_vencimento=proxima_ordem("data_vencimento"),
        proxima_ordem_valor=proxima_ordem("valor"),
        proxima_ordem_status=proxima_ordem("status"),
    )


#form cheque
@cheques.route('/novo', methods=['GET', 'POST'])
@login_required
def novo_cheque():

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':

        cursor.execute("""
            INSERT INTO cheques
            (codigo, valor, nome_destino, data_vencimento, status, ativo)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            request.form['codigo'],
            request.form['valor'],
            request.form['nome_destino'],
            request.form.get('data_vencimento'),
            'PENDENTE',
            1
        ))

        conn.commit()


        flash('Cheque criado com sucesso!', 'success')

        cursor.close()
        conn.close()

        sort = request.args.get("sort")
        order = request.args.get("order")

        return redirect(f'/cheques?sort={sort}&order={order}')


    cursor.execute("""
        SELECT id, nome
        FROM clientes
        WHERE ativo = TRUE
        ORDER BY nome
    """)

    clientes = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("novo_cheque.html", clientes=clientes)


#botao compensar
@cheques.route('/<int:id>/compensar')
@login_required
def compensar_cheque(id):

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE cheques
        SET status = 'COMPENSADO'
        WHERE id = %s AND ativo = 1
    """, (id,))

    conn.commit()
    cursor.close()
    conn.close()

    flash('Cheque compensado com sucesso!', 'success')
    sort = request.args.get("sort")
    order = request.args.get("order")

    return redirect(f'/cheques?sort={sort}&order={order}')

#botao sustar no cheque
@cheques.route('/<int:id>/devolver')
@login_required
def devolver_cheque(id):

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE cheques
        SET status = 'SUSTADO'
        WHERE id = %s AND ativo = 1
    """, (id,))


    conn.commit()

    flash('Cheque sustado com sucesso!', 'success')
    cursor.close()
    conn.close()

    sort = request.args.get("sort")
    order = request.args.get("order")

    return redirect(f'/cheques?sort={sort}&order={order}')

#apagar botao
@cheques.route('/<int:id>/excluir')
@login_required
def excluir_cheque(id):

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE cheques
        SET ativo = 0
        WHERE id = %s
    """, (id,))

    conn.commit()

    flash('Cheque removido!', 'success')
    cursor.close()
    conn.close()

    sort = request.args.get("sort")
    order = request.args.get("order")

    return redirect(f'/cheques?sort={sort}&order={order}')


#editrar
@cheques.route('/<int:id>/editar', methods=['GET', 'POST'])
@login_required
def editar_cheque(id):

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        cursor.execute("""
            UPDATE cheques
            SET codigo = %s,
                valor = %s,
                nome_destino = %s,
                data_vencimento = %s
            WHERE id = %s
        """, (
            request.form['codigo'],
            request.form['valor'],
            request.form['nome_destino'],
            request.form.get('data_vencimento'),
            id
        ))

        conn.commit()

        flash('Cheque atualizado com sucesso!', 'success')
        
        cursor.close()
        conn.close()

        next_url = request.form.get("next") or request.args.get("next") or "/cheques"
        return redirect(next_url)

    cursor.execute("SELECT * FROM cheques WHERE id = %s", (id,))
    cheque = cursor.fetchone()

    cursor.close()
    conn.close()

    return render_template("novo_cheque.html", cheque=cheque)

