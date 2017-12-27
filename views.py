import sys
sys.path.append(".")

from datetime import datetime
from models import User, Device, Measurement
from schema import UserSchema, DeviceSchema, MeasurementSchema
from app import *
from spinupSQLAlchemy import db
from flask import jsonify, request

user_schema = UserSchema()
users_schema = UserSchema(many = True)
device_schema = DeviceSchema()
devices_schema = DeviceSchema(many = True, only = ('id', 'model', 'manufacturerID'))
measurement_schema = MeasurementSchema()
measurements_schema = MeasurementSchema(many = True, only = ('id', 'meas_date', 'event_type', 'manufacturerID', 'gluc_value', 'insulin_value', 'carb'))

#### API #####
@app.route('/users')
def get_users():
    users = User.query.all()
    #Serialize the query
    users_result = users_schema.dump(users)
    return jsonify({'users': users_result.data})

@app.route('/users/<int:pk>')
def get_author(pk):
    try:
        user = User.query.get(pk)
    except IntegrityError:
        return jsonify({"message": "User could not be found."}), 400
    user_result = user_schema.dump(user)
    devices_result = devices_schema.dump(user.devices.all())
    return jsonify({'user': user_result.data, 'devices with key': devices_result.data})

@app.route('/devices/', methods = ['GET'])
def get_devices():
    devices = Device.query.all()
    devices_result = devices_schema.dump(devices)
    return jsonify({'devices': devices_result.data})

@app.route('/devices/<int:pk>')
def get_device(pk):
    try:
        device = Device.query.get(pk)
    except IntegrityError:
        return jsonify({"message": "Device could not be found."}), 400
    device_result = device_schema.dump(device)
    user_result = user_schema.dump(device.user)
    return jsonify({'device': device_result.data, 'users of this device': user_result})

@app.route('/devices/', methods = ['POST'])
def new_device():
    json_data = request.get_json()
    if not json_data:
        return jsonify({"message": "No input provided"}), 400
    # Validate then deserialize input
    user_id = json_data['user_id']
    print(user_id)
    user = User.query.filter_by(id = user_id).first()
    print(user)
    if user is None:
        if not json_data['user_full_name'] or not json_data['username']:
            return jsonify({"error": "can't create user without 'user_full_name' and 'username'"})
        # create new user
        user_full_name, username = json_data['user_full_name'], json_data['username']
        user = User(name = user_full_name, username = username)
        # does Flask automagically add a user.id to the user object?
        db.session.add(user)
        db.session.commit()
    # check to see if device is already in db
    model, manufacturerID = json_data['model'], json_data['manufacturerID']
    device = Device.query.filter_by(model = model, manufacturerID = manufacturerID, user_id = user.id).first()
    if device:
        return jsonify({'error': 'device already exists'})
    device, errors = device_schema.load(json_data)
    if errors:
        return jsonify(errors), 422
    if device.user_id is None:
        device.user_id = user.id
    db.session.add(device)
    db.session.commit()
    deviceAddResult = device_schema.dump(Device.query.get(device.id))
    return jsonify({"message": "New device created", "Device: ": deviceAddResult.data })

@app.route('/measurements/', methods = ['GET'])
def get_measurements():
    measurements = Measurement.query.all()
    measurements_result = measurements_schema.dump(measurements)
    return jsonify({'measurements': measurements_result.data})

@app.route('/measurements/<int:pk>')
def get_measurment(pk):
    try:
        measurement = Measurement.query.get(pk)
    except IntegrityError:
        return jsonify({"message": "Measurement could not be found."}), 400
    measurement_result = measurement_schema.dump(measurement)
    device_result = device_schema.dump(measurement.device)
    user_result = user_schema.dump(measurement.user)
    return jsonify({'measurement': measurement_result.data, "device this measurement was taken from: ": device_result, "device and user profile: ": user_result})

@app.route('/measurements/', methods = ['POST'])
def new_measurement():
    # measurement requires existing user and device IDs
    # will neither look up nor create either ID
    json_data = request.get_json()
    if not json_data:
        return jsonify({'message': "No input provided" }), 400
    if not 'user_id' in json_data or not 'manufacturerID' in json_data:
        return jsonify({"message: " : "Missing user or manufacturer id"}), 400
    check_user_id = json_data['user_id']
    valid_user = User.query.filter_by(id = check_user_id).first()
    if valid_user is None:
        return jsonify({"message: " : "User is not in database."})
    device_manufacturerID = json_data['manufacturerID']
    valid_device = Device.query.filter_by(manufacturerID = device_manufacturerID).first()
    if valid_device is None:
        return jsonify({"message: " : "Device is not in database."})

    json_data['meas_date'] = str(datetime.strptime(json_data['meas_date'], '%Y-%m-%d'))
    measurement, errors = measurement_schema.load(json_data)
    if errors:
        return jsonify(errors), 422
    measurement.device_id = valid_device.id
    measurement.user_id = valid_user.id
    db.session.add(measurement)
    db.session.commit()
    measurementAddResult = measurement_schema.dump(Measurement.query.get(measurement.id))
    return jsonify({"message": "New measurement added", "Measurement info: ": measurementAddResult.data })
