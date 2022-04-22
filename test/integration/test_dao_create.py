from unittest.mock import MagicMock, patch, call
import pytest
from backend.src.controllers.usercontroller import UserController


class TestDaoCreate:
    def test_valid_email_one_user_exist(self):
        fake_dao = MagicMock()
        fake_dao.find.return_value = [{'_id': {'$oid': '6259697356df8080e997364d'}, 'email': 'jim@gmail.com',
                                       'firstName': 'Jim', 'lastName': 'Ahlstrand'}]
        uc = UserController(fake_dao)
        valid_email = 'jim@gmail.com'

        assert len(uc.get_user_by_email(valid_email)) != 0
