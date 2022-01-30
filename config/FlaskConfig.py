import os
from config.PostgreConfig import DB_USER, DB_PASS, DB_NAME, DB_HOST, DB_PORT

SECRET_KEY = "Super_secret_code"  # os.urandom(30)
DEBUG = False
TESTING = False
UPLOAD_FOLDER = "static/img/"
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"