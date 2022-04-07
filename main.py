
import os
from server.server import server
from routes import routes


routes.setRoutes()
port = int(os.environ.get("PORT", 5000))  

server.app.run(host='0.0.0.0', port=port)