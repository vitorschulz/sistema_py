from flask import Flask

def create_app():
    app = Flask(__name__)

    app.secret_key = "mae123"

    from app.routes.main_routes import main
    app.register_blueprint(main)

    from app.routes.clientes_routes import clientes
    app.register_blueprint(clientes)

    from app.routes.shopping_routes import shopping
    app.register_blueprint(shopping)

    from app.routes.lojas_routes import lojas
    app.register_blueprint(lojas)

    from app.routes.viagens_routes import viagens
    app.register_blueprint(viagens)

    from app.routes.pedidos_routes import pedidos
    app.register_blueprint(pedidos)

    from app.routes.cheques_routes import cheques
    app.register_blueprint(cheques)

    from app.routes.financeiro_routes import financeiro
    app.register_blueprint(financeiro)

    return app