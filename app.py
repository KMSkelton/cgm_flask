import sys
sys.path.append(".")
import os
databaseURL = os.environ['DATABASE_URI']

from flask import Flask, jsonify
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from spinupSQLAlchemy import db

app = Flask(__name__)
application = app

#requires mySQL connection string
# mysql://<user>:<pass>@<URL>/<databaseName>
app.config['SQLALCHEMY_DATABASE_URI'] = databaseURL

# Order matters - initialize SQLAlchemy before Marshmallow
ma = Marshmallow(app)
migrate = Migrate(app, db)

from views import *
db.init_app(app)

if __name__ == "__main__":
    app.run(debug=True)
