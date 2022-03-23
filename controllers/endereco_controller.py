from flask_restx import Resource
from models.endereco_model import EnderecoModel

from server.server import server

mydb = server.mydb

class EnderecoController(Resource):
    def get(self, id):
        conn = mydb.cursor()
        endereco = EnderecoModel()
        try:
            query = "select * from endereco where id = %s"
            parametros = (id)
            conn.execute(query, parametros)
            response = conn.fetchall()
            endereco.fromBd(response)
        except:
            return "Ocorreu um erro"
        finally:
            conn.close()