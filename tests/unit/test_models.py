def test_new_user(new_user):
  assert new_user.id == '0042'
  assert new_user.name == 'Ford Prefect'
  assert not new_user.name == 'Ford Fairlane'
  