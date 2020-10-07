# Udacity Fullstack Nanodegree - Project 5 : Capstone Project 

## Content

1. [Introduction](#introduction)
2. [Start Project locally](#start-locally)
3. [API Documentation](#api)
4. [Authentification](#authentification)

<a name="introduction"></a>
## Introduction

This is the last project of the `Udacity-Full-Stack-Nanodegree` Course.
It covers following technical topics in 1 app:

1. Database modeling with `postgres` & `sqlalchemy` (see `models.py`)
2. API to performance CRUD Operations on database with `Flask` (see `app.py`)
3. Automated testing with `Unittest` (see `test_app`)
4. Authorization & Role based Authentification with `Auth0` (see `auth.py`)
5. Deployment to `Heroku`

<a name="start-locally"></a>
## Start Project locally

To start and run the local development server,

1. Initialize and activate a virtualenv:
2. Install the dependencies:
```bash
$ pip install -r requirements.txt
```
To run the app locally, you need to setup the environment variables used inside the code. 

3. Open setup.sh file and update the environment variables.
 ```
export AUTH0_DOMAIN='grajnikanth.us.auth0.com'
export ALGORITHMS='RS256'
export API_AUDIENCE='casting'
export DATABASE_URL="postgres://localhost:5432/capstone"
export TEST_DATABASE_URL="postgres://localhost:5432/test_capstone"
```
AUTH0_DOMAIN - You can setup your own domain name per the project requirements or use the above with the bearer JWT tokens I provided in this readme. Note that the JWT tokens might expire.

API_AUDIENCE - Update this per your AUTH0 settings if not using the above.

DATABASE_URL - This is the Postgres database you want to use with this app.

TEST_DATABASE_URL - This the postgres database you want to use with test_app.py for testing

4. Run the following command to store the environment variables in the local memory
  ```bash 
  $ source setup.sh
  ```
6. Use the ```capstonedb.psql``` to create the example tables ```actors``` and ```movies``` using the following command
 ```bash 
  $ psql yourdbname < capstonedb.psql
  ```

7. Run the development server:
  ```bash 
  $ python app.py
  ```

8. (optional) To execute tests, first create a tables for the test database described above and use ```capstone_test.psql``` file to start test database and run
```bash 
$ python test_app.py
```

## API Documentation
<a name="api"></a>

Here you can find all existing endpoints, which methods can be used, how to work with them & example responses you´ll get.


### Base URL

**_https://raj5uc-fsnd-capstone.herokuapp.com/_**

### Authentification

Please see [API Authentification](#authentification-bearer)

### Available Endpoints

Here is a short table about which resources exist and which method you can use on them.

                          Allowed Methods
       Endpoints    |  GET |  POST |  DELETE | PATCH  |
                    |------|-------|---------|--------|
      /actors       |  [x] |  [x]  |   [x]   |   [x]  |   
      /movies       |  [x] |  [x]  |   [x]   |   [x]  |   

### How to work with each endpoint

Click on a link to directly get to the ressource.

1. Actors
   1. [GET /actors](#get-actors)
   2. [POST /actors](#post-actors)
   3. [DELETE /actors](#delete-actors)
   4. [PATCH /actors](#patch-actors)
2. Movies: Movie endpoints are similar to the actors endpoints. Detailed explanation of these endpoints is not being provided
   1. GET /movies
   2. POST /movies
   3. DELETE /movies
   4. PATCH /movies

Each ressource documentation is clearly structured:
1. Description in a few words
2. `Postman` example to send requests
3. More descriptive explanation of input & outputs.
4. Required permission
5. Example Response.


# <a name="get-actors"></a>
### 1. GET /actors

Query actors.

```
GET https://raj5uc-fsnd-capstone.herokuapp.com/actors
```
- Fetches a list of actors in the database
- Authorization: requires bearer token with permissions to Get Actors - See sample tokens in the end
- Requires permission: `get:actors`
- Returns: 
  1. List of dict of actors with following fields:
      - **integer** `id`
      - **string** `name`
      - **string** `gender`
      - **integer** `age`
  2. **boolean** `success`

#### Example response
```js
{
    "actors": [
        {
            "age": 25,
            "gender": "male",
            "id": 1,
            "name": "Brad"
        },
        {
            "age": 25,
            "gender": "female",
            "id": 2,
            "name": "Jen"
        }
    ],
    "success": true
}
```

# <a name="post-actors"></a>
### 2. POST /actors

Insert new actor into database.

```
POST https://raj5uc-fsnd-capstone.herokuapp.com/actors
```
- Authorization: requires bearer token with permissions to Post Actors - See sample tokens in the end
- Request Arguments: **None**
- Request Headers: (_application/json_)
       1. **string** `name` (<span style="color:red">*</span>required)
       2. **integer** `age` (<span style="color:red">*</span>required)
       3. **string** `gender`
- Requires permission: `post:actors`
- Returns: 
  1. dict `containing the actor just added`
  2. **boolean** `success`

#### Example response
```js
{
    "actor_added": {
        "age": 40,
        "gender": "female",
        "id": 6,
        "name": "Wendy"
    },
    "success": true
}

```

# <a name="patch-actors"></a>
### 3. PATCH /actors

Edit an existing Actor

```
PATCH https://raj5uc-fsnd-capstone.herokuapp.com/actors/1
```
- Authorization: requires bearer token with permissions to update Actors - See sample tokens in the end
- Request Arguments: **integer** `id from actor you want to update`
- Request Headers: (_application/json_)
       1. **string** `name` 
       2. **integer** `age` 
       3. **string** `gender`
- Requires permission: `update:actors`
- Returns: 
  1. **dict** `containing the actor just added`
  2. **boolean** `success`


#### Example response
```js
{
    "actor": {
        "age": 35,
        "gender": "male",
        "id": 1,
        "name": "Brad"
    },
    "success": true
}
```

# <a name="delete-actors"></a>
### 4. DELETE /actors

Delete an existing Actor

```
DELETE https://raj5uc-fsnd-capstone.herokuapp.com/actors/1
```
- Authorization: requires bearer token with permissions to delete Actors - See sample tokens in the end
- Request Arguments: **integer** `id from actor you want to delete`
- Request Headers: `None`
- Requires permission: `delete:actors`
- Returns: 
  1. **dict** `containing the actor just deleted`
  2. **boolean** `success`

#### Example response
```js
{
    "deleted_actor": {
        "age": 40,
        "gender": "female",
        "id": 6,
        "name": "Wendy"
    },
    "success": true
}

```

# <a name="authentification"></a>
## Authentification

All API Endpoints are decorated with Auth0 permissions. To use the project locally, you need to config Auth0 accordingly

### Auth0 for locally use
#### Create an App & API

1. Login to https://manage.auth0.com/ 
2. Click on Applications Tab
3. Create Application
4. Give it a name like `casting` and select "Regular Web Application"
5. Go to Settings and find `domain`. Copy & paste it into setup.sh AUTH0_DOMAIN variable
6. Click on API Tab 
7. Create a new API:
   1. Name: `casting`
   2. Identifier `casting`
   3. Keep Algorithm as it is
8. Go to Settings and find `Identifier`. Copy & paste it into setup.sh API_AUDIENCE' variable

#### Create Roles & Permissions

1. Before creating `Roles & Permissions`, you need to `Enable RBAC` in your API (API => Click on your API Name => Settings = Enable RBAC => Save)
2. Also, check the button `Add Permissions in the Access Token`.
2. First, create a new Role under `Users and Roles` => `Roles` => `Create Roles`
3. Give it a descriptive name like `Casting Assistant`.
4. Go back to the API Tab and find your newly created API. Click on Permissions.
5. Create & assign all needed permissions accordingly 
6. After you created all permissions this app needs, go back to `Users and Roles` => `Roles` and select the role you recently created.
6. Under `Permissions`, assign all permissions you want this role to have. 

# <a name="authentification-bearer"></a>
### Auth0 to use existing API
If you want to access the real, temporary API, bearer tokens for all 3 roles are included at the end of this Readme File

## Existing Roles

They are 3 Roles with distinct permission sets:

1. Casting Assistant:
  - GET /actors (get:actors): Can see all actors
  - GET /movies (get:movies): Can see all movies
2. Casting Director (everything from Casting Assistant plus)
  - POST /actors (post:actors): Can create new Actors
  - PATCH /actors (update:actors): Can edit existing Actors
  - DELETE /actors (delete:actors): Can remove existing Actors from database
  - PATCH /movies (update:movies): Can edit existing Movies
3. Exectutive Dircector (everything from Casting Director plus)
  - POST /movies (post:movies): Can create new Movies
  - DELETE /movies (delete:movies): Can remove existing Motives from database

In your API Calls, add them as Header, with `Authorization` as key and the `Bearer token` as value. Don´t forget to also
prepend `Bearer` to the token (seperated by space).

The latest bearer tokens for the three roles are stored in the config.py file. They are valid for 24 hours starting at 11:00 pm PST 2020-10-06. Please use those to do tests and to make calls to the endpoints. Below I am providing one of those tokens for reference

For example: (Bearer token for `Executive Director`)
```js
{
    "Authorization": "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InJ4MXFWU2QyLW90UXNhb0tacG9waiJ9.eyJpc3MiOiJodHRwczovL2dyYWpuaWthbnRoLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1Zjc2ZDIzZWE1MTFmZTAwNmI3OTk5OGEiLCJhdWQiOiJjYXN0aW5nIiwiaWF0IjoxNjAyMDUwNzQ5LCJleHAiOjE2MDIxMzcxNDksImF6cCI6IlNPR1NEa3FmVkZZUXpSNmNFREVNUjBvWWhVS2dDNFh1Iiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3JzIiwiZGVsZXRlOm1vdmllcyIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicG9zdDphY3RvcnMiLCJwb3N0Om1vdmllcyIsInVwZGF0ZTphY3RvcnMiLCJ1cGRhdGU6bW92aWVzIl19.NNP5_R2tyenYArpluLT-h5tmi6bpb2d-7X8-owh4WlvGBdV7amDcNMRspdyJekqCalvni7GzI-NAybRTq3IOioeumVUxIG0DiVZFV40PfxoUnXmSe4FKKp_SO2hca2nNENWfNdJ2c7MiOY6GD3v0KjmI-DDOYLJ-bHMjrtkcpw9YW6YaIpP7bQrmv-uSsZW0JzJ-g0nxIAP2Dj7l3sBCQ4mQzsPQKX_3vChPm0yDXeHop-7dncGs1TUVEt44G0sbiVQkTHe1Y0kWmdq3Bne106L-7ue3vFMQpdGM4JYXEz1P3WkTExF49iQLK39yQcczLuZQKX9RdwCIf9p51Gxh_g"
}
```
