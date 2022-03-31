from flask_restx import Resource
from models.endereco_model import EnderecoModel
from flask import jsonify


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

    def insert(self, endereco:EnderecoModel):
        cursor = mydb.cursor(dictionary=True)
        try:
            lastId = ""
            query = "INSERT INTO endereco(pais, estado, municipio, cep, rua, numero, complemento) values('%s','%s','%s','%s','%s','%s','%s')"
            query2 = "select last_insert_id();"
            parametros = (endereco.pais, endereco.estado, endereco.municipio, endereco.cep, endereco.rua, endereco.numero, endereco.complemento)
            cursor.execute(query % parametros)

            mydb.commit()

            cursor.execute(query2)

            lastId = cursor.fetchone()
            return lastId
        except Exception as e:
            print(e)
            return False
        finally:
            cursor.close()