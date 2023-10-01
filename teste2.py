from flask import Flask, jsonify, redirect, request
from flasgger import Swagger
import cx_Oracle

# Configurar a conexão com o Oracle
oracle_connection = cx_Oracle.connect('RM95667/281088@oracle.fiap.com.br:1521/ORCL')

app = Flask(__name__)

# Config Swagger
app.config['SWAGGER'] = {
    'title': 'API MOST WANTED',
    # Outras configurações do Swagger aqui
}

# Inicializando o Swagger
swagger = Swagger(app)

# Rota do Swagger (flasgger)
@app.route('/apidocs')
def swagger_docs():
    return redirect('/apidocs/index.html')

# Rota raiz redirecionada para a rota do Swagger
@app.route('/')
def root():
    return redirect('/apidocs/index.html')


from flask import request

@app.route('/interpol', methods=['GET'])
def listar_interpol():
    """
    Listar nomes da Interpol
    ---
    parameters:
      - name: page
        in: query
        type: int
        description: Número da página a ser recuperada
      - name: per_page
        in: query
        type: int
        description: Número de itens por página
      - name: include_name
        in: query
        type: bool
        description: Incluir a coluna NAME na resposta
      - name: include_forename
        in: query
        type: bool
        description: Incluir a coluna FORENAME na resposta
    responses:
      200:
        description: Lista de nomes da Interpol
    """
    page = request.args.get('page', default=1, type=int)
    per_page = request.args.get('per_page', default=20, type=int)
    include_name = request.args.get('include_name', default=True, type=bool)
    include_forename = request.args.get('include_forename', default=True, type=bool)

    offset = (page - 1) * per_page

    columns = []
    if include_name:
        columns.append('NAME')
    if include_forename:
        columns.append('FORENAME')

    if not columns:
        return jsonify([])  # Nenhum campo selecionado, retornar lista vazia

    column_names = ', '.join(columns)

    cursor = oracle_connection.cursor()
    query = f'SELECT {column_names} FROM INTERPOLDATA OFFSET {offset} ROWS FETCH NEXT {per_page} ROWS ONLY'
    cursor.execute(query)

    data = []
    for row in cursor:
        item = {}
        for idx, column_name in enumerate(columns):
            value = row[idx].read() if row[idx] is not None else None
            item[column_name] = value
        data.append(item)

    cursor.close()
    return jsonify(data)



# Get FBI
@app.route('/fbi', methods=['GET'])
def listar_fbi():
    """
    Listar títulos do FBI
    ---
    responses:
      200:
        description: Lista de títulos do FBI
    """
    cursor = oracle_connection.cursor()
    cursor.execute('SELECT TITLE FROM FBIDATA FETCH FIRST 20 ROWS ONLY')
    titles = [row[0].read() if row[0] is not None else None for row in cursor]
    cursor.close()
    return jsonify(titles)

if __name__ == '__main__':
    app.run(port=5000, host='localhost', debug=True)
