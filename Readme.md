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
		"name": "Ashwin",
		"email": "ashwin.gupta@abc.com",
		"password": "password"
	}]
}
```

**Response** :

* HTTP Status : OK - 200
* Body : 
```json
{
    "ResponseMessage": [{
        "responseCode": "api response code",
        "responseMessage": "message text"
    }]
}
```

#### Users Retrieval

**API** : `/api/v1/users`

**HTTP Method** : GET

**Security** : BASIC_AUTH

**Request Body** : None

**Response** :

***success***
* HTTP Status : OK - 200
* Body : 
```json
{
    "UserDetails": [{
        "email": "ashwin.gupta@abc.com",
        "id": 1,
        "name": "Ashwin"
    }, {
        "email": "rish.imadan@abc.com",
        "id": 2,
        "name": "Rishi"
    }]
}
```
***failure***
* HTTP Status : OK - 200
* Body : 
```json
{
    "ResponseMessage": [{
        "responseCode": "api response code",
        "responseMessage": "message text"
    }]
}
```

#### User Modification

**API** : `/api/v1/users/<int:id>`

**HTTP Method** : PUT

**Security** : BASIC_AUTH

**Request Body** : 
```json
{
	"UserDetails": [{
		"newpassword": "newpassword"
	}]
}
```

**Response** :

* HTTP Status : OK - 200
* Body : 
```json
{
    "ResponseMessage": [{
        "responseCode": "api response code",
        "responseMessage": "message text"
    }]
}
```

#### User Deletion

**API** : `/api/v1/users/<int:id>`

**HTTP Method** : DELETE

**Security** : BASIC_AUTH

**Request Body** : None

**Response** :

* HTTP Status : OK - 200
* Body : 
```json
{
    "ResponseMessage": [{
        "responseCode": "api response code",
        "responseMessage": "message text"
    }]
}