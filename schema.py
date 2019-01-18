from marshmallow import post_load
from marshmallow_sqlalchemy import field_for
from models import ma, User, Device, Measurement

class UserSchema(ma.Schema):
    id = field_for(User, 'id', dump_only=True)

    class Meta:
        # Fields to expose
        fields = ('id', 'name', 'username')
        model = User

    @post_load
    def make_user(self, data):
        return User(**data)

class DeviceSchema(ma.Schema):
    id = field_for(Device, 'id', dump_only=True)

    class Meta:
        # Fields to expose
        fields = ('id', 'model', 'manufacturerID')

        model = Device

    @post_load
    def make_device(self, data):
        return Device(**data)

class MeasurementSchema(ma.Schema):
    id = field_for(Measurement, 'id', dump_only=True)

    class Meta:
        # Fields to expose
        model = Measurement

    @post_load
    def make_measurement(self, data):
        return Measurement(**data)
