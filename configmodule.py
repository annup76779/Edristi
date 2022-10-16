from datetime import timedelta
import os
import json
import pymysql

class Config(object):
    TESTING = False
    SECRET_KEY = 'eYEk_AvjD_bcj0tT_454KfekPntL97zgxXX2lKh5Iis-rxhk'

    # Database Stuff is done here
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    with open(os.path.join(os.path.abspath(os.path.dirname(__name__)), "config.json"),\
         "r", encoding="utf-8") as config:
         config = json.load(config)

    # setting the database URI
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://{username}:{password}@{host}:{port}/{database_name}".format(**config)
    MIGRATION_DIR = "./migrations"

    # jwt stuff is done here
    JWT_SECRET_KEY = 'WEka6Y6hnqBPiKs4Je67qruW8aeoyGyzFlx0q-2vzSQ6JICf' # set this later into environment variable
    JWT_TOKEN_LOCATION = ["headers"]
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=30 * 6)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30 * 12)
    JWT_QUERY_STRING_NAME = "token"
    JWT_QUERY_STRING_VALUE_PREFIX = "Bearer "

    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg',"mp4",}


class Development(Config):
    SQLALCHEMY_ECHO = True

class Production(Config):
    SQLALCHEMY_ECHO = False

class Testing(Config):
    TESTING = True
    SQLALCHEMY_ECHO = True