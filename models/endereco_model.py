

class EnderecoModel():
    id:int
    pais:str
    estado:str
    municipio:str
    cep:str
    rua:str 
    numero:int
    complemento:str

    def fromBd(self, data):
        self.id = data['id']
        self.pais = data['pais']
        self.estado = data['estado']
        self.municipio = data['municipio']
        self.cep = data['cep']
        self.rua = data['rua']
        self.numero = data['numero']
        self.complemento = data['complemento']

    def toJson(self):
        return [{
            
                'pais': self.pais,
                'estado':self.estado,
                'municipio':self.municipio,
                'cep':self.cep,
                'rua':self.rua,
                'numero': self.numero,
                'complemento':self.complemento            
        }]