from server.server import server

from controllers.usuario_controller import usuarioController
app = server.app

class Routes():
    
    def setRoutes(self):
        server.app.add_url_rule('/auth/login','login', usuarioController.login, methods=['POST'])
        server.app.add_url_rule('/auth/register', 'register', usuarioController.register, methods=['POST'])
        server.app.add_url_rule('/home', 'home', usuarioController.getUser, methods=['GET'])
        server.app.add_url_rule('/auth/auth', 'auth', usuarioController.getAutheticate, methods=['GET'])


routes = Routes()
