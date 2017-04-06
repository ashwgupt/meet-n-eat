import json

from flask import Flask, request, jsonify
from sqlalchemy import create_engine, exc
from sqlalchemy.orm import sessionmaker
from models import Base, proposalData
from com.sep.demo.users.usersOps import extractUserId,isUserAuthorized,extractUserName
from com.sep.demo.requests.requestOps import extractUser
from com.sep.demo.utils.responseCode import returnStatus

engine = create_engine('sqlite:///proposals/Proposal.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

def proposalFunc(email):
    if request.method == 'GET':
        return True
    elif request.method == 'POST':
        return createProposal(email)

def createProposal(email):
    rdata = request.data
    rawdata = json.loads(rdata)
    jsonData = rawdata["ProposalDetails"]
    try:
        for item in jsonData:
            request_id = item.get("requestId")
    except Exception as err:
        print err.message
        return returnStatus("Mandatory field - requestId missing or Incorrect datatype passed")
    userProposedFrom = extractUserName(extractUserId(email))
    try:
        proposal = session.query(proposalData).filter_by(request_id=request_id,user_proposed_from=userProposedFrom).one()
        print proposal.request_id
        return returnStatus("Proposal already exist!!")
    except Exception as err:
        userProposedTo = extractUserName(extractUser(request_id))
        if (extractUserId(email) == int(extractUser(request_id))):
            return returnStatus("Cannot propose to yourself!!")
        newProposal = proposalData(request_id=request_id, user_proposed_from=userProposedFrom, user_proposed_to=userProposedTo)
        try:
            session.add(newProposal)
            session.commit()
            return jsonify(proposalData=newProposal.serialize)
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
