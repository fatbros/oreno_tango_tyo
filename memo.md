## Google credentials

### authorization url
http://localhost:5000/api/google/authorization_url

#### res
* authorization_url
* state

### credentials
* curl -X POST http://localhost:5000/api/google/credentials --data-urlencode "callback_url=?" --data-urlencode "state=?"

#### req params
* callback_url
* state

#### res
* objectid
* email
* jwt token
