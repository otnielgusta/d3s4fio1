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
    
    def getRequestData(self, request):
        if 'email' in request.json:  
            self.tipo = 'email'
            self.login = request.json['email']

        elif 'cpf' in request.json:
            self.tipo = 'cpf'
            self.login = request.json['cpf']

        elif 'pis' in request.json:
            self.tipo= 'pis'            
            self.login = request.json['pis']

        self.senha = request.json['senha']      
