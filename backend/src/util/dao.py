# coding=utf-8
import os

import pymongo
from dotenv import dotenv_values

# create a data access object
from backend.src.util.validators import getValidator

import json
from bson import json_util
from bson.objectid import ObjectId


class DAO:

    def __init__(self, collection_name: str):
        # load the local mongo URL (something like mongodb://localhost:27017)
        LOCAL_MONGO_URL = dotenv_values('.env').get('MONGO_URL')
        # check out of the environment (which can be overridden by the docker-compose file) also specifies an URL, and use that instead if it exists
        MONGO_URL = os.environ.get('MONGO_URL', LOCAL_MONGO_URL)

        # connect to the MongoDB and select the appropriate database
        print(f'Connecting to collection {collection_name} on MongoDB at url {MONGO_URL}')
        client = pymongo.MongoClient(MONGO_URL)
        database = client.edutask

        validator = getValidator(collection_name)
        # create the collection if it does not yet exist
        if collection_name not in database.list_collection_names():
            database.create_collection(collection_name, validator=validator)

        self.collection = database[collection_name]

    # create a new entry
    def create(self, data):
        # preprocess the data: trim strings, make list items unique
        for key in data:
            if isinstance(data[key], str):
                data[key] = data[key].strip()
            if isinstance(data[key], list):
                data[key] = list(set(data[key]))

        # insert the object into the database
        try:
            inserted_id = self.collection.insert_one(data).inserted_id
        except Exception as e:
            raise

        # return the created object
        obj = self.collection.find_one({'_id': inserted_id})
        return self.to_json(obj)

    # find one specific object by id
    def findOne(self, id: str):
        try:
            obj = self.collection.find_one({'_id': ObjectId(id)})
            return self.to_json(obj)
        except Exception as e:
            raise

    # find all objects that comply to the optional filter
    def find(self, filter=None, toid: list = None):
        # if the filter contains attributes that are IDs, then they need to be converted
        if toid and len(toid) > 0:
            for i in toid:
                converted = []
                for element in filter[i]:
                    conv = ObjectId(element['$oid'])
                    converted.append(conv)
                filter[i] = {'$in': converted}

        objs = []
        try:
            dbobjs = self.collection.find(filter)

            for obj in dbobjs:
                objs.append(self.to_json(obj))

            return objs
        except Exception as e:
            raise

    # update an existing entry
    def update(self, id: str, update_data: dict):
        try:
            update_result = self.collection.update_one(
                {'_id': ObjectId(id)},
                update_data
            )
            return update_result.acknowledged
        except Exception as e:
            raise

    # delete an existing entry
    def delete(self, id: str):
        try:
            result = self.collection.delete_one(
                {'_id': ObjectId(id)}
            )
            return result.acknowledged
        except Exception as e:
            raise

    # transform an object into a json object
    def to_json(self, data):
        return json.loads(json_util.dumps(data))
