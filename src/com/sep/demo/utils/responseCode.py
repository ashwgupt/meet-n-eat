from flask import jsonify

# TODO: Return response message with error text
def returnStatus(message):
    response = {'responseCode': 'ABCD1000', 'responseMessage': message}
    return jsonify(ResponseMessage=[response])


