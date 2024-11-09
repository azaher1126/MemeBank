import unittest
from uuid import uuid4
from os import path, mkdir, remove, rmdir

from website import create_app
from website.database import db
from website.config import TestConfig

class BaseTestClass(unittest.TestCase):
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
            db.session.remove()
            db.engine.dispose()
            remove(cls.db_path)
        rmdir(cls.uploads_dir)

    def setUp(self) -> None:
        self.client = self.app.test_client()
        return super().setUp()
    