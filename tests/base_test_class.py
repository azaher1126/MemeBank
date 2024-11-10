import unittest
from uuid import uuid4
from os import path, mkdir, remove, rmdir
from contextlib import contextmanager
from flask_migrate import stamp
from flask_login import login_user, logout_user
from werkzeug.security import generate_password_hash

from website import create_app
from website.database import db
from website.database.user_model import User
from website.config import TestConfig

class BaseTestClass(unittest.TestCase):
    TEST_USER_EMAIL = "unittest@memebank.com"
    TEST_USERNAME = "unittest"
    TEST_FIRST_NAME = "Unit"
    TEST_LAST_NAME = "Test"
    TEST_USER_PASSWORD = "TestPassword1"

    @classmethod
    def setUpClass(cls) -> None:
        test_dir = path.join(path.dirname(path.realpath(__file__)),'testData')
        if not path.exists(test_dir):
            mkdir(test_dir)
        cls.uploads_dir = path.join(test_dir, 'uploads')
        if not path.exists(cls.uploads_dir):
            mkdir(cls.uploads_dir)
        cls.db_path = path.join(test_dir, f'{uuid4()}.db')
        test_config = TestConfig(cls.db_path, cls.uploads_dir)
        cls.app = create_app(test_config)

    @classmethod
    def tearDownClass(cls) -> None:
        with cls.app.app_context():
            db.engine.dispose()
            remove(cls.db_path)
        rmdir(cls.uploads_dir)

    def setUp(self) -> None:
        self.client = self.app.test_client()
        return super().setUp()
    
    def tearDown(self) -> None:
        # Clean database for next test case
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
            db.create_all()
            stamp()

    def createTestUser(self):
        with self.app.app_context():
            test_user = User(email=BaseTestClass.TEST_USER_EMAIL, username=BaseTestClass.TEST_USERNAME,
                        first_name=BaseTestClass.TEST_FIRST_NAME, last_name=BaseTestClass.TEST_LAST_NAME,
                        password=generate_password_hash(BaseTestClass.TEST_USER_PASSWORD))
            db.session.add(test_user)
            db.session.commit()
            self.test_user_id = test_user.id

    @contextmanager
    def logged_in_context(self):
        with self.app.test_request_context():
            test_user = db.session.query(User).filter(User.id == self.test_user_id).first()
            login_user(test_user)
            yield
