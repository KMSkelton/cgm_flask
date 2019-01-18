from flask import jsonify, request
from flask_restful import Resource, reqparse
from sqlalchemy.exc import IntegrityError

from models import db, Device, User
from schema import DeviceSchema, UserSchema

user_schema = UserSchema(strict=True)
users_schema = UserSchema(many = True, strict=True)
device_schema = DeviceSchema(strict=True)
devices_schema = DeviceSchema(many = True, only = ('id', 'model', 'manufacturerID'), strict=True)

parser = reqparse.RequestParser()
parser.add_argument('id')
parser.add_argument('user_id')
parser.add_argument('user_full_name')
parser.add_argument('username')
parser.add_argument('model', required=True)
parser.add_argument('manufacturerID', required=True)

class DeviceListResource(Resource):
    def get(self):
        devices = Device.query.all()
        devices_result = devices_schema.dump(devices)
        return jsonify({'devices': devices_result.data})

    def post(self):
        print("DeviceListPost", self)
        json_data = parser.parse_args()
        if not json_data:
            return jsonify({"message": "No input provided"}), 400
        print(json_data)
        # Validate then deserialize input
        user_id = json_data['user_id']
        print(user_id)
        user = User.query.filter_by(id = user_id).first()
        print(user)
        if user is None:
            if not json_data['user_full_name'] or not json_data['username']:
                return jsonify({'error': 'can\'t create user without "user_full_name" and "username"'})
            # create new user
            user_full_name, username = json_data['user_full_name'], json_data['username']
            user = User(name = user_full_name, username = username)
            # does Flask automagically add a user.id to the user object?
            db.session.add(user)
            db.session.commit()
        # check to see if device is already in db
        model, manufacturerID = json_data['model'], json_data['manufacturerID']
        print(model, manufacturerID)
        device = Device.query.filter_by(id=json_data['id']).first()
        if device:
            return jsonify({'error': 'device already exists', 'data': device_schema.dump(device)})
        device = Device.query.filter_by(model = model, manufacturerID = manufacturerID, user_id = user.id).first()
        if device:
            return jsonify({'error': 'device already exists', 'data': device_schema.dump(device)})

        # How to manually create a device:
        # device = Device(
        #     'model' = model,
        #     'manufacturerID' = manufacturerID,
        #     'user_id' = user.id
        # )
        try:
            device, errors = device_schema.load(json_data)
        except Exception as e:
            print("Excpetio", e)
            return jsonify(e), 422
        if errors:
            print("ERRORS", errors)
            return jsonify(errors), 422

        print("device", device)
        if device.user_id is None:
            device.user_id = user.id
            print("added user", device)
        db.session.add(device)
        db.session.commit()
        deviceAddResult = device_schema.dump(Device.query.get(device.id))
        return jsonify({"message": "New device created", "data": {"device: ": deviceAddResult.data }})

class DeviceResource(Resource):
    def get(self, id):
        try:
            device = Device.query.get(id)
        except IntegrityError:
            return jsonify({"message": "Device could not be found."}), 400
        device_result = device_schema.dump(device)
        user_result = user_schema.dump(device.user)
        return jsonify({'data': { 'device': device_result.data, 'users of this device': user_result}})
