from models import User, Device, Measurement


def test_new_user():
  """
  GIVEN a User model
  WHEN a new User is created
  THEN check the username and name fields are correct
  """
  new_user = User('Test User', 'testuser')
  assert new_user.username == 'testuser'
  assert new_user.name == 'Test User'
  assert not new_user.name == 'Sooper User'

def test_new_device():
  new_device = Device('0042', 'Very Real Device', 'LowestBidderDevices')
  assert new_device.id == '0042'
  assert new_device.model == 'Very Real Device'
  assert not new_device.model == 'Contrived Device for Pytest'
  assert new_device.manufacturerID == 'LowestBidderDevices'

def test_new_measurement():
  new_measurement = Measurement(1, '001100', 'a', 'manu12', 110, 111, 101.00)
  assert new_measurement.id == 1
  assert new_measurement.meas_date == '001100'
  assert new_measurement.event_type == 'a'
  assert new_measurement.manufacturerID == 'manu12'
  assert new_measurement.gluc_value == 110
  assert new_measurement.insulin_value == 111
  assert new_measurement.carb == 101.00
  assert not new_measurement.carb == 86753.29
