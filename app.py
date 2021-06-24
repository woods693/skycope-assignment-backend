from flask import Flask, request, jsonify, session
from time import sleep
import os
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
import service1, service2

#include a counter after to make sure that when the same service is called after a prolonged period of time, I should reset the gen
def generate(file_path):
        with open(file_path, "r") as logfile:
            print(logfile.seek(0, os.SEEK_END))
            while True:
                #gives a generator object that can be called repeatedly using next which resumes the method from where it originally yielded
                yield {"entry": logfile.readlines()}

app = Flask(__name__)
app.config['SECRET_KEY'] = 'This is a sample key for my flask web server'
auth = HTTPBasicAuth()

users = {
    "user1": generate_password_hash("user1"),
    "user2": generate_password_hash("user2")
}

privilege = {
    "user1": "normal",
    "user2": "admin"
}

app.config["DEBUG"] = True

log_file_path_1 = "./logs/service1-debug.log"
log_file_path_2 = "./logs/service2-debug.log"

gen_1 = None
gen_2 = None

@app.route("/")
def main():
    return "Main Page of Web-Server"

@app.route('/api/login', methods=['POST'])
def login():
    global gen_1, gen_2
    gen_1 = None
    gen_2 = None
    json_data = request.json
    user = json_data['username']
    priv = ""
    #print(check_password_hash(users[user],json_data['password']))
    if user in users and check_password_hash(users[user],json_data['password']):
        session['logged_in'] = True
        status = True
        priv = privilege[user]
    else:
        status = False
        user = ""
    return jsonify({'result': status, 'username': user, 'privilege': priv})

@app.route('/api/logout')
def logout():
    session.pop('logged_in', None)
    return jsonify({'result': 'false'})

@app.route("/run_service1", methods=['GET'])
def run_service1():
    os.system('python service1.py')
    return "Running Service 1"

@app.route("/run_service2", methods=['GET'])
def run_service2():
    os.system('python service2.py')
    return "Running Service 2"

@app.route("/api/service1", methods=['GET'])
def service1():
    global gen_1, gen_2
    gen_2 = None
    if gen_1 is None: 
        gen_1 = generate("./logs/service1-debug.log")
    return next(gen_1)

@app.route("/api/service2", methods=['GET'])
def service2():                            
    global gen_1, gen_2
    gen_1 = None
    if gen_2 is None:
        gen_2 = generate("./logs/service2-debug.log")
    return next(gen_2)

if __name__ == "__main__":
    app.run()
