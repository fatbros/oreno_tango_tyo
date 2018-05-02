from .Model import Model


class UserModel(Model):
    def insertUser(self, account_setting):
        inserted_user = self.db.users.insert_one(account_setting)

        return inserted_user

    def getUser(self, user_id):
        get_user = self.db.users.find_one({'twitter_user_id': user_id})

        return get_user
