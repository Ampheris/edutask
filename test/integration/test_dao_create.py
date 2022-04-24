from unittest.mock import MagicMock, patch, call
import pytest
from backend.src.controllers.usercontroller import UserController


class TestDaoCreate:
    def test_string_uniqueItem_false(self):
        # uniqueItem is for the tasks only since its the only array in the list.
        dao_user = DAO('user')
        user_not_unique = {'id': '625969d956df8080e997398e', 'email': "john.doe@test.com", 'firstName': "John",
                           'lastName': 'Johnsson', 'tasks': [1, 2, 2]}

        with pytest.raises(Exception):
            dao_user.create(user_not_unique)

    def test_string_uniqueItem_true(self):
        pass

    def test_boolean_uniqueItem_false(self):
        pass

    def test_boolean_uniqueItem_true(self):
        pass

    # Returns object
    def test_data_string_uniqueItems_true_all_props_true(self):
        pass

    def test_data_boolean_uniqueItems_true_all_props_true(self):
        pass

    # Should fail
    def test_data_string_uniqueItems_false_all_props_true(self):
        pass

    def test_data_string_uniqueItems_true_all_props_false(self):
        pass
