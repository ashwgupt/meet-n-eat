from flask import Flask
from users import usersOps
from requests import requestOps
from proposals import proposalOps
from flask_httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()
app = Flask(__name__)

@app.route("/api/v1/users", methods = ['POST', 'GET'])
def users():
    return usersOps.userFunction()

# TODO: Secure GET method for users
# @app.route("/api/v1/users/", methods = ['GET'])
# @auth.login_required
# def users():
#     return usersOps.userFunction()


@app.route("/api/v1/users/<int:id>", methods = ['GET', 'PUT', 'DELETE'])
@auth.login_required
def modifyUsers(id):
    return usersOps.userId(id,this_user)


@app.route("/api/v1/requests", methods = ['GET', 'POST'])
@auth.login_required
def request():
    return requestOps.requestFunc(this_user)

@app.route("/api/v1/requests/<int:id>", methods = ['GET', 'PUT', 'DELETE'])
@auth.login_required
def requestId(id):
    return requestOps.RequestId(id,this_user)

@app.route("/api/v1/proposals", methods = ['GET', 'POST'])
@auth.login_required
def proposalsRequest():
    return proposalOps.proposalFunc(this_user)

@app.route("/api/v1/proposals/<int:id>", methods = ['GET'])
@auth.login_required
def proposalsRequestId(id):
    return proposalOps.proposalFuncId(id,this_user)

@auth.verify_password
def verify_password(username, password):
    global this_user
    this_user = username
    return usersOps.validateUser(username,password)


if __name__ == '__main__':
    app.debug = False
    app.run(host='0.0.0.0', port=5000)