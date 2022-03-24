from flask import jsonify, request
from flask_restx import Resource
from models.usuario_model import UsuarioModel
from server.server import server


mydb = server.mydb

class UsuarioController(Resource):
    def post(self):
        
        
        cursor = mydb.cursor(dictionary=True)        
        usuario = UsuarioModel()
        try:
            
            query = ('select * from usuario u inner join endereco e on e.id = u.idEndereco where u.id = %s')
            parametros = (request.form.get('id'))
            cursor.execute(query % parametros)
            result = cursor.fetchone()
            usuario.fromBd(result)
            

        except Exception as error:
            return error
        finally:
            cursor.close()
        return jsonify(usuario.toJson())