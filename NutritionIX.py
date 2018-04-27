"""
API DOCS:
https://docs.google.com/document/d/1_q-K-ObMTZvO0qUEAxROrN3bwMujwAN25sLHwJzliK0/edit
https://trackapi.nutritionix.com/docs/
NUTRITION ID REFERENCE:
https://docs.google.com/spreadsheets/d/14ssR3_vFYrVAidDLJoio07guZM80SMR5nxdGpAX-1-A/edit#gid=0
"""

import json
from PIL import Image
from pyzbar.pyzbar import decode
import requests


APPLICATION_ID = '08a406db'
APPLICATION_KEY = 'ce2b4b499aa0b4ea891aadb62e681d44'
HEADERS = {
    'Content-Type': 'application/json',
    'x-app-id': APPLICATION_ID,
    'x-app-key': APPLICATION_KEY
}


def quick_food_search():
    """
    Quick food search API (with autocomplete)
    Used to populate search interfaces (eg. search bar drop downs)
    Reference: https://gist.github.com/mattsilv/6d19997bbdd02cf5337e9d4806b4f464
    """
    url = 'https://trackapi.nutritionix.com/v2/search/instant'
    params = {
        'query': 'Gyro',
        'detailed': True
    }
    response = requests.get(url=url, headers=HEADERS, params=params)
    content = json.loads(response.content)

    print(json.dumps(content, indent=4))


def detailed_nutrition_lookup():
    """
    Natural language nutrition lookup API
    References:
    - https://gist.github.com/mattsilv/9dfb709e7609537ffd3b1b8c097e9bfb
    - https://gist.github.com/mattsilv/95f94dd1378d4747fb68ebb2d042a4a6
    """
    url = 'https://trackapi.nutritionix.com/v2/natural/nutrients'
    body = {
        "query": "for breakfast i ate 2 eggs, bacon, and french toast",
        "timezone": "US/Eastern"
    }
    response = requests.post(url=url, headers=HEADERS, json=body)
    content = json.loads(response.content)

    print(json.dumps(content, indent=4))


def filtered_search():
    """
    Filtered searches based on nutrition (eg. less than 500 calories, 10mg of sodium)
    Caveat - Open ended search not allowed, need to provide name of food
    Basically serves the purpose of finding brands of food products that meet certain nutritional values
    Reference: https://gist.github.com/SorJEF/7879bd6c17237c9daf9cd678fd0d1fcc
    """
    url = 'https://trackapi.nutritionix.com/v2/search/instant'

    # 203 - Protein
    # 204 - Fat
    # 205 - Carbohydrate
    # 208 - Calories
    # gte - Greater than or equal to
    # lte - Less than or equal to
    body = {
        "query": "burgers",
        "full_nutrients": {
            "203": {
                "gte": 5
            },
            "204": {
                "lte": 5
            },
            "205": {
                "gte": 10,
                "lte": 40
            }
        }
    }
    response = requests.post(url=url, headers=HEADERS, json=body)
    content = json.loads(response.content)

    print(json.dumps(content, indent=4))


def restaurant_lookup(measure='point_distance'):
    """
    Location-based restaurant lookup API
    Supports point distance or bounding box queries
    Reference: https://gist.github.com/SorJEF/6319e7f6a0474a8a2b2ada80037fffe7
    """
    url = 'https://trackapi.nutritionix.com/v2/locations'

    # Lookup by distance from point (lon, lat)
    if measure == 'point_distance':
        params = {
            'll': '39,-77',
            'distance': '10km',
            'limit': 1
        }
        response = requests.get(url=url, headers=HEADERS, params=params)
        content = json.loads(response.content)
        print(json.dumps(content, indent=4))

    # Lookup within a bounded box (2 lon, lat)
    elif measure == 'bounded_box':
        params = {
            'north_east': '46.4983,-63.6328',
            'south_west': '27.9167, -117.9492',
            'limit': 1
        }
        response = requests.get(url=url, headers=HEADERS, params=params)
        content = json.loads(response.content)
        print(json.dumps(content, indent=4))


def barcode_lookup():
    """
    Nutrition lookup using barcode
    Reference: https://gist.github.com/mattsilv/478c9288f213ce5333399a41bd6da5a4
    """
    url = 'https://trackapi.nutritionix.com/v2/search/item'
    params = {
        'upc': decode_barcode()
    }
    response = requests.get(url=url, headers=HEADERS, params=params)
    content = json.loads(response.content)

    print(json.dumps(content, indent=4))


def decode_barcode():
    """
    Decodes barcode using pyzbar library
    """
    decoded_barcode = decode(Image.open('sample-barcode.png'))
    return decoded_barcode[0][0]


# quick_food_search()
# detailed_nutrition_lookup()
# filtered_search()
# restaurant_lookup(measure='point_distance')
# restaurant_lookup(measure='bounded_box')
# decode_barcode()
barcode_lookup()
