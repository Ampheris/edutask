from unittest.mock import MagicMock, patch, call
import pytest
from backend.src.util.dao import DAO

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
