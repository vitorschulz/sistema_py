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

    query += """
        GROUP BY v.id
        ORDER BY v.data_viagem ASC
    """

    cursor.execute(query, tuple(params))
    movimentacoes = cursor.fetchall()

    receita_total = sum(item['receita'] or 0 for item in movimentacoes)
    custo_total = sum(item['custo'] or 0 for item in movimentacoes)
    saldo_total = sum(item['lucro'] or 0 for item in movimentacoes)

    cursor.execute("""
        SELECT *
        FROM cheques
        WHERE ativo = 1
        ORDER BY criado_em DESC
    """)

    cheques = cursor.fetchall()


    total_compensado = sum(c['valor'] for c in cheques if c['status'] == 'COMPENSADO')
    total_pendente = sum(c['valor'] for c in cheques if c['status'] == 'PENDENTE')

    labels = []
    receitas = []
    custos = []
    lucros = []


    for item in movimentacoes:
        labels.append(item['data'].strftime('%d/%m') if item['data'] else '')
        receitas.append(float(item['receita'] or 0))
        custos.append(float(item['custo'] or 0))
        lucros.append(float(item['lucro'] or 0))
        print(item['custo'], item['receita'], item['lucro'])

    cursor.close()
    conn.close()

    return render_template(
        "financeiro.html",
        movimentacoes=movimentacoes,
        cheques=cheques,
        total_compensado=total_compensado,
        total_pendente=total_pendente,
        receita_total=receita_total,
        custo_total=custo_total,
        saldo_total=saldo_total,
        labels=labels,
        receitas=receitas,
        custos=custos,
        lucros=lucros
        )
