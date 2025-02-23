import pytest
from Python.User import User

def test_user_creation():
    test_user = "Alice"
    test_password = "password"
    test_email = "alice@mail.com"

    user = User(test_user,test_password,test_email)
    assert user.username == test_user
    assert user.password_hash == test_password
    assert user.email == test_email