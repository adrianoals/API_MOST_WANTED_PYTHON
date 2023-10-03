from flask import Flask, jsonify, redirect, request
from flasgger import Swagger
import cx_Oracle

# Configurar a conexão com o Oracle
oracle_connection = cx_Oracle.connect('XXXXXX/XXXXXX@oracle.fiap.com.br:1521/ORCL')

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

@app.route('/interpol', methods=['GET'])
def listar_interpol():
    """
    Lista dos Mais Procurados da Interpol
    ---
    parameters:
      - name: page
        in: query
        type: int
        description: Número da página a ser recuperada
        default: 1
      - name: per_page
        in: query
        type: int
        description: Número de itens por página, limite de 20 itens
        default: 20
        maximum: 20
    responses:
      200:
        description: Lista de nomes da Interpol
    """
    page = request.args.get('page', default=1, type=int)
    per_page = request.args.get('per_page', default=20, type=int)

    offset = (page - 1) * per_page

    cursor = oracle_connection.cursor()
    cursor.execute(f'SELECT NAME, FORENAME, DATE_OF_BIRTH, ENTITY_ID FROM INTERPOLDATA OFFSET {offset} ROWS FETCH NEXT {per_page} ROWS ONLY')
    
    data = []
    for row in cursor:
        name = row[0].read() if row[0] is not None else None
        forename = row[1].read() if row[1] is not None else None
        date_of_birth = row[2].read() if row[2] is not None else None
        entity_id = row[3].read() if row[3] is not None else None
        data.append({'NAME': name, 'FORENAME': forename, 'DATE_OF_BIRTH': date_of_birth, 'ENTITY_ID': entity_id})
    
    cursor.close()
    return jsonify(data)

# Get FBI
@app.route('/fbi', methods=['GET'])
def listar_fbi():
    """
    Lista dos Mais Procurados do FBI
    ---
    parameters:
      - name: page
        in: query
        type: int
        description: Número da página a ser recuperada
        default: 1
      - name: per_page
        in: query
        type: int
        description: Número de itens por página, limite de 20 itens
        default: 20
        maximum: 20
    responses:
      200:
        description: Lista de nomes do FBI
    """
    page = request.args.get('page', default=1, type=int)
    per_page = request.args.get('per_page', default=20, type=int)

    offset = (page - 1) * per_page

    cursor = oracle_connection.cursor()
    cursor.execute(f'SELECT TITLE, NATIONALITY, URL, CAUTION, DESCRIPTION FROM FBIDATA OFFSET {offset} ROWS FETCH NEXT {per_page} ROWS ONLY')
    
    data = []
    for row in cursor:
        title = row[0].read() if row[0] is not None else None
        nationality = row[1].read() if row[1] is not None else None
        url = row[2].read() if row[2] is not None else None
        caution = row[3].read() if row[3] is not None else None
        description = row[4].read() if row[4] is not None else None
        data.append({'TITLE': title, 'NATIONALITY': nationality, 'URL': url, 'CAUTION': caution, 'DESCRIPTION': description})

    cursor.close()
    return jsonify(data)


if __name__ == '__main__':
    app.run(port=5000, host='localhost', debug=True)
