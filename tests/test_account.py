from base_test_class import BaseTestClass

class AccountTests(BaseTestClass):
    def test_logged_in_home(self):
        """Test the logged in home page"""
        self.createTestUser()
        with self.logged_in_context():
            response = self.client.get('/')
            self.assertEqual(response.status_code, 200)
            self.assertIn('memes', response.text)
            self.assertIn(AccountTests.TEST_USERNAME, response.text)

    def test_logged_in_anonymous_only(self):
        """Test anonymous only"""
        self.createTestUser()
        with self.logged_in_context():
            response = self.client.get('/login')
            self.assertEqual(response.status_code, 302)
            self.assertEqual(response.location, '/')

    def test_login_user_email(self):
        """Test logging in a user"""
        self.createTestUser()
        response = self.client.post('/login', data=dict(
            username_or_email=AccountTests.TEST_USER_EMAIL,
            password=AccountTests.TEST_USER_PASSWORD
        ))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.location, '/')

    def test_login_user_username(self):
        """Test logging in a user"""
        self.createTestUser()
        response = self.client.post('/login', data=dict(
            username_or_email=AccountTests.TEST_USERNAME,
            password=AccountTests.TEST_USER_PASSWORD
        ))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.location, '/')
    
    def test_login_missing_info(self):
        """Test login without all the info"""
        self.createTestUser()
        response = self.client.post('/login', data=dict(
            username_or_email=AccountTests.TEST_USER_EMAIL,
        ))
        self.assertEqual(response.status_code, 200)
        self.assertIn('Error in the Password field - This field is required', response.text)

    def test_login_invalid_password(self):
        """Test login with the wrong password"""
        self.createTestUser()
        response = self.client.post('/login', data=dict(
            username_or_email=AccountTests.TEST_USER_EMAIL,
            password="TheWrongPassword"
        ))
        self.assertEqual(response.status_code, 200)
        self.assertIn('Incorrect password', response.text)

    def test_login_invalid_email(self):
        self.createTestUser()
        response = self.client.post('/login', data=dict(
            username_or_email='nonexistent@memebank.com',
            password="TheWrongPassword"
        ))
        self.assertEqual(response.status_code, 200)
        self.assertIn('Email does not exist', response.text)

    def test_visit_user_profile(self):
        self.createTestUser()
        response = self.client.get(f'/profile/{AccountTests.TEST_USERNAME}')
        self.assertEqual(response.status_code, 200)
        self.assertIn('memes', response.text)
        self.assertIn(AccountTests.TEST_USERNAME, response.text)

    def test_visit_nonexistent_user_profile(self):
        self.createTestUser()
        response = self.client.get('/profile/nonexistent')
        self.assertEqual(response.status_code, 404)