# sg

## Description

This exercise has been built using Flask, SQLAlchemy and JWT for authentication. I used a [docker image by tiangolo](https://github.com/tiangolo/uwsgi-nginx-flask-docker), with nginx, python and flask
installed and docker-compose to run, build and configure.

I used pip and a requirements.txt file to install the extra pieces of sofware i needed.

## Build and Run

    docker-compose build
    docker-compose up

Once finished, you can reach api root [here](http://locahost)


## Endpoints calls

### /auth

Authentication endpoint. Here we can get the access_token (jwt) that we will use to reach the non public endpoints

input:

    curl -X POST -H "Accept:application/json" -H "Content-Type:application/json" -d '{"username": "testuser2", "password": "abcxyz"}' http://localhost/auth

output:

        {
            "access_token": "TOKEN"

        }

This token will expire in 5 minutes

### /artists
List of artists (public endpoint)

input:

    curl -X GET -H "Accept:application/json" -H "Content-Type:application/json"  http://localhost/artists?page=1&size=2


output:

    {
    "data": [
        {
          "id": 1,
          "name": "AC/DC"
        },
        {
          "id": 2,
          "name": "Accept"
        }
      ],
    "meta": {
        "page": 1,
        "size": 2
    }
    }


### /artists/:id/albums
List of albums for one artist (restricted to authenticated users)

input:

    curl -X GET -H "Accept:application/json" -H "Content-Type:application/json" -H "Authorization: JWT ${TOKEN}" http://localhost/artists/1/albums


output:

    {
    "albums": [
        "For Those About To Rock We Salute You",
        "Let There Be Rock"
    ],
    "artist name": "AC/DC"
    }


### /albums
List of albums with songs (restricted to authenticated users)

input:

    curl -X GET -H "Accept:application/json" -H "Content-Type:application/json" -H "Authorization: JWT ${TOKEN}" "http://localhost/albums?page=2&size=2"


output:

    {
      "data": [
        {
          "album": "Restless and Wild",
          "tracks": [
            "Fast As a Shark",
            "Restless and Wild",
            "Princess of the Dawn"
          ]
        },
        {
          "album": "Let There Be Rock",
          "tracks": [
            "Go Down",
            "Dog Eat Dog",
            "Let There Be Rock",
            "Bad Boy Boogie",
            "Problem Child",
            "Overdose",
            "Hell Ain't A Bad Place To Be",
            "Whole Lotta Rosie"
          ]
        }
      ],
      "meta": {
        "page": 2,
        "size": 2
      }
    }


### /albums/advanced
List of albums, including artist name, track count, total album duration (sum of
tracks duration), longest track duration and shortest track duration. (restricted
to authenticated users)

input:

    curl -X GET -H "Accept:application/json" -H "Content-Type:application/json" -H "Authorization: JWT ${TOKEN}" "http://localhost/albums/advanced?page=2&size=2"


output:

    {
      "data": [
        {
          "album": "Restless and Wild", 
          "artist": "Accept", 
          "longest duration": 375418, 
          "shortest duration": 230619, 
          "total duration": 858088
        }, 
        {
          "album": "Let There Be Rock", 
          "artist": "AC/DC", 
          "longest duration": 369319, 
          "shortest duration": 215196, 
          "total duration": 2453259
        }
      ], 
      "meta": {
        "page": 2, 
        "size": 2
      }
    }

### /passphrase/basic
A passphrase consists of a series of words (lowercase letters) separated by spaces. To
ensure security, a valid passphrase must contain no duplicate words.

input:

    curl -X POST "http://localhost/passphrase/basic" -H  "accept: application/json" -H  "Content-Type: application/json" -d '{"passphrase": "aa bb cc dd ee\naa bb cc dd aa"}'

output:

### /passphrase/advanced
For added security, yet another system policy has been put in place. Now, a valid
passphrase must contain no two words that are anagrams of each other - that is, a
passphrase is invalid if any word's letters can be rearranged to form any other word in
the passphrase.

input:

    curl -X POST "http://localhost/passphrase/advanced" -H  "accept: application/json" -H  "Content-Type: application/json" -d '{"passphrase": "aa bb cc dd ee\naa bb cc dd aa"}'


output:

    {
      "total passphrases": 2,
      "valid passphrases": 1
    }

## Tests

Once the cointainer is up, run


    docker exec -t sg_app pytest

25 tests are testing the endpoints. Functionality is so simple that I think these test are enough.

## Source Code and implementation facts.


### Database
As we had a database previously built, we generated models from database using the sqlalchemy automap extension ( *app/config/database.py* )
connexxion
connexxionconnexxion
### Authentication
We used [flask-jwt](https://pythonhosted.org/Flask-JWT/) flask extension. In order to simplify the code, we stored *usernames* and *passwords* in a static dictionary instead of storing them in database ( *app/config/api_users.py* )

### Endpoint routes

All endpoint definitions are placed in *app/config/routes.py* using blueprint.

## Improvements

We always could do more tests, for sure.

Documentation, we could use OpenAPI Specification (Swagger Spec) to document and give a sandbox to play and know the api.

Validation, serialization/deserialization. We almost did nothing about, we could do it ourselves or use [marsmallow](https://marshmallow.readthedocs.io/en/stable/)
