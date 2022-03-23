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
        self.id = data['id']
        self.nome = data['nome']
        self.email = data['email']
        self.endereco.id = data['idEndereco']
        self.endereco.pais = data['pais']
        self.endereco.estado = data['estado']
        self.endereco.municipio = data['municipio']
        self.endereco.numero = data['numero']
        self.endereco.rua = data['rua']
        self.endereco.complemento = data['complemento']
        self.cpf = data['cpf']
        self.pis = data['pis']

    def toJson(self):
        return {
            'nome': self.nome,
            'email': self.email,
            'endereco': self.endereco.toJson,
            'cpf':self.cpf,
            'pis':self.pis
        }
        
