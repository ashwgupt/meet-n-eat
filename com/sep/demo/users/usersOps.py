import json

from flask import Flask, request, jsonify
from sqlalchemy import create_engine, exc, exists
from sqlalchemy.orm import sessionmaker
from werkzeug.security import generate_password_hash, check_password_hash
from models import Base,userData
from com.sep.demo.utils.responseCode import returnStatus


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
        print err.message
        return returnStatus("Mandatory fields missing or Incorrect datatype passed " \
              "All fields - Name, Email, Password must be String")


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
      return returnStatus("User Id already registered!!")
  except ValueError as err:
      session.rollback()
      print err.message
      return returnStatus("Malformed Input!!")
  except Exception as err:
      session.rollback()
      err.message
      return returnStatus("Something went wrong, we also dont know!!")


def validateUser(_email, passwords):
    flag = False
    try:
        User = session.query(userData).filter_by(email=_email).one()
    except Exception:
        session.rollback()
        return False
    flag = check_password_hash(User.password_hash,passwords)
    return flag


def extractUserId(_email):
    User = session.query(userData).filter_by(email=_email).one()
    return User.id


def userId(id,emailId):
    userId = extractUserId(emailId)
    try:
        user = session.query(userData).filter_by(id=id).one()
        if not (isUserAuthorized(user.id, userId)):
            return returnStatus("Not authorized to perform this operation!!")
    except Exception:
        session.rollback()
        return returnStatus("No such user exists!!")
    if request.method == 'GET':
         return getUser(id)
    elif request.method == 'PUT':
        return modifyUser(id)
    elif request.method == 'DELETE':
        return deleteUser(id)


def deleteUser(_id):
    try:
        user = session.query(userData).filter_by(id=_id).one()
    except Exception:
        session.rollback()
        return returnStatus("No such user exists!!")
    session.delete(user)
    session.commit()
    return returnStatus("User deleted!!")


def modifyUser(id):
    try:
        user = session.query(userData).filter_by(id = id).one()
    except Exception as err:
        print err.message
        return returnStatus("No such user exists!!")
    rdata = request.data
    rawdata = json.loads(rdata)
    jsonData = rawdata["UserDetails"]

    for item in jsonData:
        password = item.get("newpassword")
    try:
        if password is not None:
            password_hash = generate_password_hash(password)
            user.password_hash = password_hash
        session.commit()
    except Exception as err:
        session.rollback
        print err.message
    user = session.query(userData).filter_by(id = id).one()
    return jsonify(UserDetails=[user.serialize])


def getUser(id):
    try:
        user = session.query(userData).filter_by(id = id).one()
        return jsonify(UserDetails=[user.serialize])
    except Exception as err:
        print err.message
        return returnStatus("No such user exists!!")


def isUserAuthorized(allowed_id, passed_id):
    if int(allowed_id)==passed_id:
        return True
    else:
        return False
