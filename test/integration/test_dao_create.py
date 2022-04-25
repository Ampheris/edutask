import json
import os
from unittest.mock import patch, MagicMock
import pytest
from backend.src.util.dao import DAO
from backend.src.util.validators import getValidator

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
def sut():
    fabricated_filename = 'C:\\Users\\mathi\\Documents\\edutask\\backend\src\static\\validators\\test.json'
    fabricated_data = {
        "$jsonSchema": {
            "bsonType": "object",
            "required": ["firstName", "lastName", "email"],
            "properties": {
                "firstName": {
                    "bsonType": "string",
                    "description": "the first name of a user must be determined"
                },
                "lastName": {
                    "bsonType": "string",
                    "description": "the last name of a user must be determined"
                },
                "email": {
                    "bsonType": "string",
                    "description": "the email address of a user must be determined"
                },
                "tasks": {
                    "bsonType": "array",
                    "uniqueItems": True,
                    "items": {
                        "bsonType": "objectId"
                    }
                }
            }
        }
    }

    with open(fabricated_filename, 'w') as output_file:
        json.dump(fabricated_data, output_file)

    dao = DAO('test')
    yield dao
    dao.drop()
    os.remove(fabricated_filename)


# Only testing the validation for users.
class TestDaoCreate:
    # the values of a property flagged with 'uniqueItems' are unique among all documents of the collection.
    def test_string_uniqueItem_false(self, sut):
        # uniqueItem is for the tasks only since its the only array in the list.
        tasks_not_unique = {'id': '625969d956df8080e997398e', 'email': "john.doe@test.com", 'firstName': "John",
                            'lastName': 'Johnsson', 'tasks': [1, 2, 2]}
        tasks_not_unique_two = {'id': '625969d956df8080e997398e', 'email': "john.doe@test.com", 'firstName': "John",
                                'lastName': 'Johnsson', 'tasks': ['test', 'test', 'hello']}

        with pytest.raises(Exception):
            sut.create(tasks_not_unique)

        with pytest.raises(Exception):
            sut.create(tasks_not_unique_two)

    # (2) every property complies to the bson data type constraint
    def test_firstname_not_comply(self, sut):
        invalid_firstname_num = {'email': "john.doe@test.com", 'firstName': 123, 'lastName': 'Doe'}
        invalid_firstname_bool = {'email': "john.doe@test.com", 'firstName': False, 'lastName': 'Doe'}
        invalid_firstname_array = {'email': "john.doe@test.com", 'firstName': [1, 2, 3], 'lastName': 'Doe'}

        with pytest.raises(Exception):
            sut.create(invalid_firstname_num)

        with pytest.raises(Exception):
            sut.create(invalid_firstname_bool)

        with pytest.raises(Exception):
            sut.create(invalid_firstname_array)

    def test_lastname_not_comply(self, sut):
        invalid_lastname_num = {'email': "john.doe@test.com", 'firstName': 'Jane', 'lastName': 123}
        invalid_lastname_bool = {'email': "john.doe@test.com", 'firstName': 'Jane', 'lastName': True}
        invalid_lastname_array = {'email': "john.doe@test.com", 'firstName': 'Jane', 'lastName': [1, 2, 3]}

        with pytest.raises(Exception):
            sut.create(invalid_lastname_num)

        with pytest.raises(Exception):
            sut.create(invalid_lastname_bool)

        with pytest.raises(Exception):
            sut.create(invalid_lastname_array)

    def test_email_not_comply(self, sut):
        invalid_email_num = {'email': 123, 'firstName': 'Jane', 'lastName': 'Doe'}
        invalid_email_bool = {'email': False, 'firstName': 'Jane', 'lastName': 'Doe'}
        invalid_email_array = {'email': [1, 2, 3], 'firstName': 'Jane', 'lastName': 'Doe'}

        with pytest.raises(Exception):
            sut.create(invalid_email_num)

        with pytest.raises(Exception):
            sut.create(invalid_email_bool)

        with pytest.raises(Exception):
            sut.create(invalid_email_array)

    def test_tasks_not_comply(self, sut):
        pass

    # (1) the data for the new object contains all required properties
    def test_does_not_have_all_required_properties(self, sut):
        no_lastname = {'email': 'test@test.com', 'firstName': 'Jane'}
        no_firstname = {'email': 'test@test.com', 'lastName': 'Doe'}
        no_email = {'firstName': 'Jane', 'lastName': 'Doe'}

        with pytest.raises(Exception):
            sut.create(no_lastname)

        with pytest.raises(Exception):
            sut.create(no_firstname)

        with pytest.raises(Exception):
            sut.create(no_email)

    # Returns object, all 1-3 conditions are good.
    def test_data_string_uniqueItems_true_all_props_true(self, sut):
        user_data = {'email': 'lbg@telia.com', 'firstName': 'Linnea', 'lastName': 'B'}
        user = sut.create(user_data)

        assert sut.findOne(user['_id']['$oid'])['email'] == user_data['email']
        assert sut.findOne(user['_id']['$oid'])['firstName'] == user_data['firstName']
        assert sut.findOne(user['_id']['$oid'])['lastName'] == user_data['lastName']
