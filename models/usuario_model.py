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

    def fromBd(self, data):
        self.endereco = EnderecoModel()
        self.id = data['id']
        self.nome = data['nome']
        self.email = data['email']
        self.endereco.fromBd(data)
        self.cpf = data['cpf']
        self.pis = data['pis']

    def toJson(self):
        return {
            'nome': self.nome,
            'email': self.email,
            'endereco': self.endereco.toJson(),
            'cpf':self.cpf,
            'pis':self.pis
        }
        
