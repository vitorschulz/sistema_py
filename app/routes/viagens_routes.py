from flask import Blueprint, render_template, request, redirect, jsonify
from app.config import get_db_connection

viagens = Blueprint("viagens", __name__)

# listar
@viagens.route("/viagens")
def listar_viagens():

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT *
        FROM viagens
        WHERE ativo = 1
        ORDER BY data_viagem DESC
    """)

    viagens = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("viagens.html", viagens=viagens)


# nova viagem
@viagens.route("/viagens/nova", methods=["GET","POST"])
def nova_viagem():

    if request.method == "POST":

        local = request.form["local"]
        data_viagem = request.form["data_viagem"]
        observacoes = request.form["observacoes"].strip()

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO viagens
            (local, data_viagem, observacoes, status)
            VALUES (%s,%s,%s,%s)
        """, (local, data_viagem, observacoes, "Planejada"))

        conn.commit()

        cursor.close()
        conn.close()

        return redirect("/viagens")

    return render_template("nova_viagem.html")

# detalhes da viagem
@viagens.route("/viagens/<int:id>")
def detalhe_viagem(id):

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)


    cursor.execute("""
        SELECT *
        FROM viagens
        WHERE id = %s
    """, (id,))

    viagem = cursor.fetchone()


    cursor.execute("""
        SELECT 
            pedidos.id,
            pedidos.ordem,
            pedidos.tipo,
            clientes.nome AS cliente_nome,
            lojas.nome AS loja_nome,
            shopping.nome AS shopping_nome

        FROM pedidos

        JOIN clientes 
            ON pedidos.cliente_id = clientes.id

        JOIN lojas 
            ON pedidos.loja_id = lojas.id

        JOIN shopping 
            ON lojas.shopping_id = shopping.id AND shopping.ativo = TRUE

        WHERE pedidos.viagem_id = %s

        ORDER BY pedidos.ordem ASC
    """, (id,))

    pedidos = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "viagem_detalhe.html",
        viagem=viagem,
        pedidos=pedidos
    )

#registrar pedido na viagem
@viagens.route("/viagens/<int:id>/novo_pedido", methods=["GET","POST"])
def novo_pedido(id):

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == "POST":

        loja_id = request.form["loja_id"]
        cliente_id = request.form["cliente_id"]
        tipo = request.form["tipo"]
        observacoes = request.form.get("observacoes","").strip()

        cursor.execute("""
            SELECT COALESCE(MAX(ordem),0)+1 AS nova_ordem
            FROM pedidos
            WHERE viagem_id = %s
        """,(id,))

        ordem = cursor.fetchone()["nova_ordem"]

        cursor.execute("""
            INSERT INTO pedidos
            (viagem_id, loja_id, cliente_id, tipo, observacoes, ordem)
            VALUES (%s,%s,%s,%s,%s,%s)
        """,(id, loja_id, cliente_id, tipo, observacoes, ordem))

        conn.commit()

        cursor.close()
        conn.close()

        return redirect(f"/viagens/{id}")

    cursor.execute("SELECT id,nome FROM shopping WHERE ativo=1")
    shoppings = cursor.fetchall()

    cursor.execute("SELECT id,nome,shopping_id FROM lojas WHERE ativo=1")
    lojas = cursor.fetchall()

    cursor.execute("SELECT id,nome FROM clientes WHERE ativo=1")
    clientes = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "novo_pedido.html",
        viagem_id=id,
        shoppings=shoppings,
        lojas=lojas,
        clientes=clientes
    )

#status viagem
@viagens.route("/viagens/<int:id>/status", methods=["POST"])
def atualizar_status_viagem(id):

    data = request.get_json()
    status = data["status"]

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE viagens
        SET status = %s
        WHERE id = %s
    """, (status, id))

    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({"success": True})

#editar viagem
@viagens.route("/viagens/<int:id>/editar", methods=["GET","POST"])
def editar_viagem(id):

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == "POST":

        local = request.form["local"]
        data_viagem = request.form["data_viagem"]
        observacoes = request.form["observacoes"].strip()

        cursor.execute("""
            UPDATE viagens
            SET local=%s, data_viagem=%s, observacoes=%s
            WHERE id=%s
        """,(local,data_viagem,observacoes,id))

        conn.commit()

        cursor.close()
        conn.close()

        return redirect("/viagens")


    cursor.execute("""
        SELECT *
        FROM viagens
        WHERE id=%s
    """,(id,))

    viagem = cursor.fetchone()

    cursor.close()
    conn.close()

    return render_template("nova_viagem.html", viagem=viagem)

#excluir viagem
@viagens.route("/viagens/<int:id>/excluir")
def excluir_viagem(id):

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE viagens
        SET ativo = 0
        WHERE id = %s
    """,(id,))

    conn.commit()

    cursor.close()
    conn.close()

    return redirect("/viagens")


