# cgm_flask

Installation and Run
in terminal:

`$ pip3 install -r requirements.txt`

Requires cgm_flask directory in PYTHONPATH

in terminal in cgm_flask directory:

`$ export PYTHONPATH=$PWD`

Starting App:

`$ export FLASK_APP=run.py`

`$ flask run`

Viewing output: localhost:5000/api/devices

To view the SQL databases:

`$mySQL -u USER -p [return]
$[key symbol] type PW [return]
$show databases`

Example POST route:

`$ http POST :5000/api/devices model=notTotesFake manufacturerID=3030XYZ user_id=1`

  yields:
    HTTP/1.0 200 OK
    Content-Length: 153
    Content-Type: application/json
    Date: Tue, 05 Sep 2017 05:29:30 GMT
    Server: Werkzeug/0.12.2 Python/3.6.1

    {
        "data": {
            "device: ": {
                "id": 3,
                "manufacturerID": "3030XYZ",
                "model": "notTotesFake"
            }
        },
        "message": "New device created"
    }


To migrate data (update db). We are using flask-migrate to manage the
database. flask-migrate will create a table named "alembic_version" in your database.

`$ flask db migrate` (does nothing useful after the first use. It compares the models.py to the database state. Then it writes a file that tells the db how to go from current state to the state we want. It stores the file name in the alembic_versions table in the db. It DOES create a new file in migrations/versions.)

`$ flask db upgrade` (up-grades the db to have the useful stuff)

TESTS!!

remove any __pycache__ files from /test to ensure that
previous tests do not give false positive/negative

`$ export PYTHONPATH=$PWD`

`pytest`
