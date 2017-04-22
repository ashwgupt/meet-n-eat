import json

from flask import Flask, request, jsonify, _app_ctx_stack
from sqlalchemy import create_engine, exc
from sqlalchemy.orm import sessionmaker

from models import Base, proposalData
from src.com.sep.demo.requests.requestOps import extractUser, acceptRequest
from src.com.sep.demo.users.usersOps import extractUserId, extractUserName
from src.com.sep.demo.utils.responseCode import returnStatus

engine = create_engine('sqlite:///../../../../generated/Proposal.db')

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
    session = get_db()
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
            return returnStatus("Proposal created!!")
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
    session = get_db()
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
    session = get_db()
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
    session = get_db()
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
    session = get_db()
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