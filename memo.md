## Google credentials

### authorization url
http://localhost:5000/api/google/authorization_url

#### res params
* authorization_url
* state

### credentials
* curl -X POST http://localhost:5000/api/google/credentials --data-urlencode "callback_url=?" -d "state=?"

#### req params
* callback_url
* state

#### res params
* objectid
* email
* jwt_token

### update password
* curl -X PUT http://localhost:5000/api/password -d "objectid=?" -d "password=?" -d "jwt_token=?"

#### req params
* objectid
* password
* jwt_token

#### res params
* bool

### login
* curl -X POST http://localhost:5000/api/login -d "email=?" -d "password=?"

#### req params
* email
* password

#### res params
* objectid
* email
* jwt_token

## curl memo
* res headerを見る場合は `-i` を付ける
* urlをパラメータに持たせる場合は `--data-urlencode` を付ける
