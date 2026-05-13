import pytest
from unittest.mock import Mock 
from src.controllers.usercontroller import UserController

@pytest.fixture
def fake_dao():
    return Mock()

#valid test case: valid email, one user exists
def test_get_user_by_email_valid_email_one_user_exists(fake_dao): 
    user = {"email": "user@example.com", "user": "user1"}
    fake_dao.find.return_value = [user]

    controller = UserController(fake_dao)

    result = controller.get_user_by_email("user@example.com")

    assert result == user

#edge test case: valid email, multiple users exist
def test_get_user_by_email_valid_email_multiple_users_exist(fake_dao):
    user1 = {"email": "user@example.com", "user": "user1"}
    user2 = {"email": "user@example.com", "user": "user2"}
    fake_dao.find.return_value = [user1, user2]

    controller = UserController(fake_dao)

    result = controller.get_user_by_email("user@example.com")

    assert result == user1


#invalid test case: valid email, no user exists
def test_get_user_by_email_valid_email_no_user_exists(fake_dao):
    fake_dao.find.return_value = []

    controller = UserController(fake_dao)

    result = controller.get_user_by_email("user@example.com")

    assert result is None


#invalid test case: invalid email, missing @ symbol
def test_get_user_by_email_invalid_email_missing_at_symbl(fake_dao):
    controller = UserController(fake_dao)
    
    with pytest.raises(ValueError):
        controller.get_user_by_email("user.example.com")


#invalid test case: invalid email, missing host after dot
def test_get_user_by_email_invalid_email_missing_host_after_dot(fake_dao):
    controller = UserController(fake_dao)

    with pytest.raises(ValueError):
        controller.get_user_by_email("user@example.")


#invalid test case: database connection error
def test_get_user_by_email_database_error(fake_dao):
    fake_dao.find.side_effect = Exception("Database connection error")

    controller = UserController(fake_dao)

    with pytest.raises(Exception):
        controller.get_user_by_email("user@example.com")

