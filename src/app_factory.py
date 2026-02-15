from flask import Flask
from src.routes.static_routes import register_static_routes
from src.routes.function_routes import register_function_routes
from src.routes.community_routes import register_community_routes
from src.routes.lists_routes import register_list_routes

def create_app():
    app = Flask(
        __name__, static_folder="../static",
        template_folder="../templates"
    )

    with open("secret.key", "rb") as key_file:
        key = key_file.read()

    app.secret_key = key
    app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024

    register_static_routes(app)
    register_function_routes(app)
    register_community_routes(app)
    register_list_routes(app)

    return app
