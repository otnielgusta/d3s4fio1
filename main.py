
from server.server import server
from routes import routes


routes.setRoutes()
server.app.run()