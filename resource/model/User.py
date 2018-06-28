from .Model import Model


class UserModel(Model):
    def insertUser(self, account):
        inserted_user = self.db.users.insert_one(account)

        return inserted_user

    def getUser(self, object_id):
        get_user = self.db.users.find_one({
            '_id': object_id
        })

        return get_user

    def updatePassword(self, object_id, hash_password):
        update_password = self.db.users.update({
            '_id': object_id
        }, {
            '$set': {'hash_password': hash_password}
        })

        return update_password
