import sys
sys.path.append(".")

from flask import Flask, jsonify
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from spinupSQLAlchemy import db

app = Flask(__name__)
application = app

#TODO update config to env vars for prod
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://sooperAdmin:I<3lambKebabs@localhost/cgmviz'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://sooperAdmin:l4mbk3b4bs@cgmflask.ctkfpndtiwzr.us-west-2.rds.amazonaws.com/cgmviz'

# Order matters - initialize SQLAlchemy before Marshmallow
ma = Marshmallow(app)
migrate = Migrate(app, db)

from views import *
db.init_app(app)

if __name__ == "__main__":
    app.run(debug=True)
