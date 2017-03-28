import json

from flask import Flask, request, jsonify
from sqlalchemy import create_engine, exc
from sqlalchemy.orm import sessionmaker
from models import Base, requestData
from com.sep.demo.users.usersOps import extractUserId
from com.sep.demo.clients.geocode import getGeocodeLocation
from com.sep.demo.utils.responseCode import returnStatus

engine = create_engine('sqlite:///requests/Request.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

def requestFunc():
    if request.method == 'GET':
        return getRequest()
    elif request.method == 'POST':
        return createRequest()

def prepareRequest():
    rdata = request.data
    rawdata = json.loads(rdata)
    jsonData = rawdata["RequestDetails"]

    try:
        for item in jsonData:
            mealType = item.get("mealType")
            mealTime = item.get("mealTime")
            location = item.get("location")
            emailId = item.get("emailId")

            userId = extractUserId(emailId)
            latitude = None
            longitude = None
            if location is not None:
                latitude, longitude = getGeocodeLocation(location)
            return mealTime, mealType, longitude, latitude, location, userId
    except TypeError as err:
        return returnStatus("Mandatory fields missing or Incorrect datatype passed " \
               "All fields - MealType, MealTime, Location and EmailId must be String")

def createRequest():
    meal_time, meal_type, longitude, latitude, location_string, userId = prepareRequest()
    newRequest = requestData(meal_time = meal_time, meal_type = meal_type, longitude = longitude, latitude = latitude, location_string = location_string, user_id = userId)
    try:
        session.add(newRequest)
        session.commit()
        return jsonify(requestData=newRequest.serialize)
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

def RequestId(id):
    if request.method == 'GET':
         return getRequestId(id)
    elif request.method == 'PUT':
        return modifyRequest(id)
    elif request.method == 'DELETE':
        return deleteRequest(id)

def getRequestId(id):
    try:
        request = session.query(requestData).filter_by(id = id).one()
        return jsonify(RequestDetails=[request.serialize])
    except Exception:
        session.rollback()
        return returnStatus("No such request exist!!")

def deleteRequest(id):
   try:
       requests = session.query(requestData).filter_by(id=id).one()
   except Exception:
         session.rollback()
         return returnStatus("No such request exist!!")
   session.delete(requests)
   return returnStatus("Request deleted!!")

def modifyRequest(id):
    new_meal_time, new_meal_type, new_longitude, new_latitude, new_location_string, new_userId = prepareRequest()
    try:
        request = session.query(requestData).filter_by(id = id).one()
    except Exception as err:
        print err.message
        return returnStatus("No such request exist!!")
    try:
        if new_meal_time is not None:
            request.update({"meal_time": new_meal_time})
        if new_meal_type is not None:
            request.update({"meal_type": new_meal_type})
        if new_location_string is not None:
            request.update({"location_string": new_location_string,"longitude": new_longitude,"latitude": new_latitude})
        session.commit()
    except Exception as err:
        session.rollback
        print err.message
    request = session.query(requestData).filter_by(id = id).one()
    return jsonify(RequestDetails=[request.serialize])
