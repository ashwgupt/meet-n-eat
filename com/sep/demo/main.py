from flask import Flask
from users import usersOps
from requests import requestOps

app = Flask(__name__)



@app.route("/api/v1/users", methods = ['GET', 'POST'])
def users():
    return usersOps.userFunction()

@app.route("/api/v1/users/<int:id>", methods = ['GET', 'PUT', 'DELETE'])
def modifyUsers(id):
    return usersOps.userId(id)

@app.route("/api/v1/requests", methods = ['GET', 'POST'])
def request():
    return requestOps.requestFunc()

@app.route("/api/v1/requests/<int:id>", methods = ['GET', 'PUT', 'DELETE'])
def requestId(id):
    return requestOps.RequestId(id)

if __name__ == '__main__':
    app.debug = False
    app.run(host='0.0.0.0', port=5000)