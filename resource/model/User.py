from .Model import Model


class UserModel(Model):
    def insertUser(self, account):
        inserted_user = self.db.users.insert_one(account)

        return inserted_user

    def getUser(self, objectid):
        get_user = self.db.users.find_one({
            '_id': objectid
        })

        return get_user

    def updatePassword(self, objectid, hash_password):
        update_password = self.db.users.update_one({
            '_id': objectid
        }, {
            '$set': {'hash_password': hash_password}
        })

        return update_password
