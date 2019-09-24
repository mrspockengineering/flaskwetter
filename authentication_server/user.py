'''
Created on 18.09.2019

@author: markus
'''

# resource owner
from .. import Flaskwetter
from Flaskwetter import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    
    def get_user_id(self):
        return self.id