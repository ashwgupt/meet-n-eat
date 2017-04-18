import json

from flask import request, jsonify
from sqlalchemy import create_engine, exc
from sqlalchemy.orm import sessionmaker
from models import Base, requestData
from com.sep.demo.users.usersOps import extractUserId,isUserAuthorized
from com.sep.demo.clients.geocode import getGeocodeLocation
from com.sep.demo.utils.responseCode import returnStatus

engine = create_engine('sqlite:///requests/Request.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

def requestFunc(email):
    if request.method == 'GET':
        return getRequest()
    elif request.method == 'POST':
        return createRequest(email)

def prepareRequest(emailId):
    rdata = request.data
    rawdata = json.loads(rdata)
    jsonData = rawdata["RequestDetails"]
    try:
        for item in jsonData:
            mealType = item.get("mealType")
            mealTime = item.get("mealTime")
            location = item.get("location")

            userId = extractUserId(emailId)
            latitude = None
            longitude = None
            if location is not None:
                latitude, longitude = getGeocodeLocation(location)
            return mealTime, mealType, longitude, latitude, location, userId
    except TypeError as err:
        return returnStatus("Mandatory fields missing or Incorrect datatype passed " \
               "All fields - MealType, MealTime, Location and EmailId must be String")

def createRequest(email):
    meal_time, meal_type, longitude, latitude, location_string, userId = prepareRequest(email)
    newRequest = requestData(meal_time = meal_time, meal_type = meal_type, longitude = longitude, latitude = latitude, location_string = location_string, user_id = userId)
    try:
        session.add(newRequest)
        session.commit()
        return returnStatus("Request created!!")
    except ValueError as err:
        session.rollback()
        print err.message
        return returnStatus("Malformed Input!!")
    except exc.IntegrityError as err:
        print err.message
        session.rollback()
        return returnStatus("Missing required field")
    except Exception as err:
        session.rollback()
        print err.message
        return returnStatus("Something went wrong, we also dont know!!")

def getRequest():
    request = session.query(requestData).all()
    return jsonify(RequestDetails=[i.serialize for i in request])

def RequestId(id,emailId):
    if request.method == 'GET':
         return getRequestId(id)
    elif request.method == 'PUT':
        return modifyRequest(id,emailId)
    elif request.method == 'DELETE':
        return deleteRequest(id,emailId)

def getRequestId(id):
    try:
        request = session.query(requestData).filter_by(id = id).one()
        return jsonify(RequestDetails=[request.serialize])
    except Exception:
        session.rollback()
        return returnStatus("No such request exist!!")

def deleteRequest(id,emailId):
   userId = extractUserId(emailId)
   try:
       requests = session.query(requestData).filter_by(id=id).one()
       if not (isUserAuthorized(requests.user_id, userId)):
           return returnStatus("Not authorized to perform this operation!!")
   except Exception:
         session.rollback()
         return returnStatus("No such request exist!!")
   session.delete(requests)
   return returnStatus("Request deleted!!")

def modifyRequest(id,emailId):
    new_meal_time, new_meal_type, new_longitude, new_latitude, new_location_string, userId = prepareRequest(emailId)
    try:
        request = session.query(requestData).filter_by(id = id).one()
        if not (isUserAuthorized(request.user_id, userId)):
            return returnStatus("Not authorized to perform this operation!!")
    except Exception as err:
        print err.message
        return returnStatus("No such request exist!!")
    try:
        if new_meal_time is not None:
            request.meal_time = new_meal_time
        if new_meal_type is not None:
            request.meal_type = new_meal_type
        if new_location_string is not None:
            request.location_string = new_location_string
            request.latitude = new_latitude
            request.longitude = new_longitude
        session.commit()
    except Exception as err:
        session.rollback
        print err.message
    return returnStatus("Request modified!!")

def extractUser(id):
    request = session.query(requestData).filter_by(id=id).one()
    return request.user_id

def acceptRequest(id):
    try:
        request = session.query(requestData).filter_by(id=id).one()
        request.filled = True
        session.commit()
    except Exception as err:
        session.rollback()
        print err.message()
        return returnStatus("We dont know dude!!")


