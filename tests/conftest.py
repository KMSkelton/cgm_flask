import pytest
from ...models import User

@pytest.fixture(scope="module")
def new_user():
  user = User('0042', 'Ford Prefect', 'Ix')
  return user