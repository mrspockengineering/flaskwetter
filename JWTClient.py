'''
Created on 24.09.2019

@author: markus

Client for REST-API protected by HTTPBasicAuth (/login + /protected)

next:
- https, token im header?

'''
import requests
from requests.auth import HTTPBasicAuth
import json
import time

def basicAuth():
# Http BasicAuth
    token_array=[]
    while 1:
        time.sleep(10)
        response = requests.get('http://localhost:5000/login', auth=('','password'))        # allg.: client_key, client_secret
        print(response.content.decode('utf-8'))
        token = json.loads(response.content.decode('utf-8'))['token']
        token_array.append(token); print(token_array)
        
#        url = 'http://localhost:5000/protected'
        url = 'http://localhost:5000/jsonusers'
        # token im header
        # headers = {'Authorization': 'Bearer' + token}
        # response = requests.get(url, headers = headers)
        
        # token im get
        response = requests.get(url+'?token='+token)
        data = response.content.decode('utf-8')
        print(data, type(data))

if __name__ == '__main__':
    basicAuth()
    