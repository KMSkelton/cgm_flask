Installation and Run
in terminal:

$pip3 install -r requirements.txt


Starting App:
$export FLASK_APP=app.py
$flask run

Viewing output: localhost:5000/devices/  may need 127.0.0.1:5000/devices/

To view the SQL databases:
$mySQL -u USER -p [return]
$[key symbol] type PW [return]
$show databases;

Example POST route:
http POST :5000/devices/ id=13 model=notTotesFake manufacturerID=3030XYZ user_id=1

  yields:
    HTTP/1.0 200 OK
    Content-Length: 153
    Content-Type: application/json
    Date: Tue, 05 Sep 2017 05:29:30 GMT
    Server: Werkzeug/0.12.2 Python/3.6.1

    {
        "Device: ": {
            "id": 13,
            "manufacturerID": "3030XYZ",
            "model": "notTotesFake",
            "user": 1
        },
        "message": "New device created"
    }


To migrate data (update db). We are using flask-migrate to manage the
database. flask-migrate will create a table named "alembic_version" in the database.
$flask db migrate 
    ( Only compares
    models.py to the database state. Then it writes a file that 
    tells the db how to go from current state to the state we want. 
    It stores the file name in the alembic_versions table in the db. 
    It DOES create a new file in migrations/versions.)
$flask db upgrade (up-grades the db to have the useful stuff)



11/19/17 - set up Vue front end
8/9/17 - add measurements (fix create_meas_record). Pass device_id and userRecord_id into measurements
8/6/17 - add user_id to the deviceRecord
