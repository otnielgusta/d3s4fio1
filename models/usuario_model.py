import json
import uuid
from models.endereco_model import EnderecoModel


class UsuarioModel():
    pass
    id:int
    nome:str
    email:str
    endereco:EnderecoModel
    cpf:str
    pis:str
    senha:str

    def __init__(self) -> None:
        pass
        self.endereco = EnderecoModel()


    def fromBd(self, data):
        self.nome = data['nome']
        self.email = data['email']
        self.endereco.fromBd(data)
        self.cpf = data['cpf']
        self.pis = data['pis']

    def fromJson(self, data):     

        self.nome = data['nome']
        self.email = data['email']
        self.cpf = data['cpf']
        self.pis = data['pis']
        self.endereco.fromJson(data)

    def toJson(self):
        return {
            'nome': self.nome,
            'email': self.email,
            'endereco': self.endereco.toJson(),
            'cpf':self.cpf,
            'pis':self.pis
        }
        
