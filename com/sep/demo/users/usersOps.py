import json

from flask import Flask, request, jsonify
from sqlalchemy import create_engine, exc
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
    #Call the method to Get all of the puppies
    print "GET CALL"
    return getAllUsers()
  elif request.method == 'POST':
	#Call the method to make a new puppy
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
            # name = request.args.get('name', '')
            # description = request.args.get('description', '')

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