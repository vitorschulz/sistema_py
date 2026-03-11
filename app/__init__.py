from flask import Flask

def create_app():
    app = Flask(__name__)

    from app.routes.main_routes import main
    app.register_blueprint(main)

    from app.routes.clientes_routes import clientes
    app.register_blueprint(clientes)

    from app.routes.shopping_routes import shopping
    app.register_blueprint(shopping)

    return app