
from server.server import server
from routes import routes


routes.setRoutes()
server.app.run(host='0.0.0.0', port=8000)