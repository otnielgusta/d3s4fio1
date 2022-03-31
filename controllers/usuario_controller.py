import json
from lib2to3.pgen2 import token
import os
from flask import jsonify, request
from flask_restx import Resource
from controllers.endereco_controller import EnderecoController
from models.user_login_model import UsuarioLoginModel
from models.usuario_model import UsuarioModel
from server.server import server
from passlib.context import CryptContext
from dotenv import load_dotenv, find_dotenv
from controllers.authenticate import Authenticate
import datetime
import jwt

mydb = server.mydb
api = server.api
app = server.app

load_dotenv(find_dotenv())

class UsuarioController(Resource):
    cryptContext = CryptContext(schemes=["bcrypt"])
    auth = Authenticate()

    def getSenhaCriptografada(self,password):
        print(password)
        return self.cryptContext.hash(password)

    def verifyPassword(self,passwordFromFront, passwordFromDb):
        return self.cryptContext.verify(passwordFromFront, passwordFromDb)

    def register(self):
        cursor = mydb.cursor()
        try:
            user = UsuarioModel()
            enderecoController = EnderecoController()
            data = json.loads(request.data)
            user.fromJson(data=data)
            senha = self.getSenhaCriptografada(data['senha'])
            user.senha = senha
            
            lastId =  enderecoController.insert(user.endereco)
            if lastId != "":
                print(lastId)
                query = "INSERT INTO USUARIO(nome, email, idEndereco, cpf, pis, senha) values('%s','%s',%s,'%s',%s,'%s')"
                parametros = (user.nome, user.email, lastId['last_insert_id()'], user.cpf, user.pis, user.senha)
                cursor.execute(query %parametros)
                print("entrou exerc")
                mydb.commit()
                return jsonify({"status": 200}), 200
            else:
                return Exception
        
        except Exception as e:
            print(e)
            return jsonify(str(e))

        finally:
            cursor.close()

    def login(self):
        user = UsuarioLoginModel()
        user.getRequestData(data=request.data)     

        cursor = mydb.cursor(dictionary=True)    
        try:                      
            query = ("select id, cpf, senha from usuario where %s = '%s'")
            parametros = (user.tipo, user.login)  
            cursor.execute(query % parametros )
            result = cursor.fetchone()

            if result is not None: 
                if not self.verifyPassword(user.senha, result['senha']):
                    return jsonify({ "error": "Suas credenciais estão incorretas"}), 401     
                
                user.id = result['id']    
                                   
            else:
                return jsonify({"error":"Usuário não encontrado"}), 403
            payload = {
                "id":user.id,
                "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")))
            }

            userResponse = self.getCurrentuser(user.id)
            

            token = jwt.encode(payload, os.getenv('SECRET_KEY'))
            response = jsonify({
                "token": token,
                "user": userResponse
            })
            response.headers.add('Access-Control-Allow-Origin', '*')

            return response
        except Exception as error:

            return jsonify(str("A exception é: ",error)), 404
        finally:
            cursor.close()

    def getAutheticate(self):
        tokenRequest = None
        if 'authorization' in request.headers:
            tokenRequest = request.headers['authorization']
        
        if not tokenRequest:
                return jsonify({"error": "Sem permissão para acessar"}), 403  
        
        response = self.auth.verifyToken(token=tokenRequest)

        return response

    def getUser(self):
        tokenRequest = None
        if 'authorization' in request.headers:
            tokenRequest = request.headers['authorization']
          
        if not tokenRequest:
            return jsonify({"error": "Sem permissão para acessar"}), 403  

        response = self.auth.verifyAndDecodToken(token=tokenRequest)

        if response['status'] == "200":
            id = response['id']                      
            return self.getCurrentuser(id)

        return jsonify(response['error']), int(response['status'])
        
    def getCurrentuser(self,id):
        user = UsuarioModel()
        cursor = mydb.cursor(dictionary=True)        
        query = ("select u.id as id, nome, email, cpf, pis, e.id as idEndereco, pais, estado, municipio, cep, rua, numero, complemento from usuario as u inner join endereco as e on u.idEndereco = e.id where u.id = %s")
        cursor.execute(query % (id))
        result = cursor.fetchone()
        user.fromBd(result)
        return user.toJson()
    
     

usuarioController = UsuarioController()