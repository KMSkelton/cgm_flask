import sys
sys.path.append("../")

from cgmFlask.models import User, Device, Measurement
from cgmFlask.app import ma

class UserSchema(ma.ModelSchema):
    class Meta:
        # Fields to expose
        model = User

class DeviceSchema(ma.ModelSchema):
    class Meta:
        # Fields to expose
        model = Device

class MeasurementSchema(ma.ModelSchema):
    class Meta:
        # Fields to expose
        model = Measurement
