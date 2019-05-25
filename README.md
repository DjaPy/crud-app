# Description

A simple application in the style of ReST Api. Implements CRUD database operation via ReST.

# CRUD app

The app consists of three microservices.

- The application server is written in [Flask](http://flask.pocoo.org/). Uses additional libraries to speed up development (connexion, flask-login, flask-sqlalchemy, marshmallow, etc.).
Gunicorn python WSGI HTTP server is used to connect the proxy server to the application server.

- Proxy server on nginx with basic settings.
 
- PostgreSQL database of the latest version. With basic settings.

Data of database and application server are stored in data storage.

# Build and run

- Clone the repository to your computer.
- Configure `example.env` and rename to `.env`.
- From the root directory of the project, run the `docker-compose build`.
- Start docker-compose `docker-compose up -d`
- Create a database and write the initial data to the tables `docker-compose run web /usr/local/bin/python db_build.py`
- The app is ready to use.

# How to use

After the application is successfully deployed, you must log in or register.
```
default login    - admin
default password - qwerty
```

