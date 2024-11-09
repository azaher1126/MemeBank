from os import environ
from secrets import token_hex

class Config():
    SECRET_KEY = environ.get("SECRET_KEY")
    RECAPTCHA_PUBLIC_KEY = environ.get("RECAPTCHA_PUBLIC_KEY")
    RECAPTCHA_PRIVATE_KEY = environ.get("RECAPTCHA_PRIVATE_KEY")
    UPLOADS_BASE_PATH = environ.get("UPLOADS_BASE_PATH")
    DB_PATH = environ.get('DB_PATH')

class DevelopmentConfig(Config):
    if not Config.SECRET_KEY:
        raise Exception("SECRET_KEY must be provided in .env file.")
    if not Config.RECAPTCHA_PUBLIC_KEY:
        raise Exception("RECAPTCHA_PUBLIC_KEY must be provided in .env file.")
    if not Config.RECAPTCHA_PRIVATE_KEY:
        raise Exception("RECAPTCHA_PRIVATE_KEY must be provided in .env file.")

class TestConfig(Config):
    if not Config.SECRET_KEY:
        SECRET_KEY = token_hex()
    if not Config.RECAPTCHA_PUBLIC_KEY:
        RECAPTCHA_PUBLIC_KEY = ''
    if not Config.RECAPTCHA_PRIVATE_KEY:
        RECAPTCHA_PRIVATE_KEY = ''
    TESTING = True