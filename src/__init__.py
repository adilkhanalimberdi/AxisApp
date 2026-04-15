from flask import Flask
from src.config import Config

def create_app():
    app = Flask(
        __name__,
        template_folder=Config.TEMPLATE_FOLDER,
        static_folder=Config.STATIC_FOLDER,
    )

    from src.routes.main_routes import bp
    app.register_blueprint(bp)

    return app