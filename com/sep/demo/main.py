from flask import Flask
from users import usersOps
from requests import requestOps

app = Flask(__name__)



@app.route("/api/v1/users", methods = ['GET', 'POST'])
def users():
    return usersOps.userFunction()

@app.route("/api/v1/login", methods = ['GET', 'POST'])
def login():
    return usersOps.loginUser()

@app.route("/api/v1/requests", methods = ['GET', 'POST'])
def request():
    return requestOps.requestFunc()

@app.route("/api/v1/requests/<int:id>", methods = ['GET', 'PUT', 'DELETE'])
def requestId(id):
    return requestOps.RequestId(id)

if __name__ == '__main__':
    app.debug = False
    app.run(host='0.0.0.0', port=5000)