#seta p cima
@viagens.route("/pedidos/<int:id>/subir")
def subir_pedido(id):

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT id, viagem_id, ordem
        FROM pedidos
        WHERE id = %s
    """,(id,))
    pedido = cursor.fetchone()

    cursor.execute("""
        SELECT id, ordem
        FROM pedidos
        WHERE viagem_id = %s AND ordem < %s
        ORDER BY ordem DESC
        LIMIT 1
    """,(pedido["viagem_id"], pedido["ordem"]))

    anterior = cursor.fetchone()

    if anterior:

        cursor.execute(
            "UPDATE pedidos SET ordem=%s WHERE id=%s",
            (anterior["ordem"], pedido["id"])
        )

        cursor.execute(
            "UPDATE pedidos SET ordem=%s WHERE id=%s",
            (pedido["ordem"], anterior["id"])
        )

        conn.commit()

    cursor.close()
    conn.close()

    return redirect(f"/viagens/{pedido['viagem_id']}")

#botao descer
@viagens.route("/pedidos/<int:id>/descer")
def descer_pedido(id):

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT id, viagem_id, ordem
        FROM pedidos
        WHERE id = %s
    """,(id,))
    pedido = cursor.fetchone()

    cursor.execute("""
        SELECT id, ordem
        FROM pedidos
        WHERE viagem_id = %s AND ordem > %s
        ORDER BY ordem ASC
        LIMIT 1
    """,(pedido["viagem_id"], pedido["ordem"]))

    proximo = cursor.fetchone()

    if proximo:


        cursor.execute(
            "UPDATE pedidos SET ordem=%s WHERE id=%s",
            (proximo["ordem"], pedido["id"])
        )

        cursor.execute(
            "UPDATE pedidos SET ordem=%s WHERE id=%s",
            (pedido["ordem"], proximo["id"])
        )

        conn.commit()

    cursor.close()
    conn.close()

    return redirect(f"/viagens/{pedido['viagem_id']}")

#editar pedido
@viagens.route("/pedidos/<int:id>/editar", methods=["GET","POST"])
def editar_pedido(id):

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == "POST":

        loja_id = request.form["loja_id"]
        cliente_id = request.form["cliente_id"]
        tipo = request.form["tipo"]
        observacoes = request.form.get("observacoes","").strip()

        cursor.execute("""
            UPDATE pedidos
            SET loja_id=%s, cliente_id=%s, tipo=%s, observacoes=%s
            WHERE id=%s
        """,(loja_id, cliente_id, tipo, observacoes, id))

        conn.commit()

        cursor.execute("SELECT viagem_id FROM pedidos WHERE id=%s",(id,))
        viagem_id = cursor.fetchone()["viagem_id"]

        cursor.close()
        conn.close()

        return redirect(f"/viagens/{viagem_id}")

    cursor.execute("""
        SELECT *
        FROM pedidos
        WHERE id=%s
    """,(id,))
    pedido = cursor.fetchone()

    viagem_id = pedido["viagem_id"]

    cursor.execute("SELECT id,nome FROM shopping WHERE ativo=1")
    shoppings = cursor.fetchall()

    cursor.execute("SELECT id,nome,shopping_id FROM lojas WHERE ativo=1")
    lojas = cursor.fetchall()

    cursor.execute("SELECT id,nome FROM clientes WHERE ativo=1")
    clientes = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "novo_pedido.html",
        pedido=pedido,
        viagem_id=viagem_id,
        shoppings=shoppings,
        lojas=lojas,
        clientes=clientes
    )

#botao apagar pedido
@viagens.route("/pedidos/<int:id>/excluir")
def excluir_pedido(id):

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("SELECT viagem_id FROM pedidos WHERE id=%s",(id,))
    pedido = cursor.fetchone()

    viagem_id = pedido["viagem_id"]

    cursor.execute("DELETE FROM pedidos WHERE id=%s",(id,))

    cursor.execute("SET @ordem = 0")

    cursor.execute("""
        UPDATE pedidos
        SET ordem = (@ordem := @ordem + 1)
        WHERE viagem_id = %s
        ORDER BY ordem
    """, (viagem_id,))

    conn.commit()

    cursor.close()
    conn.close()

    return redirect(f"/viagens/{viagem_id}")