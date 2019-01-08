# Questioner API 

Questioner API provides endpoints for the [Questioner application](https://github.com/felix45/Questioner) to help meetup organizers prioritize questions to be answered. 

## Required Features

  - Create a user account
  - Sign in a user
  - Create a meetup record
  - Create a question record
  - Confirm attendance to a meetup (RSVP)
  - Upvote on a question record
  - Downvote on a question record
  - Fetch all meetup records
  - Fetch a specific meetup record 

## List of endpoints

| Method | Endpoint | functionality |
|--------|----------|----------|
|  POST  | /api/v1/auth/register     |   Create a user account       |
|  POST  | /api/v1/auth/login     |   Sign in a user       |
|  POST  | /api/v1/meetups     |   Create a meetup record       |
|  GET  | /api/v1/meetups/<meetupid>    | Fetch a specific meetup record. |
|  GET  | /api/v1/meetups/upcoming |   Fetch all upcoming meetup records.       |
|  POST  | /api/v1/questions     |   Create a question for a specific meetup.       |
|  PATCH  | /api/v1/questions/<questionid>/upvote    |  Upvote on a specific question record       |
|  PATCH  | /api/v1/questions/<questionid>/downvote    |  Down vote on a specific question record       |

## Installation

Install python on your computer
- Clone the repository from github and change directory to Questioner

 ``` 
    $ git clone https://github.com/Felix45/Questioner.git
    $ cd Questioner 
```
- Install a virtual environment and activate it 
 ```
  $ virtualenv env
  $ source env/bin/activate
  ````
- Install all the requirements using requirements.txt

``` 
    $ pip install -r requirements.txt 
```
- Start the flask application
 ```
    $ export FLASK_DEBUG=1
    $ export FLASK_ENV=development
    $ export FLASK_APP=run.py
    $ flask run
 ```
 ## Testing Endpoints

 - Install Post Man http client to test the endpoints
 - Open the Post Man test client and enter an endpoint url

  ```http://localhost:5000/api/v1/<endpoint>```

## Tests

- To see the tests you have to use the terminal in a virtual environment
  ``` $ pytest```

   
## Author 

Felix Ouma