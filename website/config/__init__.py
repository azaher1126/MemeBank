from os import environ
from secrets import token_hex
from dotenv import load_dotenv
import logging

load_dotenv()

class Config():
    def __init__(self):
        self.SECRET_KEY = environ.get("SECRET_KEY")
        self.RECAPTCHA_PUBLIC_KEY = environ.get("RECAPTCHA_PUBLIC_KEY")
        self.RECAPTCHA_PRIVATE_KEY = environ.get("RECAPTCHA_PRIVATE_KEY")
        self.UPLOADS_BASE_PATH = environ.get("UPLOADS_BASE_PATH")
        self.DB_PATH = environ.get('DB_PATH')
        self.APP_PORT = int(environ.get('APP_PORT', 5000))

class DevelopmentConfig(Config):
    def __init__(self):
        super().__init__()
        if not self.SECRET_KEY:
            self.SECRET_KEY = token_hex()
            logger = logging.getLogger(__name__)
            logger.warning("WARNING: SECRET_KEY not set in environment or .env file. Using a random key for development. This will not work in production.")
        if not self.RECAPTCHA_PUBLIC_KEY or not self.RECAPTCHA_PRIVATE_KEY:
            self.RECAPTCHA_PUBLIC_KEY = ''
            self.RECAPTCHA_PRIVATE_KEY = ''
            self.TESTING = True

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