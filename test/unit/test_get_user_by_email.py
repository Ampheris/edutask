from unittest.mock import MagicMock, patch, call
import pytest
from backend.src.controllers.usercontroller import UserController


class TestGetUserByEmail:
    def test_valid_email_one_user_exist(self):
        fake_dao = MagicMock()
        fake_dao.find.return_value = [{'_id': {'$oid': '6259697356df8080e997364d'}, 'email': 'jim@gmail.com',
                                       'firstName': 'Jim', 'lastName': 'Ahlstrand'}]
        uc = UserController(fake_dao)
        valid_email = 'jim@gmail.com'

        assert len(uc.get_user_by_email(valid_email)) != 0

    @patch('builtins.print')
    def test_valid_email_many_user_exist(self, mock_print):
        fake_dao = MagicMock()
        fake_dao.find.return_value = [{'_id': {'$oid': '6259697356df8080e997364d'}, 'email': 'jim@gmail.com',
                                       'firstName': 'Jim', 'lastName': 'Ahlstrand'},
                                      {'_id': {'$oid': '625969d956df8080e997364e'}, 'email': 'jim@gmail.com',
                                       'firstName': 'Therese', 'lastName': 'Bergöö'}]
        uc = UserController(fake_dao)
        valid_email = 'jim@email.com'
        returned_user = {'_id': {'$oid': '6259697356df8080e997364d'}, 'email': 'jim@gmail.com',
                         'firstName': 'Jim', 'lastName': 'Ahlstrand'}
        uc.get_user_by_email(valid_email)
        mock_print.assert_called()

        assert uc.get_user_by_email(email=valid_email) == returned_user

    def test_valid_email_user_not_exist(self):
        fake_dao = MagicMock()
        fake_dao.find.return_value = {'users': []}
        uc = UserController(fake_dao)

        valid_email = 'valid@email.com'

        # Should return none but raises error
        assert uc.get_user_by_email(email=valid_email) is None

        # with pytest.raises(Exception):
        #     uc.get_user_by_email(email=valid_email)

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

