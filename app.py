from flask import Blueprint
from flask_restful import Api
from resources.users import UserResource, UserListResource
from resources.devices import DeviceResource, DeviceListResource

api_bp = Blueprint('api', __name__)
api = Api(api_bp)

api.add_resource(UserResource, '/users/<int:id>', endpoint="user")
api.add_resource(UserListResource, '/users', endpoint="users")

api.add_resource(DeviceResource, '/devices/<int:id>', endpoint="device")
api.add_resource(DeviceListResource, '/devices', endpoint="devices")