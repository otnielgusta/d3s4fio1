from flask import Flask
from flask_restful import Api
from flask_restx import api
from mysql.connector import connection

class Server():

    mydb = connection.MySQLConnection(
        host='127.0.0.1',
        user='root',
        password='Contrabaixo98',
        database= 'desafio1'
    )

    app = Flask(__name__)
    api = Api(app)

server = Server()