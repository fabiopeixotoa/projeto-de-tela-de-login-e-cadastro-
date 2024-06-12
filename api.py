def get_db_connection():
    conn = psycopg2.connect(
        host="localhost",
        database="cadastro_clientes",
        user="seu_usuario",
        password="sua_senha"
    )
    return conn

@app.route('/clientes', methods=['GET'])
def get_clientes():
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute('SELECT * FROM clientes;')
    clientes = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(clientes)

@app.route('/clientes/<int:id>', methods=['GET'])
def get_cliente(id):
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute('SELECT * FROM clientes WHERE id = %s;', (id,))
    cliente = cursor.fetchone()
    cursor.close()
    conn.close()
    if cliente is None:
        return jsonify({'error': 'Cliente não encontrado'}), 404
    return jsonify(cliente)

@app.route('/clientes', methods=['POST'])
def create_cliente():
    novo_cliente = request.get_json()
    nome = novo_cliente['nome']
    email = novo_cliente['email']
    telefone = novo_cliente.get('telefone')
    endereco = novo_cliente.get('endereco')

    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute(
        'INSERT INTO clientes (nome, email, telefone, endereco) VALUES (%s, %s, %s, %s) RETURNING *;',
        (nome, email, telefone, endereco)
    )
    cliente_criado = cursor.fetchone()
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify(cliente_criado), 201

@app.route('/clientes/<int:id>', methods=['PUT'])
def update_cliente(id):
    dados_atualizados = request.get_json()
    nome = dados_atualizados.get('nome')
    email = dados_atualizados.get('email')
    telefone = dados_atualizados.get('telefone')
    endereco = dados_atualizados.get('endereco')

    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute(
        'UPDATE clientes SET nome = %s, email = %s, telefone = %s, endereco = %s WHERE id = %s RETURNING *;',
        (nome, email, telefone, endereco, id)
    )
    cliente_atualizado = cursor.fetchone()
    conn.commit()
    cursor.close()
    conn.close()
    if cliente_atualizado is None:
        return jsonify({'error': 'Cliente não encontrado'}), 404
    return jsonify(cliente_atualizado)

@app.route('/clientes/<int:id>', methods=['DELETE'])
def delete_cliente(id):
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute('DELETE FROM clientes WHERE id = %s RETURNING *;', (id,))
    cliente_deletado = cursor.fetchone()
    conn.commit()
    cursor.close()
    conn.close()
    if cliente_deletado is None:
        return jsonify({'error': 'Cliente não encontrado'}), 404
    return jsonify(cliente_deletado), 204

if __name__ == '__main__':
    app.run(debug=True)