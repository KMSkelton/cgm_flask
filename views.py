from .models import User, Device, Measurement
from .schema import UserSchema, DeviceSchema, MeasurementSchema
from .app import app
from flask import jsonify

user_schema = UserSchema()
users_schema = UserSchema(many=True)
device_schema = DeviceSchema()
devices_schema = DeviceSchema(many=True, only=('id', 'model', 'manufacturerID'))
measurement_schema = MeasurementSchema()
measurements_schema = MeasurementSchema(many=True, only=('id', 'meas_date', 'event_type', 'manufacturerID', 'gluc_value', 'insulin_value', 'carb'))

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

@app.route('/devices/', methods=['GET'])
def get_devices():
    devices = Device.query.all()
    devices_result = devices_schema.dump(devices)
    return jsonify({'devices': devices_result.data})

@app.route("/devices/<int:pk>")
def get_device(pk):
    try:
        device = Device.query.get(pk)
    except IntegrityError:
        return jsonify({"message": "Device could not be found."}), 400
    device_result = device_schema.dump(device)
    user_result = user_schema.dump(device.user)
    return jsonify({'device': device_result.data, 'users of this device': user_result})
