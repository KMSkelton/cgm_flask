import sys
sys.path.append("../")

from models import User, Device, Measurement
from app import ma

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
