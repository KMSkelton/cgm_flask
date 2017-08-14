import sys
sys.path.append("../")

from flask import Flask, jsonify
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://sooperAdmin:I<3lambKebabs@localhost/cgmviz'

# Order matters - initialize SQLAlchemy before Marshmallow
db = SQLAlchemy(app)
ma = Marshmallow(app)

from . import views

if __name__ == "__main__":
    app.run(debug=true, port=5000)
