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
application = app
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://sooperAdmin:I<3lambKebabs@localhost/cgmviz'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://sooperAdmin:l4mbk3b4bs@cgmflask.ctkfpndtiwzr.us-west-2.rds.amazonaws.com/cgmviz'

# Order matters - initialize SQLAlchemy before Marshmallow
db = SQLAlchemy(app)
ma = Marshmallow(app)
migrate = Migrate(app, db)

import views
# import views

if __name__ == "__main__":
    app.run(debug=True)
