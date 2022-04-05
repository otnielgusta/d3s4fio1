import pytest
from server.server import server
from routes import routes

@pytest.fixture(scope="module")
def app():
    app = server.app
    routes.setRoutes()
    return app

@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()