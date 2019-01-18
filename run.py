import os
basedir = os.path.abspath(os.path.dirname(__file__))
import sys
sys.path.append(basedir)

from flask import Flask
from flask_migrate import Migrate

def create_app(config_filename="config"):
    print("sys path", sys.path)
    migrate = Migrate()
    app = Flask(__name__)
    app.config.from_object(config_filename)
    from app import api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    from models import db, ma
    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)

    return app


if __name__ == "__main__":
    app = create_app("config")
    app.run(debug=True)
