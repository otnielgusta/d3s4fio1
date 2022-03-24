import datetime
import os
from functools import wraps
from flask import request, jsonify

import jwt

class Authenticate:
    def verifyAndDecodToken(self,token):
        try:
            tokenDecoded = jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=os.getenv("ALGORITHM"))
        except jwt.exceptions.ExpiredSignatureError:
            return jsonify({"error":"Token expirado"}), 401
        except:
            return jsonify({"error":"Acesso negado"}), 401
        
        return {
            "ok"
        }   
