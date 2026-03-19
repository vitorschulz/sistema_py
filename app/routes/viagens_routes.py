from flask import Blueprint, render_template, request, redirect, jsonify, flash
from collections import defaultdict
from app.config import get_db_connection

viagens = Blueprint("viagens", __name__)

# listar
@viagens.route("/viagens")
def listar_viagens():

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    data = request.args.get("data")
    data_inicio = request.args.get("data_inicio")
    data_fim = request.args.get("data_fim")

    query = """
        SELECT *
        FROM viagens
        WHERE ativo = 1
    """

    params = []

    if data:
        query += " AND data_viagem = %s"
        params.append(data)
        

    elif data_inicio and data_fim:
        query += " AND data_viagem BETWEEN %s AND %s"
        params.append(data_inicio)
        params.append(data_fim)

    elif data_inicio:
        query += " AND data_viagem = %s"
        params.append(data_inicio)

    elif data_fim:
        query += " AND data_viagem = %s"
        params.append(data_fim)

    query += " ORDER BY data_viagem DESC"

    cursor.execute(query, tuple(params))
    viagens_lista = cursor.fetchall()


    cursor.close()
    conn.close()

    return render_template("viagens.html", viagens=viagens_lista)


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

        flash("Viagem criada com sucesso!", "success")

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
            pedidos.observacoes,
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

        ORDER BY 
        shopping.nome,
        lojas.nome,
        pedidos.ordem
    """, (id,))

    pedidos = cursor.fetchall()

    estrutura = defaultdict(lambda: defaultdict(list))

    for pedido in pedidos:

        estrutura[pedido["shopping_nome"]][pedido["loja_nome"]].append(pedido)

    cursor.execute("""
    SELECT vc.id, vc.ordem, c.nome, c.endereco, vc.cliente_id
    FROM viagem_clientes vc
    JOIN clientes c ON c.id = vc.cliente_id
    WHERE vc.viagem_id = %s
    ORDER BY vc.ordem
""", (id,))

    clientes_viagem = cursor.fetchall()

    cursor.execute("""
    SELECT id, nome 
    FROM clientes 
    WHERE ativo = 1
    """)

    clientes = cursor.fetchall()

    cursor.execute("""
    SELECT *
    FROM viagem_financeiro
    WHERE viagem_id = %s
""", (id,))

    financeiro = cursor.fetchall()

    total_ganho = sum(f["valor"] for f in financeiro if f["tipo"] == "GANHO")
    total_custo = sum(f["valor"] for f in financeiro if f["tipo"] == "CUSTO")

    saldo = total_ganho - total_custo

    total_clientes = len(clientes_viagem)

    total_shoppings = len(estrutura)

    total_lojas = sum(len(lojas) for lojas in estrutura.values())

    total_pedidos = sum(
        len(pedidos)
        for lojas in estrutura.values()
        for pedidos in lojas.values()
    )

    cursor.close()
    conn.close()

    return render_template(
        "viagem_detalhe.html",
        viagem=viagem,
        estrutura=estrutura,
        clientes_viagem=clientes_viagem,
        clientes=clientes,
        financeiro=financeiro,
        total_ganho=total_ganho,
        total_custo=total_custo,
        saldo=saldo,
        total_clientes=total_clientes,
        total_shoppings=total_shoppings,
        total_lojas=total_lojas,
        total_pedidos=total_pedidos
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
            AND loja_id = %s
        """, (id, loja_id))

        ordem = cursor.fetchone()["nova_ordem"]

        cursor.execute("""
            INSERT INTO pedidos
            (viagem_id, loja_id, cliente_id, tipo, observacoes, ordem)
            VALUES (%s,%s,%s,%s,%s,%s)
        """,(id, loja_id, cliente_id, tipo, observacoes, ordem))

        conn.commit()

        cursor.close()
        conn.close()

        flash("Tarefa adicionada com sucesso!", "success")

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

        flash("Viagem atualizada com sucesso!", "success")

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

    flash("Viagem excluída com sucesso!", "success")

    return redirect("/viagens")


#seta p cima
@viagens.route("/pedidos/<int:id>/subir")
def subir_pedido(id):

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT id, viagem_id, loja_id, ordem
        FROM pedidos
        WHERE id = %s
    """,(id,))
    pedido = cursor.fetchone()

    cursor.execute("""
        SELECT id, ordem
        FROM pedidos
        WHERE viagem_id = %s 
        AND loja_id = %s
        AND ordem < %s
        ORDER BY ordem DESC
        LIMIT 1
    """,(pedido["viagem_id"], pedido["loja_id"], pedido["ordem"]))

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
@viagens.route("/pedidos/<int:id>/descer", methods=["POST"])
def descer_pedido(id):

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT id, viagem_id, loja_id, ordem
        FROM pedidos
        WHERE id = %s
    """,(id,))
    pedido = cursor.fetchone()

    cursor.execute("""
        SELECT id, ordem
        FROM pedidos
        WHERE viagem_id = %s
        AND loja_id = %s
        AND ordem > %s
        ORDER BY ordem ASC
        LIMIT 1
    """,(pedido["viagem_id"], pedido["loja_id"], pedido["ordem"]))

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
        next_url = request.form.get("next")

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

        flash("Tarefa atualizada com sucesso!", "success")

        if next_url:
            return redirect(next_url)

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
    
    cursor.execute("SELECT viagem_id, loja_id FROM pedidos WHERE id=%s",(id,))
    pedido = cursor.fetchone()

    viagem_id = pedido["viagem_id"]
    loja_id = pedido["loja_id"]

    cursor.execute("DELETE FROM pedidos WHERE id=%s",(id,))

    cursor.execute("SET @ordem = 0")

    cursor.execute("""
        UPDATE pedidos
        SET ordem = (@ordem := @ordem + 1)
        WHERE viagem_id = %s
        AND loja_id = %s
        ORDER BY ordem
    """, (viagem_id, loja_id))

    conn.commit()

    cursor.close()
    conn.close()

    flash("Tarefa excluída com sucesso!", "success")

    return redirect(f"/viagens/{viagem_id}")

