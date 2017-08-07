Installation and Run
in terminal:

$conda create --name cgm_flask python=3

$source activate cgm_flask

$pip install -r requirements.txt


Starting App:
$export FLASK_APP=app.py
$flask run

Viewing output: localhost:9090/v1.0/items

To view the SQL databases:
$mySQL -u USER -p [return]
$[key symbol] type PW [return]
$show databases


To migrate data (update db). We are using flask-migrate to manage the
database. flask-migrate will create a table named "alembic_version" in your database.
$flask db migrate (which does nothing useful. Denise says it compares the models.py to the database state. Then it writes a file that tells the db how to go from current state to the state we want. It stores the file name in the alembic_versions table in the db. It DOES create a new file in migrations/versions.)
$flask db upgrade (up-grades the db to have the useful stuff)



8/6/17 - next: add user_id to the deviceRecord
