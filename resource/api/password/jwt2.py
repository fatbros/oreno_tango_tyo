import base64
import json

import jwt

_jwt = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiYWRtaW4iOnRydWV9.TJVA95OrM7E2cBab30RMHrHDcEfxjoYZgeFONFh7HgQ'

tmp = _jwt.split('.')

header = json.loads(base64.b64decode(tmp[0]).decode())
payload = json.loads(base64.b64decode(tmp[1]).decode())

print('==========')
print(header)
print(payload)
print('==========')

decode_data = jwt.decode(_jwt, 'secret', algorithms=['HS256'])
print(decode_data)

# decode_data = jwt.decode(_jwt, 'test', algorithms=['HS256'])
# print(decode_data)

encode_data = jwt.encode(payload, 'secret', algorithm='HS256', headers=header)

decode_data2 = jwt.decode(encode_data, 'secret', algorithms=['HS256'])
print(decode_data2)
