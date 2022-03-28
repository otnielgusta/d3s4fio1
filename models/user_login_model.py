from base64 import decode
from flask import request
import json


class UsuarioLoginModel():
    pass
    id:int
    login:str
    tipo:str
    senha:str

    def fromBd(self, data):
        self.id = data['id']
        self.login = data['login']
        self.tipo = data['tipo']
        self.senha = data['senha']
    
    def getRequestData(self, data):
        request = json.loads(data)
        if 'email' in request:  
            self.tipo = 'email'
            self.login = str(request['email'])

        elif 'cpf' in request:
            self.tipo = 'cpf'
            self.login = str(request['cpf'])

        elif 'pis' in request:
            self.tipo= 'pis'            
            self.login = str(request['pis'])

        self.senha = str(request['senha'])      
