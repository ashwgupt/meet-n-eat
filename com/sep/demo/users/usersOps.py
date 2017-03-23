import json

from flask import Flask, request, jsonify
from sqlalchemy import create_engine, exc, exists
from sqlalchemy.orm import sessionmaker
from werkzeug.security import generate_password_hash, check_password_hash
from models import Base,userData

engine = create_engine('sqlite:///users/Users.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

app = Flask(__name__)

def userFunction():
  if request.method == 'GET':
    return getAllUsers()
  elif request.method == 'POST':
    print "Making a New User"
    rdata = request.data
    rawdata = json.loads(rdata)
    jsonData = rawdata["UserDetails"]

    try:
        for item in jsonData:
            name = item.get("name")
            print name
            email = item.get("email")
            print email
            passwords = item.get("password")
            print passwords
            password_hash = generate_password_hash(passwords)
            print "%s", password_hash
            return makeANewUser(name, email, password_hash)
    except TypeError as err:
        return "Mandatory fields missing or Incorrect datatype passed " \
              "All fields - Name, Email, Password must be String"


def loginUser():
    if request.method == 'POST':
        rdata = request.data
        rawdata = json.loads(rdata)
        jsonData = rawdata["UserDetails"]

        for item in jsonData:
            email = item.get("email")
            passwords = item.get("password")

        return validateUser(email, passwords)

def getAllUsers():
  user = session.query(userData).all()
  return jsonify(UserDetails=[i.serialize for i in user])

def makeANewUser(name,email,passwords):
  newUser = userData(name = name, email=email, password_hash=passwords)
  try:
      session.add(newUser)
      session.commit()
      return jsonify(userData=newUser.serialize)
  except exc.IntegrityError as err:
      session.rollback()
      print err.message
      return "User Id already registered!!"
  except ValueError as err:
      session.rollback()
      print err.message
      return "Malformed Input!!"
  except Exception as err:
      session.rollback()
      err.message
      return "Something went wrong, we also dont know!!"

def validateUser(_email, passwords):
    try:
        User = session.query(userData).filter_by(email=_email).one()
    except Exception:
        session.rollback()
        return "No such user exists!!"
    _flag = check_password_hash(User.password_hash,passwords)
    if True == _flag:
        return "Login successfull"
    elif True != _flag:
        return "Login failed"

def extractUserId(_email):
    User = session.query(userData).filter_by(email=_email).one()
    return User.id

def userId(id):
    if request.method == 'GET':
         return getUser(id)
    elif request.method == 'PUT':
         return modifyUser(id)
    elif request.method == 'DELETE':
        return deleteUser(id)

def deleteUser(_id):
    try:
        User = session.query(userData).filter_by(id=_id).one()
    except Exception:
        session.rollback()
        return "No such user exists!!"
    session.delete(User)
    session.commit()
    return "User deleted!!"

def modifyUser(id):
    user = session.query(userData).filter_by(id = id)
    rdata = request.data
    rawdata = json.loads(rdata)
    jsonData = rawdata["UserDetails"]

    for item in jsonData:
        password = item.get("password")
    try:
        if password is not None:
            password_hash = generate_password_hash(password)
            user.update({"password_hash": password_hash})
        session.commit()
    except Exception as err:
        session.rollback
        print err.message
    user = session.query(userData).filter_by(id = id)
    return jsonify(RequestDetails=[i.serialize for i in user])

def getUser(id):
    try:
        #user = session.query(userData).filter_by(id = id).first()
        user = session.query((userData).exists().where(id == id)).scalar()
        return jsonify(UserDetails=[i.serialize for i in user])
    except Exception as err:
        session.rollback()
        print err.message
        return "No such user exists!!"
