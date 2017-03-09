import json

from flask import Flask, request, jsonify
from sqlalchemy import create_engine, exc
from sqlalchemy.orm import sessionmaker
from models import Base, requestData

def requestFunc():
    if request.method == 'GET':
        # Call the method to Get all of the puppies
        return getAllRequests()
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
            #extract longitude and latitude , extract id using email from Users DB
            return makeANewUser(name, email, password_hash)
    except TypeError as err:
        return "Mandatory fields missing or Incorrect datatype passed " \
               "All fields - Name, Email, Password must be String"

