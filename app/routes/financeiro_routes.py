from flask import Blueprint, render_template, request, redirect, flash
from app.routes.main_routes import login_required
from app.config import get_db_connection

financeiro = Blueprint("financeiro", __name__)

#listagem do financeiro e tb pegagem de dados necessarios e totais
@financeiro.route('/financeiro')
@login_required
def pagina_financeiro():

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    data_inicio = request.args.get("data_inicio")
    data_fim = request.args.get("data_fim")

    sort = request.args.get("sort")
    order = request.args.get("order")

    if order not in ["asc", "desc"]:
        order = None

    colunas_mov = {
        "mov_data": "v.data_viagem",
        "mov_local": "v.local",
        "mov_receita": "receita",
        "mov_custo": "custo",
        "mov_lucro": "lucro"
    }

    colunas_cheques = {
        "chq_codigo": "codigo",
        "chq_nome_destino": "nome_destino",
        "chq_valor": "valor",
        "chq_status": "status"
    }

    sort_mov = colunas_mov.get(sort)
    sort_cheque = colunas_cheques.get(sort)

    if order is None:
        sort_mov = None
        sort_cheque = None

    query = """
    SELECT 
        v.id AS id,
        v.data_viagem AS data,
        v.local,

        SUM(CASE 
            WHEN UPPER(vf.tipo) = 'GANHO' THEN COALESCE(vf.valor, 0)
            ELSE 0 
        END) AS receita,

        SUM(CASE 
            WHEN UPPER(vf.tipo) = 'CUSTO' THEN COALESCE(vf.valor, 0)
            ELSE 0 
        END) AS custo,

        SUM(CASE 
            WHEN UPPER(vf.tipo) = 'GANHO' THEN COALESCE(vf.valor, 0)
            WHEN UPPER(vf.tipo) = 'CUSTO' THEN -COALESCE(vf.valor, 0)
            ELSE 0 
        END) AS lucro

        FROM viagens v

        LEFT JOIN viagem_financeiro vf
            ON vf.viagem_id = v.id

        WHERE v.ativo = 1
    """

    params = []

    if data_inicio:
        query += " AND v.data_viagem >= %s"
        params.append(data_inicio)

    if data_fim:
        query += " AND v.data_viagem <= %s"
        params.append(data_fim)

    query += " GROUP BY v.id"

    if sort_mov and order:
        query += f" ORDER BY {sort_mov} {order.upper()}"
    else:
        query += " ORDER BY v.data_viagem ASC"

    cursor.execute(query, tuple(params))
    movimentacoes = cursor.fetchall()

    query_cheques = """
        SELECT *
        FROM cheques
        WHERE ativo = 1
    """

    if sort_cheque and order:
        query_cheques += f" ORDER BY {sort_cheque} {order.upper()}"
    else:
        query_cheques += " ORDER BY criado_em DESC"

    cursor.execute(query_cheques)
    cheques = cursor.fetchall()

    receita_total = sum(item['receita'] or 0 for item in movimentacoes)
    custo_total = sum(item['custo'] or 0 for item in movimentacoes)
    saldo_total = sum(item['lucro'] or 0 for item in movimentacoes)

    total_compensado = sum(c['valor'] for c in cheques if c['status'] == 'COMPENSADO')
    total_pendente = sum(c['valor'] for c in cheques if c['status'] == 'PENDENTE')

    labels, receitas, custos, lucros = [], [], [], []

    for item in movimentacoes:
        labels.append(item['data'].strftime('%d/%m') if item['data'] else '')
        receitas.append(float(item['receita'] or 0))
        custos.append(float(item['custo'] or 0))
        lucros.append(float(item['lucro'] or 0))

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
        "financeiro.html",
        movimentacoes=movimentacoes,
        cheques=cheques,

        proxima_ordem_data=proxima_ordem("mov_data"),
        proxima_ordem_local=proxima_ordem("mov_local"),
        proxima_ordem_receita=proxima_ordem("mov_receita"),
        proxima_ordem_custo=proxima_ordem("mov_custo"),
        proxima_ordem_lucro=proxima_ordem("mov_lucro"),

        proxima_ordem_codigo=proxima_ordem("chq_codigo"),
        proxima_ordem_destino=proxima_ordem("chq_nome_destino"),
        proxima_ordem_valor=proxima_ordem("chq_valor"),
        proxima_ordem_status=proxima_ordem("chq_status"),

        receita_total=receita_total,
        custo_total=custo_total,
        saldo_total=saldo_total,
        total_compensado=total_compensado,
        total_pendente=total_pendente,

        labels=labels,
        receitas=receitas,
        custos=custos,
        lucros=lucros
    )
