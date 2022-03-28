import os
from ctypes import sizeof
from flask import jsonify, request
from flask_restx import Resource
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
        return self.cryptContext.hash(password)

    def verifyPassword(self,passwordFromFront, passwordFromDb):
        return self.cryptContext.verify(passwordFromFront, passwordFromDb)

    def register(self):
        try:
            nome = request.json['nome']
            email = request.json['email']
            idEndereco = request.json['idEndereco']
            cpf = request.json['cpf']
            pis = request.json['pis']
            senha = self.getSenhaCriptografada(request.json['senha'])

            cursor = mydb.cursor()
            query = "INSERT INTO USUARIO(nome, email, idEndereco, cpf, pis, senha) values('%s','%s',%s,'%s',%s,'%s')"
            parametros = (nome, email, idEndereco, cpf, pis, senha)
            cursor.execute(query %parametros)
            mydb.commit()
            return jsonify({"status": 200})
        
        except Exception as e:
            return jsonify(str(e))

    def login(self):
        user = UsuarioLoginModel()
        print(request)
        user.getRequestData(request=request)               
        cursor = mydb.cursor(dictionary=True)        
        try:                      
            query = ("select id, cpf, senha from usuario where %s = '%s'")
            parametros = (user.tipo, user.login)  
            cursor.execute(query % parametros )
            result = cursor.fetchone()

            if result is not None:               
                if not self.verifyPassword(user.senha, result['senha']):
                    return jsonify({ "error": "Suas credenciais estão incorretas"}), 403     
                
                user.id = result['id']    
                                   
            else:
                return jsonify({"error":"Usuário não encontrado"}), 403
            payload = {
                "id":user.id,
                "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")))
            }

            token = jwt.encode(payload, os.getenv('SECRET_KEY'))
            cursor.close()

            return jsonify({"token": token})
        except Exception as error:
            cursor.close()

            return jsonify(str("A exception é: ",error)), 404
        finally:
            cursor.close()

    def getUser(self):
        tokenRequest = None
        if 'authorization' in request.headers:
            tokenRequest = request.headers['authorization']
          
        if not tokenRequest:
            print("sem token")
            return jsonify({"error": "Sem permissão para acessar"}), 403  

        response = self.auth.verifyAndDecodToken(token=tokenRequest)

        if response['status'] == "200":
            id = response['id']                      
            return self.getCurrentuser(id)

        return jsonify(response['error']), int(response['status'])
        
    def getCurrentuser(self,id):
        print("O id é: ", id)
        cursor = mydb.cursor(dictionary=True)        
        query = ("select * from usuario where id = %s")
        cursor.execute(query % (id))
        result = cursor.fetchone()
        return jsonify(result)
    
     

usuarioController = UsuarioController()