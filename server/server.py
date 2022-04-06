import os
import dotenv
from flask import Flask
from flask_restx import Api
from mysql.connector import connection
from dotenv import load_dotenv, find_dotenv
from flask_cors import CORS

load_dotenv(find_dotenv())


class Server():

    mydb = connection.MySQLConnection(
        host= os.getenv("HOST"),
        user= os.getenv("USER"),
        password=os.getenv("PASSWORD"),
        database= os.getenv("DATABASE")
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