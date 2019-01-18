import sys
sys.path.append("../")

from cgmFlask.models import User, Device, Measurement
from cgmFlask.app import ma

class UserSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('id', 'name', 'username')
        model = User

class DeviceSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('id', 'model', 'manufacturerID')

        model = Device

class MeasurementSchema(ma.Schema):
    class Meta:
        # Fields to expose
        model = Measurement
