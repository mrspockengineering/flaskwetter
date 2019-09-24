'''
Created on 14.09.2019

@author: Erazer
'''
import os
import json

path = os.path.abspath(os.path.dirname(__file__))

with open (path + "\data\\user.json", "r") as inputfile:
    json_user = json.load(inputfile)
    print(json_user)