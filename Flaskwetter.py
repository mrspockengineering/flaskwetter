'''

version 1.0


Wetterapp:
- Routing individuell
- DB-Anbindung

https://www.tutorialspoint.com/flask/flask_variable_rules.htm
https://realpython.com/python-f-strings/
    Formats

security (1t2)
https://www.youtube.com/watch?v=J5bIPtEbS0Q  (jwt)

next:
https
heroku        https://www.youtube.com/watch?v=skc-ZEU9kO8
'''

from flask import Flask, request, make_response, render_template, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
import json
import jwt
import datetime
from functools import wraps

from authlib.flask.oauth1 import ResourceProtector, current_credential
from authlib.flask.oauth1.cache import create_exists_nonce_func
from authlib.flask.oauth1.sqla import (
    create_query_client_func,
    create_query_token_func,
    OAuth1ClientMixin
)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)
app.config['SECRET_KEY'] = 'thisisthesecretkey'

# resource owner
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    def get_user_id(self):
        return self.id

class Client(db.Model, OAuth1ClientMixin):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey('user.id', ondelete='CASCADE')
    )
    user = db.relationship('User')


    



# div: formatting
name = "hans"
age = 23
def fformat():
    return f"flaskv11: hello {name}, you are {age} years"

users = {
    "page_count": 1,
    "page_number": 1,
    "page_size": 30,
    "total_records": 1,
    "users": [
        {
            "id": "dJCHw4R1R3GqCoGoW8mzzz",
            "first_name": "Hans",
            "last_name": "Mueller",
            "email": "hansmueller@gmx.de",
        },
        {
            "id": "dJCHw4R1R3GqCoGoW8mzzz",
            "first_name": "Hansi",
            "last_name": "Meier",
            "email": "hansmueller@gmx.de",
        },
        {
            "id": "dJCHw4R1R3GqCoGoW8mzzz",
            "first_name": "Hans",
            "last_name": "Mueller",
            "email": "hansmueller@gmx.de",
        },
        {
            "id": "dJCHw4R1R3GqCoGoW8mzzz",
            "first_name": "Stefan",
            "last_name": "Wirtz",
            "email": "stefanwirtz@gmx.de",
        }       
    ]
}

users2 = {
    "page_count": 1,
    "page_number": 1,
    "page_size": 30,
    "total_records": 1,
    "users": [
        {
            "id": "dJCHw4R1R3GqCoGoW8mzzz",
            "first_name": "Hans",
            "last_name": "Mueller",
            "email": "hansmueller@gmx.de",
        },
        {
            "id": "dJCHw4R1R3GqCoGoW8mzzz",
            "first_name": "Stefan",
            "last_name": "Wirtz",
            "email": "stefanwirtz@gmx.de",
        } 
               
    ]
}
# user_json = json.load(users)


wetterdaten = [
    {
        'author': 'Markus Gradl',
        'stadt': 'München',
        'max_temp': '32°',
        'min_temp': '19°',
        'date': 'July 22, 2019'
    },
    {
        'author': 'Markus Gradl',
        'stadt': 'München',
        'max_temp': '29°',
        'min_temp': '20°',
        'date': 'July 23, 2019'
    },
    {
        'author': 'Andrea Meier',
        'max_temp': '36°',
        'min_temp': '25°',
        'date': 'July 22, 2019'
    },
]


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token')   # http://localhost:5000/route?token=alshhfijfjdkls
        
        if not token:
            return jsonify({'message' : 'Token is missing!'}), 403
        
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
        except:
            return jsonify({'message' : 'Token is missing or invalid'}), 403
    
        return f(*args, **kwargs)
    
    return decorated
    
@app.route('/unprotected')
def unprotected():
    return jsonify({'message' : 'Anyone can view this!'})

@app.route('/protected')
@token_required
def protected():
    return jsonify({'message' : 'This is only available for people with valid tokens.'})



@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', wdaten=wetterdaten)

@app.route("/about")
def about():
    return render_template('about.html', title='About1')

@app.route('/hello')
def hello():
    return 'Hello worldv1t'

@app.route('/hello/<name>')
def hello_name(name):
    return 'Helloo %s!' %name   # %name = variable

@app.route('/hello2/<name>')
def hello2_name(name):
    return 'Hello2 %s!' %name   # %name = variable

@app.route('/add/<var1>/<var2>')
def add(var1, var2):
    return str(var1) + ' + ' + str(var2) + " = " + str(int(var1) + int(var2))

@app.route("/jsonusers")
@token_required
def jsonusers():
    resp = app.response_class(
    response=json.dumps(users),
    status=200,
    mimetype='application/json'
    )
    return resp

@app.route("/jsonusers2")           # simple Password-auth
def jsonusers2():
    resp = app.response_class(
    response=json.dumps(users2),
    status=200,
    mimetype='application/json'
    )
    
    auth = request.authorization
    if auth and auth.password == 'password':        
#        return make_response('Could verify')
        return resp
    return make_response('Could verify!', 401, {'WWW-Authenticate' : 'Basic realm="Login Required"'})


# jwt-Authenticaton provided from Flask; expiration time
@app.route("/login")          
def login():
    resp = app.response_class(
    response=json.dumps(users2),
    status=200,
    mimetype='application/json'
    )
    
    auth = request.authorization
    if auth and auth.password == 'password':
        # user, expires
        token = jwt.encode({'user' : auth.username, 'exp' : datetime.datetime.utcnow()  + datetime.timedelta(seconds = 30)}, app.config['SECRET_KEY'])   # minutes = 30     
#        return make_response('Could verify') # verify token in jwt.io
        print(token)
        return jsonify({'token' : token.decode('UTF-8')})    # alternative: 'token' : token.decode('UTC-8')
    return make_response('Could verify!', 401, {'WWW-Authenticate' : 'Basic realm="Login Required"'})


@app.route("/jsonwetter/")
@app.route("/jsonwetter")
def jsonwetter():
    resp = app.response_class(
    response=json.dumps(wetterdaten),
    status=200,
    mimetype='application/json'
    )
    return resp

def getWetterId(wid):
    return wetterdaten[wid]

@app.route('/jsonwetter/<wid>')
def jsonwetterId(wid):
    wdata = getWetterId(int(wid))    
    resp = app.response_class(
    response=json.dumps(wdata),
    status=200,
    mimetype='application/json'
    )
    return resp

if __name__ == '__main__':
#    print(getWetterId(0))
    print(fformat())
    app.run(debug=True)




'''
missing:        - security
                - POST
                
                
                - Database
                - pip3 install forms?
                - json-file
                
                - Python3- Umgebung
                
                - refactorin
'''