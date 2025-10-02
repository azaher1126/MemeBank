import unittest
from uuid import uuid4
from os import path, mkdir, remove, rmdir
from shutil import copyfile, rmtree
from contextlib import contextmanager
from flask_migrate import stamp
from flask_login import login_user
from werkzeug.security import generate_password_hash

from website import create_app
from website.database import db
from website.database.user_model import User
from website.database.meme_model import Meme
from website.database.tag_model import Tag
from website.config import TestConfig

class BaseTestClass(unittest.TestCase):
    TEST_USER_EMAIL_TEMPLATE = "unittest_{}@memebank.com"
    TEST_USERNAME_TEMPLATE = "unittest_{}"
    TEST_FIRST_NAME = "Unit"
    TEST_LAST_NAME = "Test"
    TEST_USER_PASSWORD = "TestPassword1"

    @classmethod
    def setUpClass(cls) -> None:
        cls.test_dir = path.join(path.dirname(path.realpath(__file__)),'testData')
        if not path.exists(cls.test_dir):
            mkdir(cls.test_dir)
        cls.uploads_dir = path.join(cls.test_dir, 'uploads')
        if not path.exists(cls.uploads_dir):
            mkdir(cls.uploads_dir)
        cls.db_path = path.join(cls.test_dir, f'{uuid4()}.db')
        test_config = TestConfig(cls.db_path, cls.uploads_dir)
        cls.app = create_app(test_config)

    @classmethod
    def tearDownClass(cls) -> None:
        with cls.app.app_context():
            db.engine.dispose()
            remove(cls.db_path)
        rmtree(cls.uploads_dir)

    def setUp(self) -> None:
        self.client = self.app.test_client()
        self.test_user_ids = []
        return super().setUp()
    
    def tearDown(self) -> None:
        # Clean database for next test case
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
            db.create_all()
            stamp()

    def createTestUser(self) -> int:
        next_id = self.test_user_ids[-1] + 1 if len(self.test_user_ids) > 0 else 1
        test_email = BaseTestClass.TEST_USER_EMAIL_TEMPLATE.format(next_id)
        test_username = BaseTestClass.TEST_USERNAME_TEMPLATE.format(next_id)
        with self.app.app_context():
            test_user = User(email=test_email, username=test_username,
                        first_name=BaseTestClass.TEST_FIRST_NAME, last_name=BaseTestClass.TEST_LAST_NAME,
                        password=generate_password_hash(BaseTestClass.TEST_USER_PASSWORD))
            db.session.add(test_user)
            db.session.commit()
            self.test_user_ids.append(test_user.id)
            return test_user.id

    def createTestMeme(self, user_id: int, tags: str) -> int:
        meme_image = path.join(self.test_dir, 'test_meme.jpg')
        meme_uploads_dir = path.join(self.uploads_dir, 'memes')
        if not path.exists(meme_uploads_dir):
            mkdir(meme_uploads_dir)
        copyfile(meme_image, path.join(meme_uploads_dir, 'test_meme.jpg'))
        split_tags = tags.split()
        with self.app.app_context():
            test_meme = Meme(user_id=user_id, url='test_meme.jpg')

            for split_tag in split_tags:
                dbTag = db.session.query(Tag).filter(Tag.name==split_tag).one_or_none()
                if not dbTag:
                    dbTag = Tag(name=split_tag)
                test_meme.tags.append(dbTag)

            db.session.add(test_meme)
            db.session.commit()
            return test_meme.id
        
    def createTag(self, tag: str):
        with self.app.app_context():
            test_tag = Tag(name=tag)
            db.session.add(test_tag)
            db.session.commit()
        
    def likeMeme(self, meme_id: int, user_id: int):
        with self.app.app_context():
            test_meme = db.session.query(Meme).filter(Meme.id == meme_id).one_or_none()
            if not test_meme:
                raise ValueError(f"The meme with id {meme_id} does not exist.")
            test_user = db.session.query(User).filter(User.id == user_id).one_or_none()
            if not test_user:
                raise ValueError(f"The user with id {user_id} does not exist.")
            test_meme.users_liked.append(test_user)
            db.session.commit()

    @contextmanager
    def logged_in_context(self, user_id: int | None = None):
        if not user_id:
            user_id = self.test_user_ids[0]
        with self.app.test_request_context():
            test_user = db.session.query(User).filter(User.id == user_id).one()
            login_user(test_user)
            yield

    def assertStartsWith(self, actual: str, start: str):
        self.assertTrue(actual.startswith(start), f"Expected '{actual}' to start with '{start}'.")
