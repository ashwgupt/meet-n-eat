import json

from flask import Flask, request, jsonify, _app_ctx_stack
from sqlalchemy import create_engine, exc
from sqlalchemy.orm import sessionmaker
from werkzeug.security import generate_password_hash,\
    check_password_hash

from models import Base, userData
from src.com.sep.demo.utils.responseCode import returnStatus

engine = create_engine('sqlite:///../../../../generated/Users.db')

app = Flask(__name__)


def get_db():
    """
    Opens a new database connection if there is none yet for the
    current application context.
    """
    top = _app_ctx_stack.top
    if not hasattr(top, 'sqlite_db'):
        DBSession = sessionmaker(bind=engine)
        top.sqlite_db = DBSession()
    return top.sqlite_db


@app.cli.command('initdb')
def initdb_command():
    """Initialize the database."""
    Base.metadata.bind = engine
    print('Initialized the database.')


@app.teardown_appcontext
def close_database(exception):
    """Closes the database again at the end of the request."""
    top = _app_ctx_stack.top
    if hasattr(top, 'sqlite_db'):
        top.sqlite_db.close()

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
    session = get_db()
    try:
        user = session.query(userData).all()
        return jsonify(UserDetails=[i.serialize for i in user])
    except exc.OperationalError:
        return returnStatus("The database doesn't exist yet")
    except Exception as err:
        print err.message
        return returnStatus("Database exception occurraed")


def makeANewUser(name,email,passwords):
  newUser = userData(name = name, email=email, password_hash=passwords)
  session = get_db()
  try:
      session.add(newUser)
      session.commit()
      return returnStatus("User registered!!")
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
    session = get_db()
    try:
        User = session.query(userData).filter_by(email=_email).one()
    except Exception:
        session.rollback()
        return flag
    flag = check_password_hash(User.password_hash,passwords)
    return flag


def extractUserId(_email):
    session = get_db()
    User = session.query(userData).filter_by(email=_email).one()
    return User.id


def extractUserName(id):
    session = get_db()
    User = session.query(userData).filter_by(id=id).one()
    return User.name


def userId(id,emailId):
    userId = extractUserId(emailId)
    session = get_db()
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

##TODO To delete requests/proposals for the user
def deleteUser(_id):
    session = get_db()
    try:
        user = session.query(userData).filter_by(id=_id).one()
    except Exception:
        session.rollback()
        return returnStatus("No such user exists!!")
    session.delete(user)
    session.commit()
    return returnStatus("User deleted!!")


def modifyUser(id):
    session = get_db()
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
    return returnStatus("User modified!!")


def getUser(id):
    session = get_db()
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
