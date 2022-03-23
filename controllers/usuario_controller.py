from ast import parse
from flask import jsonify, request
from flask_restx import Resource
from models.usuario_model import UsuarioModel

from server.server import server

mydb = server.mydb
class UsuarioController(Resource):
    def get(self):
        cursor = mydb.cursor(dictionary=True)
        usuario = UsuarioModel()
        try:
            query = ("select * from usuario u inner join endereco e on e.id = u.idEndereco where u.id = %s")
            parametros = (request.args.get('id'))
            cursor.execute(query, parametros)
            result = cursor.fetchall()
            print("antes do from bd")

            #print(result['nome'])
            #usuario.fromBd(result)
            print("depois do from bd")

        except:
            return "Ocorreu um erro"
        finally:
            cursor.close()
        return jsonify(result)