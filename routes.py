from server.server import server

from controllers.usuario_controller import UsuarioController

class Routes():
    def setRoutes(self):
        server.api.add_resource(UsuarioController, '/usuario')

routes = Routes()
