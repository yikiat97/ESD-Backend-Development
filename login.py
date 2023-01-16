from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from os import environ
import requests

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
 
db = SQLAlchemy(app)

CORS(app) 
 
class Login(db.Model):
    __tablename__ = 'login'
    
    username = db.Column(db.String(20), primary_key=True)
    password= db.Column(db.String(20), nullable=False)
    customer_id = db.Column(db.Integer)
    admin_id = db.Column(db.Integer)

    def __init__(self, username, password, customer_id = None, admin_id = None):
        self.admin_id = admin_id
        self.username = username
        self.password = password
        self.customer_id = customer_id

    def json(self):
        return {"admin_id": self.admin_id, "username": self.username, "password": self.password, "customer_id": self.customer_id}
 

 
@app.route("/login")
def get_all():
    login_list = Login.query.all()
    if len(login_list):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "logins": [login.json() for login in login_list]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no login info."
        }
    ), 404

 
@app.route("/login/<string:username>")
def find_by_username(username):
    login = Login.query.filter_by(username=username).first()
    if login:
        return jsonify(
            {
                "code": 200,
                "data": login.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Username not found."
        }
    ), 404   

 
@app.route("/login/<string:username>", methods=['POST'])
def create_username(username):
    if (Login.query.filter_by(username=username).first()):
        return jsonify(
            {
                "code": 400,
                "data": {
                    "username": username
                },
                "message": "Username already exists."
            }
        ), 400

    data = request.get_json()
    login = Login(username, **data)

    try:
        db.session.add(login)
        db.session.commit()
    except:
        return jsonify(
            {
                "code": 500,
                "data": {
                    "username": username
                },
                "message": "An error occurred creating the account."
            }
        ), 500

    return jsonify(
        {   
            "code": 201,
            "data": login.json()
        }
    ), 201

@app.route("/login/<string:username>", methods=['PUT'])
def update_login(username):
    login = Login.query.filter_by(username=username).first()
    if login:
        data = request.get_json()
        if "password" in data:
            login.password = data['password']
        # Commented this out because shouldnt be able to modify the customer_id and admin_id, doesnt make sense
        # if "customer_id" in data:
        #     login.customer_id = data['customer_id'] 
        # if "admin_id" in data:
        #     login.admin_id = data['admin_id'] 
        db.session.commit()
        return jsonify(
            {
                "code": 200,
                "data": login.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "data": {
                "username": username
            },
            "message": "Login not found."
        }
    ), 404

@app.route("/login/<string:username>", methods=['DELETE'])
def delete_login(username):
    login = Login.query.filter_by(username=username).first()
    if login:
        db.session.delete(login)
        db.session.commit()
        return jsonify(
            {
                "code": 200,
                "data": {
                    "username": username
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "data": {
                "username": username
            },
            "message": "Login not found."
        }
    ), 404

@app.route("/login/verify_grecaptcha", methods=["POST"])
def verify_grecaptcha():
    try:
        headers = request.headers
        params = {}
        if request.method == "POST":
            if request.is_json:
                params = request.json
            else:
                params = request.args

            method = 'verify_grecaptcha'
            # print(params)
            token = params["response"]
            # print(token)
            key = "6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe"
            url = 'https://www.google.com/recaptcha/api/siteverify'
            recaptcha_params = {'secret': key, 'response': token}
            print(recaptcha_params)
            response = requests.post(url, data=recaptcha_params)
            print(response)
            if response.status_code != 200:
                return response.content

            msg = 'success '
            results = response.json()
            # print(results)
            return jsonify(results), 200

    except Exception as error:
        return {"error": 'Bad request. ' + str(error)}, 400

 
if __name__ == '__main__':
    app.run(host = '0.0.0.0', port=5000, debug=True)