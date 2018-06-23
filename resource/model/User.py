from .Model import Model


class UserModel(Model):
    def insertUser(self, account):
        inserted_user = self.db.users.insert_one(account)

        return inserted_user

    def getUser(self, user_id):
        get_user = self.db.users.find_one({'twitter_user_id': user_id})

        return get_user

    def updatePassword(self, object_id, hash_password):
        update_password = self.db.users.update({
            '_id': object_id
        }, {
            'hash_password': hash_password
        })

        return update_password


