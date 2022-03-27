import datetime
import os
from functools import wraps
from flask import request, jsonify

import jwt

class Authenticate:
    def verifyAndDecodToken(self,token) -> dict:
        try:
            tokenDecoded = jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=os.getenv("ALGORITHM"))
        except jwt.exceptions.ExpiredSignatureError:
            return {"status":"403","error":"Token expirado"}
        except:
            return {"status":"401","error":"Acesso negado"}
        
        return {
            "status":"200",
            "id": tokenDecoded['id']
        }
