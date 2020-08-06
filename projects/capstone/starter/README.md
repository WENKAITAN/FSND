# Casting Agrency Backend

## Getting started

### Installing Dependencies

### Python 3.8

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Environment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

##### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt or pip3 install -r requirements.txt if you using python3
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) and [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) are libraries to handle the lightweight sqlite database. Since we want you to focus on auth, we handle the heavy lift for you in `./src/database/models.py`. We recommend skimming this code first so you know how to interface with the Drink model.

- [jose](https://python-jose.readthedocs.io/en/latest/) JavaScript Object Signing and Encryption for JWTs. Useful for encoding, decoding, and verifying JWTS.

## Running the server

First, you have to make sure you are working with virtual environment

Each time you open a terminal, you run:

```bash
export FLASK_APP=app.py
export FLASK_ENV=development
```

The `FLASK_ENV=development` flag will detect file changes and restart the server automatically.


To run the server, execute:

```bash
flask run
```

## API

GET '/actors'
- Fetches a list of actors
- Returns json object containing 
```{"success": True, "actors": []}```
- Sample: ```curl http://127.0.0.1:5000/actors -H "Authorization: Bearer <Access_TOKEN>"```
```
{
  "actors": [
    {
      "age": 20,
      "gender": "Male",
      "id": 7,
      "name": "tes"
    },
    {
      "age": 20,
      "gender": "Male",
      "id": 12,
      "name": "test_actor"
    }
  ],
  "success": true
}
```

POST '/actors'
- Creates a new actor to database
- Return a json object containing 
```{"success":True,"created":id,"new_movie":{}}```
- Sample: ```curl -X POST http://127.0.0.1:5000/actors -H "Authorization: Bearer <Access_TOKEN>" -d '{"name":"test","age":"30","gender":"male"}'```
```
{
  "created": 13,
  "new_actor": {
    "age": 30,
    "gender": "Male",
    "id": 13,
    "name": "test"
  },
  "success": true
}
```

PATCH '/actors/<int:id>'
- Updates the actor based on the id
- Return the actors in array or error handler
- Sample: ```curl -X PATCH http://127.0.0.1:5000/actors/id -H "Authorization: Bearer <Access_TOKEN>" -d '{"name":"test","age":"30","gender":"male"}'```

```
{
  "success": true,
  "updated": 7,
  "updated_actor": {
    "age": 30,
    "gender": "feMale",
    "id": 7,
    "name": "test"
  }
}
```
- 
DELETE '/actors/<int:id>'
- Deletes an actor from database based on the id passed in from parameter
- Returns a json object containing
```{"success":True, "actor":id}```
- Sample: ```curl -X DELETE http://127.0.0.1:5000/actors/id -H "Authorization: Bearer <Access_TOKEN>"```

```
{
  "actor": 13,
  "success": true
}
```

GET '/movies'
- Fetches a list of movies
- Returns json object containing 
```{"success": True, "movies": []}```
- Sample: ```curl http://127.0.0.1:5000/movies -H "Authorization: Bearer <Access_TOKEN>"```
```
{
  "movies": [
    {
      "id": 10,
      "release_date": "2020-07-31",
      "title": "test122"
    },
    {
      "id": 4,
      "release_date": "1996-09-09",
      "title": "tenaaaa"
    }
  ],
  "success": true
}
```

POST '/movies'
- Creates a new movie to database
- Return a json object containing 
```{"success":True,"created":id,"new_movie":{}}```
- Sample: ```curl -X POST http://127.0.0.1:5000/movies -H "Authorization: Bearer <Access_TOKEN>" -d '{"title":"test","release_date":"2020-10-01"}'```
```
{
  "created": 15,
  "new_movie": {
    "id": 15,
    "release_date": "2020-10-01",
    "title": "test"
  },
  "success": true
}
```

PATCH '/movies/<int:id>'
- Updates the movie based on the id
- Return the movies in array or error handler
- Sample: ```curl -X PATCH http://127.0.0.1:5000/movies/id -H "Authorization: Bearer <Access_TOKEN>" -d '{"title":"test22","release_date":"2020-10-01"}'```

```
{
  "success": true,
  "updated": "15",
  "updated_movie": {
    "id": 15,
    "release_date": "2020-10-01",
    "title": "test22"
  }
}
```
- 
DELETE '/movies/<int:id>'
- Deletes a movie from database based on the id passed in from parameter
- Returns a json object containing
```{"success":True, "deleted":id}```
- Sample: ```curl -X DELETE http://127.0.0.1:5000/movies/id -H "Authorization: Bearer <Access_TOKEN>"```

```
{
  "deleted": "15",
  "success": true
}
```
