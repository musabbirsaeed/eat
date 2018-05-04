#!/usr/bin/python
"""
Example outh2 authorization workflow for fitbit - run the curl command at the end to get a valid token
"""
import sys,requests
import base64
from requests_oauthlib import OAuth2Session
from oauthlib.oauth2 import MobileApplicationClient
from oauthlib.oauth2 import WebApplicationClient

# global parameters, set up the client info file and secret here
# Set up your client ID , secret and scope, id and secret should be from the 

CLIENT_FN="client_app.txt"
SCOPE = ["activity", "heartrate", "location", "nutrition", "profile", "settings", "sleep", "social", "weight"]

# Helpers 

def load_client_secrets(fn):
    "loads client secretns from a file, returning client_id and secret"
    client_id=""
    client_secret=""
    for line in open(fn):
        if line.startswith("client_id"):
            client_id=line.strip().split("=")[1].strip('"')
        elif line.startswith("client_secret"):
            client_secret=line.strip().split("=")[1].strip('"')
    if client_id == None or client_secret==None:
        raise RuntimeError("need to have %s with client app credentials setup"%fn)
    return (client_id,client_secret)

client_id,client_secret=load_client_secrets(CLIENT_FN)

# Initialize client
client = WebApplicationClient(client_id)
fitbit = OAuth2Session(client_id, client=client, scope=SCOPE,state=1,redirect_uri="http://www.google.com")
authorization_url = "https://www.fitbit.com/oauth2/authorize"

# Grab the URL for Fitbit's authorization page.
auth_url, state = fitbit.authorization_url(authorization_url)
print("Visit this page in your browser: {}".format(auth_url))

# After authenticating, Fitbit will redirect you to the URL you specified in your application settings. It contains the access token.
code = raw_input("Copy and paste the authorization token code in the redirect url here (code=XXXX): ")

# calculate authorization header - this is base64 encoding of string client_id:client_secret
b64encoded_secret=base64.b64encode("%s:%s"% (client_id,client_secret))

CMD="""
curl -X POST \\
  https://api.fitbit.com/oauth2/token \\
  -H 'authorization: Basic {b64enc}' \\
  -H 'content-type: application/x-www-form-urlencoded' \\
  -d 'client_id={client_id}&grant_type=authorization_code&redirect_uri=http%3A%2F%2Fwww.google.com&code={code}' \\
""".format(b64enc=b64encoded_secret,client_id=client_id,code=code)

print "Use this command to get a token"
print CMD

