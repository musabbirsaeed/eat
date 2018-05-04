#!/usr/bin/pytnon :
"""
example code to log food entries without food id

"""

import requests,json,sys
from fitbit.api import FitbitOauth2Client

# this file contains an access token for a particular user account
TOKEN_FILE="access_token.txt"

token = json.loads(open(TOKEN_FILE,"rt").read())

## - NB: this can be cleaned into a formal API
# meal types - this is like what time of the day meal we are recording.

MEAL_TYPE_ANYTIME=7

# food log web api  - 
# POST https://api.fitbit.com/1/user/[user-id]/foods/log.json

#NB: date needs to be YYYY-MM-DD format
# UnitId: 304 is servings. Use the API to get the food unit types
def log_food(token):
    "logs a food entry - example - NB: need to clean into API"

    user_id=token['user_id']
    headers = {'Authorization': 'Bearer %s' % token['access_token']}

    url = 'https://api.fitbit.com/1/user/%s/foods/log.json' % user_id
    food_entry={"foodName": "Laksa Mania",
        "mealTypeId": MEAL_TYPE_ANYTIME,
        "unitId":304,
        "unit":{"id":304,"name":"serving","plural":"servings"},
        "amount": 1.25,
        "date": "2018-04-29",
        "calories":370,
        "carbs":147,
        "fat":117.5,
        "fiber":115,
        "protein":115,
        "sodium":1325,
        "nutritionalValues":{
            "calories":370,
            "carbs":47,
            "fat":17.5,
            "fiber":5,
            "protein":5,
            "sodium":325,
            "shiokness": 9001,
            "calcium":10,
        } 
    }
    response=requests.post(url,data=food_entry,headers=headers);
    content=json.loads(response.content);
    print (json.dumps(content,indent=4));

log_food(token);

sys.exit(0)


# IGNORE THIS CRAP AT THE BACK


"""
API DOCS:
https://docs.google.com/document/d/1_q-K-ObMTZvO0qUEAxROrN3bwMujwAN25sLHwJzliK0/edit
https://trackapi.nutritionix.com/docs/
NUTRITION ID REFERENCE:
https://docs.google.com/spreadsheets/d/14ssR3_vFYrVAidDLJoio07guZM80SMR5nxdGpAX-1-A/edit#gid=0
"""

"""
authorization
https://www.fitbit.com/oauth2/authorize?response_type=code&client_id=22CRXZ&redirect_uri=http%3A%2F%2Fwww.google.com&scope=activity%20nutrition%20heartrate%20location%20nutrition%20profile%20settings%20sleep%20social%20weight
"""

token={"access_token":"eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiI2TDhMTDgiLCJhdWQiOiIyMkNSWFoiLCJpc3MiOiJGaXRiaXQiLCJ0eXAiOiJhY2Nlc3NfdG9rZW4iLCJzY29wZXMiOiJyc29jIHJhY3QgcnNldCBybG9jIHJ3ZWkgcmhyIHJudXQgcnBybyByc2xlIiwiZXhwIjoxNTI1NDMwOTE1LCJpYXQiOjE1MjU0MDIxMTV9.Nckz16DWQyXCICkizimAzd-3_w5xQ-EaNyr7HfUZ_is","expires_in":28800,"refresh_token":"d5b96b004d9a012c404b573ac1bdde7f0d6dee82469a390a57e9016d300989e2","scope":"activity weight social nutrition sleep location settings profile heartrate","token_type":"Bearer","user_id":"6L8LL8"}

