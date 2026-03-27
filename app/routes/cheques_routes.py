from flask import Blueprint, render_template, request, redirect, flash
from app.config import get_db_connection

cheques = Blueprint('cheques', __name__, url_prefix='/cheques')

#listagem cheques
@cheques.route('', strict_slashes=False)
def listar_cheques():


    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
    SELECT *
    FROM cheques
    WHERE ativo = TRUE
    ORDER BY criado_em DESC
""")

    lista = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("cheques.html", cheques=lista)


#form cheque
@cheques.route('/novo', methods=['GET', 'POST'])
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

        return redirect('/cheques')


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
    return redirect('/cheques')

#botao sustar no cheque
@cheques.route('/<int:id>/devolver')
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

    return redirect('/cheques')

#apagar botao
@cheques.route('/<int:id>/excluir')
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

    return redirect('/cheques')


#editrar
@cheques.route('/<int:id>/editar', methods=['GET', 'POST'])
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

        return redirect('/cheques')

    cursor.execute("SELECT * FROM cheques WHERE id = %s", (id,))
    cheque = cursor.fetchone()

    cursor.close()
    conn.close()

    return render_template("novo_cheque.html", cheque=cheque)

