import sys
sys.path.append("../")

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://sooperAdmin:I<3lambKebabs@localhost/cgmviz'

db = SQLAlchemy(app)
migrate = Migrate(app, db)
import cgmFlask.models
