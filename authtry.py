import json
import time
import urllib.request
import os
from jose import jwk, jwt
from jose.utils import base64url_decode

COGNITO_USERPOOL_ID = os.environ['COGNITO_USERPOOL_ID']
COGNITO_WEB_CLIENT_ID = os.environ['COGNITO_WEB_CLIENT_ID']
REGION = 'ap-southeast-2'
keys_url = f'https://cognito-idp.{REGION}.amazonaws.com/{COGNITO_USERPOOL_ID}/.well-known/jwks.json'

# Download the public keys only on cold start
with urllib.request.urlopen(keys_url) as f:
    keys = json.loads(f.read().decode('utf-8'))['keys']

def verify_jwt_token(token):
    # Get the kid from the headers prior to verification
    #print(token)
    headers = jwt.get_unverified_headers(token)
    print(headers)
    kid = headers['kid']
    print(kid)

    # Search for the kid in the downloaded public keys
    key = next((k for k in keys if k['kid'] == kid), None)

    if not key:
        print('Public key not found in jwks.json')
        return False

    # Construct the public key
    public_key = jwk.construct(key)

    # Get the last two sections of the token: message and signature (encoded in base64)
    message, encoded_signature = str(token).rsplit('.', 1)

    # Decode the signature
    decoded_signature = base64url_decode(encoded_signature.encode('utf-8'))

    # Verify the signature
    if not public_key.verify(message.encode("utf8"), decoded_signature):
        print('Signature verification failed')
        return False

    print('Signature successfully verified')

    # Use the unverified claims since the verification passed
    claims = jwt.get_unverified_claims(token)

    # Verify the token expiration
    if time.time() > claims['exp']:
        print('Token is expired')
        return False

    # Verify the Audience (use claims['client_id'] if verifying an access token)
    if claims['aud'] != COGNITO_WEB_CLIENT_ID:
        print('Token was not issued for this audience')
        return None

    print(claims)
    return claims


def generate_policy(principal_id, effect, resource):
    auth_response = {}
    auth_response['principalId'] = principal_id
    if effect and resource:
        policy_document = {
            'Version': '2012-10-17',
            'Statement': [
                {
                    'Effect': effect,
                    'Resource': resource,
                    'Action': 'execute-api:Invoke'
                }
            ]
        }
        auth_response['policyDocument'] = policy_document
   
    print(json.dumps(auth_response))
    return auth_response


def handler(event, context):
    print("event:    ", event)
    token = event['authorizationToken']
    claims = verify_jwt_token(token)
    
    if claims:
        principal_id = claims['sub']
        effect = 'Allow'
        resource = event['methodArn']
        return generate_policy(principal_id, effect, resource)
    else:
        return {"message": "Incorrect token"}
