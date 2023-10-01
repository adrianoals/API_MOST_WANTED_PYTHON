from flask import Flask, jsonify, redirect
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


# Get Interpol
@app.route('/interpol', methods=['GET'])
def listar_interpol():
    """
    Listar nomes da Interpol
    ---
    responses:
      200:
        description: Lista de nomes da Interpol
    """
    cursor = oracle_connection.cursor()
    cursor.execute('SELECT NAME FROM INTERPOLDATA FETCH FIRST 20 ROWS ONLY')
    names = [row[0].read() if row[0] is not None else None for row in cursor]
    cursor.close()
    return jsonify(names)

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
