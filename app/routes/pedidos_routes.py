from flask import Blueprint, render_template, request, redirect
from app.config import get_db_connection

pedidos = Blueprint("pedidos", __name__)

#click do pedido
@pedidos.route("/pedidos/<int:id>")
def detalhe_pedido(id):

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT 
            pedidos.*,
            clientes.nome AS cliente_nome,
            lojas.nome AS loja_nome,
            lojas.id AS loja_id,
            shopping.nome AS shopping_nome,
            shopping.id AS shopping_id,
            viagens.nome AS viagem_nome
        FROM pedidos
        JOIN clientes ON pedidos.cliente_id = clientes.id
        JOIN lojas ON pedidos.loja_id = lojas.id
        JOIN shopping ON lojas.shopping_id = shopping.id AND shopping.ativo = TRUE
        JOIN viagens ON pedidos.viagem_id = viagens.id
        WHERE pedidos.id = %s
    """, (id,))

    pedido = cursor.fetchone()

    cursor.execute("""
        SELECT COUNT(*) AS numero
        FROM pedidos
        WHERE cliente_id = %s
        AND viagem_id = %s
        AND id <= %s
    """, (pedido["cliente_id"], pedido["viagem_id"], pedido["id"]))

    numero_cliente = cursor.fetchone()["numero"]

    cursor.close()
    conn.close()

    return render_template(
        "pedido_detalhe.html",
        numero_cliente=numero_cliente,
        pedido=pedido
    )

