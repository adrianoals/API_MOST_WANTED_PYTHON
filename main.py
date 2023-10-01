from flask import Flask, jsonify
# from flask_restplus import Api
import cx_Oracle
import base64

# Configurar a conexão com o Oracle
oracle_connection = cx_Oracle.connect('RM95667/281088@oracle.fiap.com.br:1521/ORCL')

app = Flask(__name__)



@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/interpol', methods=['GET'])
def listar_interpol():
    cursor = oracle_connection.cursor()
    cursor.execute('SELECT NAME, FORENAME FROM INTERPOLDATA FETCH FIRST 20 ROWS ONLY')
    
    # Ler os resultados da consulta
    results = []
    for row in cursor:
        name = row[0].read() if row[0] is not None else None
        forename = row[1].read() if row[1] is not None else None
        results.append({'name': name.decode('utf-8') if name else None, 'forename': forename.decode('utf-8') if forename else None})
    
    cursor.close()
    return jsonify(results)


# @app.route('/interpol', methods=['GET'])
# def listar_interpol():
#     cursor = oracle_connection.cursor()
#     cursor.execute('SELECT NAME, FORENAME FROM INTERPOLDATA FETCH FIRST 20 ROWS ONLY')
#     # Ler os resultados da consulta e converter LOBs para Base64
#     results = []
#     for row in cursor:
#         name = row[0] if row[0] is not None else None
#         forename = row[1] if row[1] is not None else None
#         results.append({'name': name, 'forename': forename})
#     cursor.close()
#     return jsonify(results)
    # name = [row[0].read() if row[0] is not None else None for row in cursor]
    # forename = [row[0].read() if row[0] is not None else None for row in cursor]
    # cursor.close()
    # return jsonify(name)

@app.route('/fbi', methods=['GET'])
def listar_fbi():
    cursor = oracle_connection.cursor()
    cursor.execute('SELECT TITLE FROM FBIDATA FETCH FIRST 20 ROWS ONLY')
    title = [row[0].read() if row[0] is not None else None for row in cursor]
    cursor.close()
    return jsonify(title)


if __name__ == '__main__':
    app.run(port=5000, host='localhost', debug=True)
