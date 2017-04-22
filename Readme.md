# Meet-n-Eat Application

This is an application written in Python and using Flask framework showcasing a standard implementation of RESTful APIs.

## Technology Stack Used

1. Python 2.7
1. Flask 
1. SqlAlchemy

## Run Locally

This section will cover how to setup and run the application locally on any type of desktop

### Setup the App

In order to setup and run the code locally below steps shall be required:

1. Install [Python 2.7](https://www.python.org/downloads/) as the runtime engine.

1. Install Flask framework using `pip` provided by Python 2.7 to euip app with a web-server : 
`pip install flask`

1. Install Http Auth library from Flask for use of implementing Basic_Auth : 
`pip install flask_httpauth`

1. Install SqlAlchemy for RDBMS purpose : 
`pip install sqlalchemy`

1. Install `httplib2` library to provide support for http operations as client : 
`pip install httplib2`

Use any Python IDE of your choice. [PyCharm Community Edition](https://www.jetbrains.com/pycharm/download/) can be used for free.

### Launch the App

Launching the app is simple. Just run the `main.py` program to start the application. The Python command line or the chosen IDE can be used to do the same.

If started successfully, the log entry like the one below should be made on the console:

``` * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)``` 

That indicates that the application is started successfully on localhost port 5000

## Accessing APIs

To consume the APIs hosted by the application can be accessed using the documentation as below.

> Please note that for any required authentication and authorization `BASIC_AUTH` is the only available mechanism at the moment, that takes the registered users' credentials to authenticate.

### API Documentation

Below is the list of operations available, and the API endpoints and corresponding HTTP Methods to complete the operation.

#### Users Creation

**API** : `/api/v1/users`

**HTTP Method** : POST

**Security** : None

**Request Body** : 
```json
{
	"UserDetails": [{
		"name": "Ashwin", <STRING, MANDATORY>
		"email": "ashwin.gupta@abc.com", <STRING, MANDATORY>
		"password": "password" <STRING, MANDATORY>
	}]
}
```

**Response** :

* HTTP Status : UNAUTHORIZED - 401 (for case of authN failure)
* HTTP Status : OK - 200 (For all rest cases)
* Body : 
```json
{
    "ResponseMessage": [{
        "responseCode": "api response code",
        "responseMessage": "message text"
    }]
}
```
* HTTP Status : INTERNAL_SERVER_ERROR - 500 (for any other error)

#### Users Retrieval

**API** : `/api/v1/users`

**HTTP Method** : GET

**Security** : BASIC_AUTH

**Request Body** : None

**Response** :

***success***
* HTTP Status : OK - 200 (For all rest cases)
* Body : 
```json
{
    "UserDetails": [{
        "email": "ashwin.gupta@abc.com",
        "id": 1,
        "name": "Ashwin"
    }, {
        "email": "rishi.madan@abc.com",
        "id": 2,
        "name": "Rishi"
    }]
}
```
***failure***
* HTTP Status : UNAUTHORIZED - 401 (for case of authN failure)
* HTTP Status : OK - 200 (For all rest cases)
* Body : 
```json
{
    "ResponseMessage": [{
        "responseCode": "api response code",
        "responseMessage": "message text"
    }]
}
```
* HTTP Status : INTERNAL_SERVER_ERROR - 500 (for any other error)

#### User Retrieval

**API** : `/api/v1/users/<int:id>`

**HTTP Method** : GET

**Security** : BASIC_AUTH

**Request Body** : None

**Response** :

***success***
* HTTP Status : OK - 200 (For all rest cases)
* Body : 
```json
{
    "UserDetails": [{
        "email": "ashwin.gupta@abc.com",
        "id": 1,
        "name": "Ashwin"
    }]
}
```
***failure***
* HTTP Status : UNAUTHORIZED - 401 (for case of authN failure)
* HTTP Status : OK - 200 (For all rest cases)
* Body : 
```json
{
    "ResponseMessage": [{
        "responseCode": "api response code",
        "responseMessage": "message text"
    }]
}
```
* HTTP Status : INTERNAL_SERVER_ERROR - 500 (for any other error)

#### User Modification

**API** : `/api/v1/users/<int:id>`

**HTTP Method** : PUT

**Security** : BASIC_AUTH

**Request Body** : 
```json
{
	"UserDetails": [{
		"newpassword": "newpassword" <STRING, MANDATORY>
	}]
}
```

**Response** :

* HTTP Status : UNAUTHORIZED - 401 (for case of authN failure)
* HTTP Status : OK - 200 (For all rest cases)
* Body : 
```json
{
    "ResponseMessage": [{
        "responseCode": "api response code",
        "responseMessage": "message text"
    }]
}
```
* HTTP Status : INTERNAL_SERVER_ERROR - 500 (for any other error)

#### User Deletion

**API** : `/api/v1/users/<int:id>`

**HTTP Method** : DELETE

**Security** : BASIC_AUTH

**Request Body** : None

**Response** :

* HTTP Status : UNAUTHORIZED - 401 (for case of authN failure)
* HTTP Status : OK - 200 (For all rest cases)
* Body : 
```json
{
    "ResponseMessage": [{
        "responseCode": "api response code",
        "responseMessage": "message text"
    }]
}

#### Requests Creation

**API** : `/api/v1/requests`

**HTTP Method** : POST

**Security** : BASIC_AUTH

**Request Body** : 
```json
{
	"requestDetails": [{
		"meanType": "Italian", <STRING, MANDATORY>
		"mealTime: "Dinner", <STRING, MANDATORY>
		"location": "Lag Vegas, Naveda" <STRING, MANDATORY>
	}]
}
```

**Response** :

* HTTP Status : UNAUTHORIZED - 401 (for case of authN failure)
* HTTP Status : OK - 200 (For all rest cases)
* Body : 
```json
{
    "ResponseMessage": [{
        "responseCode": "api response code",
        "responseMessage": "message text"
    }]
}
```
* HTTP Status : INTERNAL_SERVER_ERROR - 500 (for any other error)

#### Requests Retrieval

**API** : `/api/v1/requests`

**HTTP Method** : GET

**Security** : BASIC_AUTH

**Request Body** : None

**Response** :

***success***
* HTTP Status : OK - 200 (For all rest cases)
* Body : 
```json
{
    "requestDetails": [{
        "mealType": "Italian",
		"mealTime": "Dinner",
		"location": "Lag Vegas, Naveda",
        "id": 1,
        "user_id": "2",
        "filled": False
    }, {
        "requestDetails": [{
        "mealType": "Mughlai",
		"mealTime": "Lunch",
		"location": "Wesminster, London",
        "id": 2,
        "user_id": "1",
        "filled": True
    }]
}
```
***failure***
* HTTP Status : UNAUTHORIZED - 401 (for case of authN failure)
* HTTP Status : OK - 200 (For all rest cases)
* Body : 
```json
{
    "ResponseMessage": [{
        "responseCode": "api response code",
        "responseMessage": "message text"
    }]
}
```
* HTTP Status : INTERNAL_SERVER_ERROR - 500 (for any other error)

#### Request Retrieval

**API** : `/api/v1/requests/<int:id>`

**HTTP Method** : GET

**Security** : BASIC_AUTH

**Request Body** : None

**Response** :

***success***
* HTTP Status : OK - 200 (For all rest cases)
* Body : 
```json
{
    "requestDetails": [{
        "requestDetails": [{
        "mealType": "Mughlai",
		"mealTime": "Lunch",
		"location": "Wesminster, London",
        "id": 2,
        "user_id": "1",
        "filled": True
    }]
}
```
***failure***
* HTTP Status : UNAUTHORIZED - 401 (for case of authN failure)
* HTTP Status : OK - 200 (For all rest cases)
* Body : 
```json
{
    "ResponseMessage": [{
        "responseCode": "api response code",
        "responseMessage": "message text"
    }]
}
```
* HTTP Status : INTERNAL_SERVER_ERROR - 500 (for any other error)

#### Request Modification

**API** : `/api/v1/requests/<int:id>`

**HTTP Method** : PUT

**Security** : BASIC_AUTH

**Request Body** : 
```json
{
	"requestDetails": [{
		"meanType": "Italian", <STRING, MANDATORY>
		"mealTime: "Lunch", <STRING, MANDATORY>
		"location": "Lag Vegas, Naveda" <STRING, MANDATORY>
	}]
}
```

**Response** :

* HTTP Status : UNAUTHORIZED - 401 (for case of authN failure)
* HTTP Status : OK - 200 (For all rest cases)
* Body : 
```json
{
    "ResponseMessage": [{
       "mealType": "Italian",
		"mealTime": "Dinner",
		"location": "Lag Vegas, Naveda",
        "id": 1,
        "user_id": "2",
        "filled": False
    }]
}
```
* HTTP Status : INTERNAL_SERVER_ERROR - 500 (for any other error)

#### Request Deletion

**API** : `/api/v1/requests/<int:id>`

**HTTP Method** : DELETE

**Security** : BASIC_AUTH

**Request Body** : None

**Response** :

* HTTP Status : UNAUTHORIZED - 401 (for case of authN failure)
* HTTP Status : OK - 200 (For all rest cases)
* Body : 
```json
{
    "ResponseMessage": [{
        "responseCode": "api response code",
        "responseMessage": "message text"
    }]
}
```
* HTTP Status : INTERNAL_SERVER_ERROR - 500 (for any other error)

#### Proposal Creation

**API** : `/api/v1/proposals`

**HTTP Method** : POST

**Security** : BASIC_AUTH

**Request Body** : 
```json
{
	"ProposalDetails": [{
		"requestId": 5 <INT, MANDATORY>
	}]
}
```

**Response** :

* HTTP Status : UNAUTHORIZED - 401 (for case of authN failure)
* HTTP Status : OK - 200 (For all rest cases)
* Body : 
```json
{
    "ResponseMessage": [{
        "responseCode": "api response code",
        "responseMessage": "message text"
    }]
}
```
* HTTP Status : INTERNAL_SERVER_ERROR - 500 (for any other error)

#### Proposals Retrieval

**API** : `/api/v1/proposals`

**HTTP Method** : GET

**Security** : BASIC_AUTH

**Request Body** : None

**Response** :

***success***
* HTTP Status : OK - 200 (For all rest cases)
* Body : 
```json
{
    "ProposalDetails": [{
        "filled": false,
        "id": 1,
        "user_proposed_to": "Jane",
        "user_proposed_from": "Tarzan",
        "request_id": 91
    }, {
        "filled": true,
        "id": 1,
        "user_proposed_to": "Romeo",
        "user_proposed_from": "Juliet",
        "request_id": 12
    }]
}
```
***failure***
* HTTP Status : UNAUTHORIZED - 401 (for case of authN failure)
* HTTP Status : OK - 200 (For all rest cases)
* Body : 
```json
{
    "ResponseMessage": [{
        "responseCode": "api response code",
        "responseMessage": "message text"
    }]
}
```
* HTTP Status : INTERNAL_SERVER_ERROR - 500 (for any other error)

#### Proposals Retrieval

**API** : `/api/v1/proposals`

**HTTP Method** : GET

**Security** : BASIC_AUTH

**Request Body** : None

**Response** :

***success***
* HTTP Status : OK - 200 (For all rest cases)
* Body : 
```json
{
    "ProposalDetails": [{
        "filled": true,
        "id": 1,
        "user_proposed_to": "Romeo",
        "user_proposed_from": "Juliet",
        "request_id": 12
    }]
}
```
***failure***
* HTTP Status : UNAUTHORIZED - 401 (for case of authN failure)
* HTTP Status : OK - 200 (For all rest cases)
* Body : 
```json
{
    "ResponseMessage": [{
        "responseCode": "api response code",
        "responseMessage": "message text"
    }]
}
```
* HTTP Status : INTERNAL_SERVER_ERROR - 500 (for any other error)

#### Proposal Modification

**API** : `/api/v1/proposals/<int:id>`

**HTTP Method** : PUT

**Security** : BASIC_AUTH

**Request Body** : None

**Response** :

* HTTP Status : UNAUTHORIZED - 401 (for case of authN failure)
* HTTP Status : OK - 200 (For all rest cases)
* Body : 
```json
{
    "ResponseMessage": [{
        "responseCode": "api response code",
        "responseMessage": "message text"
    }]
}
```
* HTTP Status : INTERNAL_SERVER_ERROR - 500 (for any other error)

#### Proposal Deletion

**API** : `/api/v1/proposals/<int:id>`

**HTTP Method** : DELETE

**Security** : BASIC_AUTH

**Request Body** : None

**Response** :

* HTTP Status : UNAUTHORIZED - 401 (for case of authN failure)
* HTTP Status : OK - 200 (For all rest cases) (For all rest cases)
* Body : 
```json
{
    "ResponseMessage": [{
        "responseCode": "api response code",
        "responseMessage": "message text"
    }]
}
```
* HTTP Status : INTERNAL_SERVER_ERROR - 500 (for any other error)
