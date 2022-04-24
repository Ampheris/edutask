from unittest.mock import MagicMock, patch, call
import pytest
from backend.src.util.dao import DAO
from backend.src.controllers.usercontroller import UserController

"""     
Creates a new document in the collection associated to this data access object. The creation of a new
document must comply to the corresponding validator, which defines the data structure of the collection.
In particular, the validator has to make sure that:

        (1) the data for the new object contains all required properties,
        
        (2) every property complies to the bson data type constraint (see
        https://www.mongodb.com/docs/manual/reference/bson-types/, though we currently only consider Strings and
        Booleans),
        
        (3) and the values of a property flagged with 'uniqueItems' are unique among all
        documents of the collection.

        parameters:
            data -- a dict containing key-value pairs compliant to the validator

        returns:
            object -- the newly created MongoDB document (parsed to a JSON object) containing the input data and an _id 
            attribute

        raises:
            WriteError - in case at least one of the validator criteria is violated
            
        
"""


@pytest.fixture
def dao():
    return DAO('user')


@pytest.fixture
def adding_valid_user(dao):
    user = dao.create({'email': 'lbg@telia.com', 'firstName': 'Linnea', 'lastName': 'B'})
    yield user
    dao.delete(user['_id']['$oid'])


# Only testing the validation for users.
class TestDaoCreate:
    # the values of a property flagged with 'uniqueItems' are unique among all documents of the collection.
    def test_string_uniqueItem_false(self):
        # uniqueItem is for the tasks only since its the only array in the list.
        dao_user = DAO('user')
        tasks_not_unique = {'id': '625969d956df8080e997398e', 'email': "john.doe@test.com", 'firstName': "John",
                            'lastName': 'Johnsson', 'tasks': [1, 2, 2]}
        tasks_not_unique_two = {'id': '625969d956df8080e997398e', 'email': "john.doe@test.com", 'firstName': "John",
                                'lastName': 'Johnsson', 'tasks': ['test', 'test', 'hello']}

        with pytest.raises(Exception):
            dao_user.create(tasks_not_unique)

        with pytest.raises(Exception):
            dao_user.create(tasks_not_unique_two)

    # (2) every property complies to the bson data type constraint
    def test_firstname_not_comply(self):
        pass

    def test_lastname_not_comply(self):
        pass

    def test_email_not_comply(self):
        pass

    def test_tasks_not_comply(self):
        pass

    # (1) the data for the new object contains all required properties
    def test_does_not_have_all_required_properties(self):
        pass

    # Returns object, all 1-3 are good.
    def test_data_string_uniqueItems_true_all_props_true(self, adding_valid_user, dao):
        user = adding_valid_user

        assert dao.findOne(user['_id']['$oid']) == user