#add cliente pra ordem
@viagens.route("/viagens/<int:id>/add_cliente", methods=["POST"])
def add_cliente(id):

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cliente_id = request.form["cliente_id"]


    cursor.execute("""
        SELECT 1 FROM viagem_clientes
        WHERE viagem_id=%s AND cliente_id=%s
    """, (id, cliente_id))

    if cursor.fetchone():
        flash("Este cliente já está na viagem!", "error")
        cursor.close()
        conn.close()
        return redirect(request.form.get("next") or f"/viagens/{id}")


    cursor.execute("""
        SELECT COALESCE(MAX(ordem),0)+1 AS nova_ordem
        FROM viagem_clientes
        WHERE viagem_id = %s
    """, (id,))

    ordem = cursor.fetchone()["nova_ordem"]

    cursor.execute("""
        INSERT INTO viagem_clientes (viagem_id, cliente_id, ordem)
        VALUES (%s,%s,%s)
    """, (id, cliente_id, ordem))

    conn.commit()

    cursor.close()
    conn.close()

    flash("Cliente adicionado na ordem!", "success")

    return redirect(request.form.get("next") or f"/viagens/{id}")


#exccluir da lista
@viagens.route("/viagem_cliente/<int:id>/excluir")
def excluir_cliente_viagem(id):

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    next_url = request.args.get("next")

    cursor.execute("SELECT viagem_id FROM viagem_clientes WHERE id=%s", (id,))
    data = cursor.fetchone()
    viagem_id = data["viagem_id"]

    cursor.execute("DELETE FROM viagem_clientes WHERE id=%s", (id,))

    cursor.execute("SET @ordem = 0")

    cursor.execute("""
        UPDATE viagem_clientes
        SET ordem = (@ordem := @ordem + 1)
        WHERE viagem_id = %s
        ORDER BY ordem
    """, (viagem_id,))

    conn.commit()

    cursor.close()
    conn.close()

    flash("Cliente removido com sucesso!", "success")

    if next_url:
        return redirect(next_url)

    return redirect(f"/viagens/{viagem_id}")

#seta subir cliente ordem
@viagens.route("/viagem_cliente/<int:id>/subir")
def subir_cliente(id):

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM viagem_clientes WHERE id=%s", (id,))
    atual = cursor.fetchone()

    cursor.execute("""
        SELECT * FROM viagem_clientes
        WHERE viagem_id=%s AND ordem < %s
        ORDER BY ordem DESC LIMIT 1
    """, (atual["viagem_id"], atual["ordem"]))

    anterior = cursor.fetchone()

    if anterior:
        cursor.execute("UPDATE viagem_clientes SET ordem=%s WHERE id=%s",
                       (anterior["ordem"], atual["id"]))

        cursor.execute("UPDATE viagem_clientes SET ordem=%s WHERE id=%s",
                       (atual["ordem"], anterior["id"]))

        conn.commit()

    cursor.close()
    conn.close()

    return redirect(request.args.get("next") or f"/viagens/{atual['viagem_id']}")


#descer ordem
@viagens.route("/viagem_cliente/<int:id>/descer")
def descer_cliente(id):

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM viagem_clientes WHERE id=%s", (id,))
    atual = cursor.fetchone()

    cursor.execute("""
        SELECT * FROM viagem_clientes
        WHERE viagem_id=%s AND ordem > %s
        ORDER BY ordem ASC LIMIT 1
    """, (atual["viagem_id"], atual["ordem"]))

    proximo = cursor.fetchone()

    if proximo:
        cursor.execute("UPDATE viagem_clientes SET ordem=%s WHERE id=%s",
                       (proximo["ordem"], atual["id"]))

        cursor.execute("UPDATE viagem_clientes SET ordem=%s WHERE id=%s",
                       (atual["ordem"], proximo["id"]))

        conn.commit()

    cursor.close()
    conn.close()

    return redirect(request.args.get("next") or f"/viagens/{atual['viagem_id']}")

#add financeiro
@viagens.route("/viagens/<int:id>/financeiro/add", methods=["POST"])
def add_financeiro(id):

    tipo = request.form["tipo"]
    valor = float(request.form["valor"])
    descricao = request.form.get("descricao", "")

    if valor <= 0:
        flash("O valor deve ser positivo!", "error")
        return jsonify({"erro": "Valor inválido"}), 400

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        INSERT INTO viagem_financeiro
        (viagem_id, tipo, valor, descricao)
        VALUES (%s,%s,%s,%s)
    """, (id, tipo, valor, descricao))

    conn.commit()

    cursor.execute("SELECT LAST_INSERT_ID() as id")
    novo_id = cursor.fetchone()["id"]

    cursor.close()
    conn.close()


    return jsonify({
    "id": novo_id,
    "tipo": tipo,
    "valor": valor,
    "descricao": descricao
    })

#deletar financeiro
@viagens.route("/financeiro/<int:id>/delete", methods=["POST"])
def deletar_financeiro(id):

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # pega antes de deletar (pra atualizar saldo)
    cursor.execute("SELECT tipo, valor FROM viagem_financeiro WHERE id = %s", (id,))
    item = cursor.fetchone()

    if not item:
        return jsonify({"erro": "Não encontrado"}), 404

    cursor.execute("DELETE FROM viagem_financeiro WHERE id = %s", (id,))
    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({
        "tipo": item["tipo"],
        "valor": item["valor"]
    })