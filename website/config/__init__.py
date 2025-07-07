from os import environ
from secrets import token_hex

class Config():
    def __init__(self):
        self.SECRET_KEY = environ.get("SECRET_KEY")
        self.RECAPTCHA_PUBLIC_KEY = environ.get("RECAPTCHA_PUBLIC_KEY")
        self.RECAPTCHA_PRIVATE_KEY = environ.get("RECAPTCHA_PRIVATE_KEY")
        self.UPLOADS_BASE_PATH = environ.get("UPLOADS_BASE_PATH")
        self.DB_PATH = environ.get('DB_PATH')

class DevelopmentConfig(Config):
    def __init__(self):
        super().__init__()
        if not self.SECRET_KEY:
            raise Exception("SECRET_KEY must be provided in .env file.")
        if not self.RECAPTCHA_PUBLIC_KEY:
            raise Exception("RECAPTCHA_PUBLIC_KEY must be provided in .env file.")
        if not self.RECAPTCHA_PRIVATE_KEY:
            raise Exception("RECAPTCHA_PRIVATE_KEY must be provided in .env file.")

class TestConfig(Config):
    def __init__(self, db_path, uploads_base_path):
        super().__init__()

        self.DB_PATH = db_path
        self.UPLOADS_BASE_PATH = uploads_base_path
        if not self.SECRET_KEY:
            self.SECRET_KEY = token_hex()
        if not self.RECAPTCHA_PUBLIC_KEY:
            self.RECAPTCHA_PUBLIC_KEY = ''
        if not self.RECAPTCHA_PRIVATE_KEY:
            self.RECAPTCHA_PRIVATE_KEY = ''
        self.TESTING = True
        self.WTF_CSRF_ENABLED = False