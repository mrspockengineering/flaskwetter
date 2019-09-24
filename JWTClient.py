'''
Created on 24.09.2019

requests protected resources

@author: markus
'''

import requests
from requests.auth import HTTPBasicAuth
import json
import jwt

# token = jwt.encode({'iss' : api_key, 'exp': exp}, api_secret, algorithm='HS256')

token = requests.get('localhost:5000/login', auth=HTTPBasicAuth('','password'))
print(token)

url = 'localhost:5000/protected'
headers = {'Authorization': 'Bearer' + token}
response = requests.get(url, headers = headers)
