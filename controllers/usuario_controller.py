from copyreg import constructor
import json
import os
from flask import jsonify, request
from flask_restx import Resource
from mysqlx import InternalError
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

    def authUpdateUser(self):
        tokenRequest = None
        if 'authorization' in request.headers:
            tokenRequest = request.headers['authorization']
          
        if not tokenRequest:
            return jsonify({"error": "Sem permissão para acessar"}), 403  

        response = self.auth.verifyAndDecodToken(token=tokenRequest)

        if response['status'] == "200":
            id = response['id']                      
            return self.updateUser(id)

        return jsonify(response['error']), int(response['status'])

    def getIdEnderecoByIdUsuario(self, id):
        cursor = mydb.cursor(dictionary=True)   

        try:
            query = ("select idEndereco from usuario where id = %s")
            cursor.execute(query % (id))
            result = cursor.fetchone()
            return result
        except Exception as e:
            return jsonify(str(e))
        finally:
            cursor.close()
    
    def updateUser(self, id):
        try:
            user = UsuarioModel()
            enderecoController = EnderecoController()
            data = json.loads(request.data)
            user.fromJson(data=data)
            user.id = id
            idEndereco = self.getIdEnderecoByIdUsuario(id)
            if idEndereco['idEndereco']:
                responseEndereco = enderecoController.update(idEndereco=idEndereco['idEndereco'],user=user)
                if responseEndereco == 200:
                    if data['senha'] != "":
                        senha = self.getSenhaCriptografada(data['senha'])
                        user.senha = senha 
                        response = self.updateWithPassword(user=user)
                        return response

                    else:

                        response = self.updateWithoutPassword(user=user)
                        return response  

                return responseEndereco             
                
        except Exception as e:
            return jsonify(str(e))

    def updateWithPassword(self, user:UsuarioModel):
        try:                
            cursor = mydb.cursor()
            query = "UPDATE USUARIO SET nome = '%s', email = '%s', cpf = '%s', pis = '%s', senha = '%s' where id = '%s'"
            parametros = (user.nome, user.email, user.cpf, user.pis, user.senha, user.id)
            cursor.execute(query % parametros)
            mydb.commit()
            return jsonify({"status": 200}), 200
        except Exception as e:
            return jsonify(str(e)), 401
        finally:
            cursor.close()

    def updateWithoutPassword(self, user:UsuarioModel):
        try:                
            cursor = mydb.cursor()
            query = "UPDATE USUARIO SET nome = '%s', email = '%s', cpf = '%s', pis = '%s' where id = '%s'"
            parametros = (user.nome, user.email, user.cpf, user.pis, user.id)
            cursor.execute(query % parametros)
            mydb.commit()
            return jsonify({"status": 200}), 200
        except Exception as e:
            return jsonify(str(e)), 401
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
            cursor.close()
            return response
        except Exception as error:
            cursor.close()
            return jsonify(str("A exception é: ",error)), 404
        

    def getAuthenticateAndId(self):
        tokenRequest = None
        if 'authorization' in request.headers:
            tokenRequest = request.headers['authorization']
        
        if not tokenRequest:
                return jsonify({"error": "Sem permissão para acessar"}), 403  
        
        response = self.auth.verifyAndDecodToken(token=tokenRequest)

        return response

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
        query = ("select nome, email, cpf, pis, e.id as idEndereco, pais, estado, municipio, cep, rua, numero, complemento from usuario as u inner join endereco as e on u.idEndereco = e.id where u.id = %s")
        cursor.execute(query % (id))
        result = cursor.fetchone()
        user.fromBd(result)
        return user.toJson()
    
    def deleteUser(self):
        response = self.getAuthenticateAndId()
        if response['status'] == "200":
            id = response['id']                      
            cursor = mydb.cursor(dictionary=True)        
            try:
                query = ("delete from usuario where id = %s")
                cursor.execute(query % (id))
                return jsonify(), 200
            except Exception as e:
                return jsonify(str(e)), 401
        return jsonify(), 401

    def getAlreadyEmail(self, email):
        print(email)
        cursor = mydb.cursor(dictionary=True)   

        try:
            query = ("select email from usuario where email = '%s'")
            cursor.execute(query % (email))
            result = cursor.fetchone()
            print(result)
            return {
                "key":"email",
                "value": result
                }
        except InternalError as e:
            return {
                "key": "no",
                "value": e
            }

        except Exception as e:
            return {
                "key": "no",
                "value": e
            }
        finally:
            cursor.close()

    def getAlreadyPis(self, pis):
        cursor = mydb.cursor(dictionary=True, buffered=True)   

        try:
            query = ("select pis from usuario where pis = '%s'")
            cursor.execute(query % (pis))
            result = cursor.fetchone()
            print("pis")
            return {
                "key":"pis",
                "value": result
                }
        except InternalError as e:
            return {
                "key": "no",
                "value": e
            }
        except Exception as e:
            return {
                "key": "no",
                "value": e
            }
        finally:
            cursor.close()

    def getUserAlreadyCpf(self, cpf):
        cursor = mydb.cursor(dictionary=True, buffered=True)   

        try:
            query = ("select cpf from usuario where cpf = '%s'")
            cursor.execute(query % (cpf))
            result = cursor.fetchone()
            print(result)
            return {
                "key":"cpf",
                "value": result
                }
        except InternalError as e:
            print(e.msg)
            return {
                "key": "no",
                "value": e
            }
        except Exception as e:
            return {
                "key": "no",
                "value": e
            }
        finally:
            cursor.close()

    def getUserAlready(self):
        try:
            user = UsuarioModel()
            data = json.loads(request.data)
            print(data)
            print("antes")
            user.fromJsonValidateAlready(data=data) 
            alreadyEmail = self.getAlreadyEmail(email=user.email)
            alreadyCpf = self.getUserAlreadyCpf(cpf=user.cpf)
            alreadyPis = self.getAlreadyPis(pis=user.pis)
            print(alreadyEmail)
            print(alreadyCpf)
            print(alreadyPis)

            if alreadyEmail['key']:

                if alreadyEmail['key'] == 'email':
                    print("entrou email")
                    if alreadyEmail['value'] is not None:
                        return jsonify({
                            "status": "yes",
                            "text": "Email já cadastrado!"
                            }), 200
            
            if alreadyCpf['key']:
                if alreadyCpf['key'] == 'cpf':
                    print("entrou cpf") 
                    if alreadyCpf['value'] is not None:
                        return jsonify({
                            "status": "yes",
                            "text": "CPF já cadastrado!"
                            }), 200

            if alreadyPis['key']:
                if alreadyPis['key'] == 'pis':
                    print("entrou pis")

                    if alreadyPis['value'] is not None:
                        return jsonify({
                            "status": "yes",
                            "text": "PIS já cadastrado!"
                            }), 200

            if(alreadyEmail['value'] is None) and alreadyCpf['value'] is None and alreadyPis['value'] is None:
                print("não tem")
                return jsonify({"status": "no"}), 404
        except Exception as e:
            return jsonify({"error": e}), 401
            

usuarioController = UsuarioController()