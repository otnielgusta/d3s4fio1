
from email import header
import json
from wsgiref import headers

from flask import jsonify
from controllers.usuario_controller import UsuarioController
from routes import routes
from tests.conftest import client

#retorna header sem token
def getMockHeader():
    return  {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      }

#retorna header com token
def getMockHeaderWithToken(token):
    return {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'authorization': token
      }


#teste de cadastro
def test_register(client):
    url = '/auth/register'
   
    mock_data = {
        "cpf": "78978967899",
        "email": "teste@gmail.com",
        "cep": "39705000",
        "complemento": "Casa",
        "estado": "Minas Gerais",
        "municipio": "São João Evangelista",
        "numero": 1513,
        "pais": "Brasil",
        "rua": "Avenida Primeiro de Junho",
        "nome": "Usuario Teste",
        "pis": "88888888888",
        "senha": "senhateste",
    }

    response = client.post(url,data=json.dumps(mock_data), headers = getMockHeader())

    assert response.status_code == 200

#busca usuario pelo id
def test_request_getCurrentUser():
   
    usuarioController = UsuarioController()

    data = usuarioController.getCurrentuser(20)

    assert data['email'] == "otnielsilvag4@gmail.com"

#teste de login
def test_login(client):
    url = '/auth/login'

    mock_data = {
        "pis": "88888888888",
        "senha": "senhateste"
    }

    response = client.post(url, data = json.dumps(mock_data), headers = getMockHeader())
    
    results = json.loads(response.data)
    token = results['token']
    user = results['user']


    return token

#teste de update de dados do usuario
def test_update(client):
    url = '/auth/update'

    mock_data = {
        "cpf": "78978967899",
        "email": "teste@gmail.com",
        "cep": "39705000",
        "complemento": "Casa",
        "estado": "Minas Gerais",
        "municipio": "São João Evangelista",
        "numero": 1513,
        "pais": "Brasil",
        "rua": "Avenida Primeiro de Junho",
        "nome": "Usuario Teste alterado",
        "pis": "88888888888",
        "senha": "senhateste",
    }
    

    auth = test_login(client=client)


    if auth is not None:
        response = client.post(url, data = json.dumps(mock_data), headers = getMockHeaderWithToken(auth))

        assert response.status_code == 200

#teste de delete de usuario
def test_delete(client):
    url = '/auth/delete'

    auth = test_login(client=client)
    if auth is not None:
        response = client.post(url, headers= getMockHeaderWithToken(auth))

        assert response.status_code == 200

#teste para buscar usuario ja existente
def test_get_already_user(client):
    url = '/login/already'

    mock_data = {
        "email": "teste@gmail.com",
        "cpf": "78978967899",
        "pis": "88888888888",
    }

    response = client.post(url, data = json.dumps(mock_data), headers = getMockHeader())

    assert response.status_code == 404