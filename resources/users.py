from flask import jsonify, request, Response
from flask_restful import Resource, reqparse
from sqlalchemy.exc import IntegrityError

from models import Device, Measurement, User
from schema import UserSchema, DeviceSchema, MeasurementSchema

user_schema = UserSchema(strict=True)
users_schema = UserSchema(many = True, strict=True)
device_schema = DeviceSchema()
devices_schema = DeviceSchema(many = True, only = ('id', 'model', 'manufacturerID'))
measurement_schema = MeasurementSchema()
measurements_schema = MeasurementSchema(many = True, only = ('id', 'meas_date', 'event_type', 'manufacturerID', 'gluc_value', 'insulin_value', 'carb'))


class UserListResource(Resource):
    def get(self):
        users = User.query.all()
        users_result = users_schema.dump(users)
        return jsonify({'users': users_result.data})

class UserResource(Resource):
    def not_found_response(self):
        not_found_response = jsonify({"message": "User could not be found."})
        not_found_response.status_code = 400
        return not_found_response

    def get(self, id):
        try:
            user = User.query.get(id)
        except IntegrityError:
            return self.not_found_response()
        if user is None:
            return self.not_found_response()
        print("user", user)
        user_result = user_schema.dump(user)
        devices_result = devices_schema.dump(user.devices.all())
        return jsonify({'user': user_result.data, 'devices with key': devices_result.data})

