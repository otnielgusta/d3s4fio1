from flask_restx import Resource
from models.endereco_model import EnderecoModel
from models.usuario_model import UsuarioModel


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

    def update(self, user:UsuarioModel, idEndereco):
        try:
            cursor = mydb.cursor()
            query = "UPDATE endereco SET pais = '%s', estado = '%s', municipio = '%s', cep = '%s', rua = '%s', numero = '%s', complemento = '%s' where id = '%s'"
            parametros = (user.endereco.pais, user.endereco.estado, user.endereco.municipio, user.endereco.cep, user.endereco.rua, user.endereco.numero, user.endereco.complemento, idEndereco)
            cursor.execute(query % parametros)
            mydb.commit()    
            return 200
        except Exception as e:
            return {"error":str(e)}, 401
        finally:
            cursor.close()

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