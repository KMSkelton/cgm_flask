import sys
sys.path.append("../")

from flask import Flask, jsonify
from flask.ext.sqlalchemy import SQLAlchemy
#not sure IntegrityError is actually being imported
from sqlalchemy.exc import IntegrityError
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow

global db, ma, app

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://sooperAdmin:I<3lambKebabs@localhost/cgmviz'

# Order matters - initialize SQLAlchemy before Marshmallow
db = SQLAlchemy(app)
ma = Marshmallow(app)

import cgmFlask.views

if __name__ == "__main__":
    app.run(debug=True, port=5000)
