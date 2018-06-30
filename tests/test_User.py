import unittest
from bson.objectid import ObjectId
from resource.model.User import UserModel
from tests.api.google.test_credentials import CredentialsMock
from resource.api.google.credentials import credentials_to_dict
from copy import deepcopy


class TestUserModel(unittest.TestCase):
    def setUp(self):
        self.userModel = UserModel()

    def test_insert_user(self):
        credentials = CredentialsMock()
        credentials_dict = credentials_to_dict(credentials)
        credentials_dict_copy = deepcopy(credentials_dict)

        insert = self.userModel.insertUser(credentials_dict)
        self.assertTrue(insert.acknowledged)

        objectid = ObjectId(insert.inserted_id)
        get_user = self.userModel.getUser(objectid)

        del get_user['_id']

        self.assertDictEqual(credentials_dict_copy, get_user)

    def test_update_password(self):
        hash_password = 'aabbcc'

        credentials = CredentialsMock()
        credentials_dict = credentials_to_dict(credentials)

        insert = self.userModel.insertUser(credentials_dict)
        objectid = insert.inserted_id

        self.userModel.updatePassword(objectid, hash_password)

        get_user = self.userModel.getUser(objectid)

        self.assertEqual(hash_password, get_user['hash_password'])


