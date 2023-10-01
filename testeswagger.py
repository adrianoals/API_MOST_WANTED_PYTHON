from flask import Flask, jsonify
from flask_restplus import Api, Resource
import cx_Oracle

# Configurar a conexão com o Oracle
oracle_connection = cx_Oracle.connect('RM95667/281088@oracle.fiap.com.br:1521/ORCL')

app = Flask(__name__)
api = Api(app, version='1.0', title='API da Interpol e FBI', description='API para listar dados da Interpol e FBI')

# Crie um namespace para a rota da Interpol
interpol_ns = api.namespace('interpol', description='Operações relacionadas à Interpol')

@interpol_ns.route('/')
class InterpolResource(Resource):
    @interpol_ns.doc('listar_interpol')
    def get(self):
        '''Listar nomes da Interpol'''
        cursor = oracle_connection.cursor()
        cursor.execute('SELECT NAME FROM INTERPOLDATA FETCH FIRST 20 ROWS ONLY')
        names = [row[0].read() if row[0] is not None else None for row in cursor]
        cursor.close()
        return jsonify(names)

# Crie um namespace para a rota do FBI
fbi_ns = api.namespace('fbi', description='Operações relacionadas ao FBI')

@fbi_ns.route('/')
class FbiResource(Resource):
    @fbi_ns.doc('listar_fbi')
    def get(self):
        '''Listar títulos do FBI'''
        cursor = oracle_connection.cursor()
        cursor.execute('SELECT TITLE FROM FBIDATA FETCH FIRST 20 ROWS ONLY')
        titles = [row[0].read() if row[0] is not None else None for row in cursor]
        cursor.close()
        return jsonify(titles)

if __name__ == '__main__':
    app.run(port=5000, host='localhost', debug=True)
