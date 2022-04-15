from unittest.mock import MagicMock

import pytest

from backend.src.controllers.usercontroller import UserController
from backend.src.util.dao import DAO


class MockUser:
    pass


class TestGetUserByEmail:
    def test_valid_email_user_exist(self, mock_find):
        fake_dao = MagicMock()
        fake_dao.find
        uc = UserController()
        valid_email = ''
        pass

    def test_valid_email_user_not_exist(self):
        pass

    def test_invalid_email(self):
        uc = UserController(MagicMock())
        invalid_email = 'test.com'
        invalid_email2 = 'test@test'

        with pytest.raises(ValueError):
            uc.get_user_by_email(email=invalid_email)

        # Should work, the regex is horrible so it just checks for something@something,
        # not <local-part>@<domain>.<host>
        with pytest.raises(ValueError):
            uc.get_user_by_email(email=invalid_email2)
