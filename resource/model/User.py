from .Model import Model


class UserModel(Model):
  def insertUser(self, account_setting):
    # pymongo error handle document
    # http://api.mongodb.com/python/current/api/pymongo/errors.html
    try:
      inserted_user = self.db.users.insert_one(account_setting)
    except self.errors.DuplicateKeyError as e:
      raise
    except:
      raise

    return inserted_user.acknowledged

  def getUser(self, user_id):
    try:
      get_user = self.db.users.find_one({'twitter_user_id': user_id})
    except:
      raise

    return get_user
