import os
SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Connect to the database


# TODO IMPLEMENT DATABASE URL
SQLALCHEMY_DATABASE_URI = "postgres://lztafuneddfxyl:3cac819a266aaa393675ddef33fd7c71c04f2125d0672797d7e869b3b846530d@ec2-18-233-32-61.compute-1.amazonaws.com:5432/d4b971oefj93ko" 
