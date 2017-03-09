import json

from flask import Flask, request, jsonify
from sqlalchemy import create_engine, exc
from sqlalchemy.orm import sessionmaker
from models import Base, requestData
from com.sep.demo.users.usersOps import extractUserId
from com.sep.demo.clients.geocode import getGeocodeLocation

engine = create_engine('sqlite:///requests/Request.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

def requestFunc():
    if request.method == 'GET':
        # Call the method to Get all of the puppies
        # return getAllRequests()
        return "GETCALL"
    elif request.method == 'POST':
        return createRequest()

def prepareRequest():
    rdata = request.data
    rawdata = json.loads(rdata)
    jsonData = rawdata["RequestDetails"]

    try:
        for item in jsonData:
            mealType = item.get("mealType")
            print mealType
            mealTime = item.get("mealTime")
            print mealTime
            location = item.get("location")
            print location
            emailId = item.get("emailId")
            print emailId

            userId = extractUserId(emailId)
            print userId
            latitude, longitude = getGeocodeLocation(location)
            print latitude
            print longitude
            return mealTime, mealType, longitude, latitude, location, userId
    except TypeError as err:
        return "Mandatory fields missing or Incorrect datatype passed " \
               "All fields - MealType, MealTime, Location and EmailId must be String"

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
        return "Malformed Input!!"
    except Exception as err:
        session.rollback()
        err.message
        return "Something went wrong, we also dont know!!"