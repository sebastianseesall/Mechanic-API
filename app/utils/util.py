from datetime import datetime, timedelta, timezone
import jwt
import jose

SECRET_KEY = "a super secret, secret key"
#encode_token function that takes in a customer_id to create a token specific to that user.
def encode_token(customer_id):
    payload = {
        'customer_id': customer_id,
        'exp': datetime.now(timezone.utc) + timedelta(days=0, hours=1),
        'iat': datetime.now(timezone.utc), #Issued at (time) (~iat~)
        'sub':  str(customer_id) #This needs to be a string or the token will be malformed and won't be able to be decoded.
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token