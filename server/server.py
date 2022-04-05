from flask import Flask
from flask_restx import Api
from mysql.connector import connection
from flask_cors import CORS


class Server():

    mydb = connection.MySQLConnection(
        host='127.0.0.1',
        user='root',
        password='',
        database= 'desafio1'
    )

    app = Flask(__name__)
    CORS(app)
    cors = CORS(app, resources={
        r"/*":{
            "origins": "*"
        }
    })
    api = Api(app)
    
    

    if __name__ == "__main__":
        pass     

def create_app():
    app = Flask(__name__)
    return app   
server = Server()