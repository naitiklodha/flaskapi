from flask import Flask, jsonify, request, session
from config import ApplicationConfig
from pymongo import MongoClient
from flask_cors import CORS, cross_origin
import json
from flask_session import Session
from flask_bcrypt import bcrypt


app = Flask(__name__)
app.config.from_object(ApplicationConfig)
CORS(app, supports_credentials=True )



# Connecting to MongoDB
client = MongoClient('localhost', 27017)

db = client.get_database('userdata')
userd = db.user
app.secret_key = 'reactwithflaskisfun@@1@@2'


@app.route('/')
def index():
    email=session.get("email")
    

    if email:
        user=userd.find_one({"email":email})
        return jsonify({
            "name":user["name"],
            "email":email,
            "dob":user["dob"],
            "gender":user["gender"]
        })
    
    return jsonify({
        "error":"Unauthorized"
    }),401

@cross_origin
@app.route('/register', methods=["POST"])
def register():
    name = request.json["name"]
    username = request.json["username"]
    email = request.json["email"]
    dob = request.json["dob"]
    password = request.json["password"]
    gender=request.json["gender"]

    login_usermail = userd.find_one({"email": email})
    login_username = userd.find_one({"username": username})

    if login_usermail:
        return jsonify({"error": "User already exists"}), 403,

    if login_username:
        return jsonify({"error": "User already exists,try another username"}), 403,

    hashedpassword = bcrypt.hashpw(password.encode('UTF-8'), bcrypt.gensalt())
    user_input = {"name": name, "username": username,
                  "dob": dob, "gender":gender,"email": email, "password": hashedpassword}
    userd.insert_one(user_input)
    session["email"] = email
    user = userd.find_one({"email": email})
    id = str(user["_id"])

    return jsonify({
        "id": id,
        "email": email
    })

@cross_origin
@app.route('/login', methods=["POST"])
def login():

    email = request.json["useridentification"]
    username = request.json["useridentification"]
    password = request.json["password"]

    login_user = userd.find_one({"email": email})

    if login_user is None:
        login_user = userd.find_one({"username": username})

    if login_user:
        if bcrypt.hashpw(password.encode('utf-8'), login_user['password']) == login_user['password']:
            session["email"] = login_user["email"]
            id = str(login_user["_id"])
            return jsonify({
                "id": id,
                "username": login_user["username"],
                "email": login_user["email"]
            })

        return jsonify({
            "error": "Wrong password"
        }), 401

    return jsonify({
        "error": "No user found"
    }), 401


@app.route("/logouts", methods=["POST"])
def logout_user():
    session.pop("email")
    return "Logout successful"


if __name__ == "__main__":
    app.run(debug=True)
