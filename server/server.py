from flask import Flask
from flask_restx import Api
from mysql.connector import connection
from dotenv import load_dotenv, find_dotenv
from flask_cors import CORS



class Server():

    mydb = connection.MySQLConnection(
        host= "$HOST",
        user="$USER",
        password="$PASSWORD",
        database= "$DATABASE",
        connection_timeout=60,
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
 
server = Server()