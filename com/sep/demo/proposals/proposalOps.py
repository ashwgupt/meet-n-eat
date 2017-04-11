import json

from flask import Flask, request, jsonify
from sqlalchemy import create_engine, exc
from sqlalchemy.orm import sessionmaker
from models import Base, proposalData
from com.sep.demo.users.usersOps import extractUserId,extractUserName
from com.sep.demo.requests.requestOps import extractUser, acceptRequest
from com.sep.demo.utils.responseCode import returnStatus

engine = create_engine('sqlite:///proposals/Proposal.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

def proposalFunc(email):
    if request.method == 'GET':
        return getProposals(email)
    elif request.method == 'POST':
        return createProposal(email)

def proposalFuncId(id,email):
    if request.method == 'GET':
        return getProposal(id,email)
    elif request.method == 'DELETE':
        return deleteProposal(id,email)
    elif request.method == 'PUT':
        return modifyProposal(id,email)


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

def getProposals(email):
    userProposedFrom = extractUserName(extractUserId(email))
    try:
        proposal = session.query(proposalData)\
            .filter((proposalData.user_proposed_from == userProposedFrom)
                    | (proposalData.user_proposed_to == userProposedFrom))
        if proposal.count() == 0:
            return returnStatus("No matching proposals found for you!!")
    except Exception as err:
        session.rollback()
        print err.message
        return returnStatus("Something went wrong, we also dont know!!")
    return jsonify(ProposalDetails=[i.serialize for i in proposal])

def getProposal(id,email):
    userProposedFrom = extractUserName(extractUserId(email))
    try:
        proposal = session.query(proposalData).filter_by(id=id)
        if proposal.count() == 0:
            msg = "Prosposal with id: "+ str(id) +" not found"
            return returnStatus(msg)
        proposal = session.query(proposalData)\
            .filter_by(id = id)\
            .filter((proposalData.user_proposed_from == userProposedFrom)
                    | (proposalData.user_proposed_to == userProposedFrom))
        if proposal.count() == 0:
            return returnStatus("Sorry you are not authorised to view the proposal!!")
    except Exception as err:
        session.rollback()
        print err.message
        return returnStatus("Something went wrong, we also dont know!!")
    return jsonify(ProposalDetails=[i.serialize for i in proposal])

def deleteProposal(id,email):
    userProposedFrom = extractUserName(extractUserId(email))
    try:
        proposal = session.query(proposalData).filter_by(id=id)
        if proposal.count() == 0:
            msg = "Prosposal with id: " + str(id) + " not found"
            return returnStatus(msg)
        proposal = session.query(proposalData) \
            .filter_by(id=id) \
            .filter_by(user_proposed_from=userProposedFrom)
        if proposal.count() == 0:
            return returnStatus("Sorry you are not authorised to delete the proposal!!")
        session.delete(proposal.one())
        session.commit()
    except Exception as err:
        session.rollback()
        print err.message
        return returnStatus("Something went wrong, we also dont know!!")
    return returnStatus("Proposal deleted successfully!!")

def modifyProposal(id,email):
    userProposedTo = extractUserName(extractUserId(email))
    try:
        proposal = session.query(proposalData).filter_by(id=id)
        if proposal.count() == 0:
            msg = "Prosposal with id: " + str(id) + " not found"
            return returnStatus(msg)
        proposal = session.query(proposalData) \
            .filter_by(id=id) \
            .filter_by(user_proposed_to=userProposedTo)
        if proposal.count() == 0:
            return returnStatus("Sorry you are not authorised to modify the proposal!!")
        proposal.one().filled = True
        session.commit()
    except Exception as err:
        session.rollback()
        print err.message
        return returnStatus("Something went wrong, we also dont know!!")
    acceptRequest(proposal.one().request_id)
    return returnStatus("Proposal accepted successfully!!")