from os import path
from .base_test_class import BaseTestClass

class AccountTests(BaseTestClass):
    def test_logged_in_home(self):
        """Test the logged in home page"""
        user_id = self.createTestUser()
        with self.logged_in_context(user_id):
            response = self.client.get('/')
            self.assertEqual(response.status_code, 200)
            self.assertIn('memes', response.text)
            self.assertIn(AccountTests.TEST_USERNAME_TEMPLATE.format(user_id), response.text)

    def test_logged_in_anonymous_only(self):
        """Test anonymous only"""
        user_id = self.createTestUser()
        with self.logged_in_context(user_id):
            response = self.client.get('/login')
            self.assertEqual(response.status_code, 302)
            self.assertEqual(response.location, '/')

    def test_login_user_email(self):
        """Test logging in a user by email"""
        user_id = self.createTestUser()
        response = self.client.post('/login', data=dict(
            username_or_email=AccountTests.TEST_USER_EMAIL_TEMPLATE.format(user_id),
            password=AccountTests.TEST_USER_PASSWORD
        ))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.location, '/')

    def test_login_user_username(self):
        """Test logging in a user by username"""
        user_id = self.createTestUser()
        response = self.client.post('/login', data=dict(
            username_or_email=AccountTests.TEST_USERNAME_TEMPLATE.format(user_id),
            password=AccountTests.TEST_USER_PASSWORD
        ))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.location, '/')
    
    def test_login_missing_info(self):
        """Test login without all the info"""
        user_id = self.createTestUser()
        response = self.client.post('/login', data=dict(
            username_or_email=AccountTests.TEST_USER_EMAIL_TEMPLATE.format(user_id),
        ))
        self.assertEqual(response.status_code, 200)
        self.assertIn('Error in the Password field - This field is required', response.text)

    def test_login_invalid_password(self):
        """Test login with the wrong password"""
        user_id = self.createTestUser()
        response = self.client.post('/login', data=dict(
            username_or_email=AccountTests.TEST_USER_EMAIL_TEMPLATE.format(user_id),
            password="TheWrongPassword"
        ))
        self.assertEqual(response.status_code, 200)
        self.assertIn('Incorrect password', response.text)

    def test_login_invalid_email(self):
        response = self.client.post('/login', data=dict(
            username_or_email='nonexistent@memebank.com',
            password="TheWrongPassword"
        ))
        self.assertEqual(response.status_code, 200)
        self.assertIn('Email or username does not exist', response.text)

    def test_register_user(self):
        response = self.client.post('/register', data=dict(
            username=AccountTests.TEST_USERNAME_TEMPLATE.format(1),
            first_name=AccountTests.TEST_FIRST_NAME,
            last_name=AccountTests.TEST_LAST_NAME,
            email=AccountTests.TEST_USER_EMAIL_TEMPLATE.format(1),
            password=AccountTests.TEST_USER_PASSWORD,
            confirm_password=AccountTests.TEST_USER_PASSWORD
        ))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.location, '/')

    def test_register_user_missing_info(self):
        response = self.client.post('/register', data=dict(
            username=AccountTests.TEST_USERNAME_TEMPLATE.format(1),
            last_name=AccountTests.TEST_LAST_NAME,
            email=AccountTests.TEST_USER_EMAIL_TEMPLATE.format(1),
            password=AccountTests.TEST_USER_PASSWORD,
            confirm_password=AccountTests.TEST_USER_PASSWORD
        ))
        self.assertEqual(response.status_code, 200)
        self.assertIn('Error in the First Name field - This field is required', response.text)

    def test_register_existent_email(self):
        self.createTestUser()
        response = self.client.post('/register', data=dict(
            username=AccountTests.TEST_USERNAME_TEMPLATE.format(1),
            first_name=AccountTests.TEST_FIRST_NAME,
            last_name=AccountTests.TEST_LAST_NAME,
            email=AccountTests.TEST_USER_EMAIL_TEMPLATE.format(1),
            password=AccountTests.TEST_USER_PASSWORD,
            confirm_password=AccountTests.TEST_USER_PASSWORD
        ))
        self.assertEqual(response.status_code, 200)
        self.assertIn('Email already belongs to an account', response.text)

    def test_register_existent_username(self):
        user_id = self.createTestUser()
        response = self.client.post('/register', data=dict(
            username=AccountTests.TEST_USERNAME_TEMPLATE.format(user_id),
            first_name=AccountTests.TEST_FIRST_NAME,
            last_name=AccountTests.TEST_LAST_NAME,
            email='nonexistent@membank.com',
            password=AccountTests.TEST_USER_PASSWORD,
            confirm_password=AccountTests.TEST_USER_PASSWORD
        ))
        self.assertEqual(response.status_code, 200)
        self.assertIn('Username already exists', response.text)

    def test_logout(self):
        user_id = self.createTestUser()
        with self.logged_in_context(user_id):
            response = self.client.get('/logout')
            self.assertEqual(response.status_code, 302)
            self.assertEqual(response.location, '/')

    def test_logout_protected_next(self):
        user_id = self.createTestUser()
        with self.logged_in_context(user_id):
            response = self.client.get('/logout?next=/upload')
            self.assertEqual(response.status_code, 302)
            self.assertEqual(response.location, '/')

    def test_logout_nonexistent_next(self):
        user_id = self.createTestUser()
        with self.logged_in_context(user_id):
            self.assertRaises(ValueError, self.client.get, '/logout?next=/nonexistent')

    def test_visit_user_profile(self):
        user_id = self.createTestUser()
        response = self.client.get(f'/profile/{AccountTests.TEST_USERNAME_TEMPLATE.format(user_id)}')
        self.assertEqual(response.status_code, 200)
        self.assertIn('memes', response.text)
        self.assertIn(AccountTests.TEST_USERNAME_TEMPLATE.format(user_id), response.text)

    def test_profile_meme_lazy_load(self):
        user_id = self.createTestUser()
        expected_id = self.createTestMeme(user_id, 'test meme one')
        last_id = self.createTestMeme(user_id, 'test meme two')
        response = self.client.get(f'/profile/{AccountTests.TEST_USERNAME_TEMPLATE.format(user_id)}?last_id={last_id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn(f'data-meme-id="{expected_id}"', response.text)
        self.assertNotIn(f'data-meme-id="{last_id}"', response.text)

    def test_profile_meme_lazy_load_nonexistent(self):
        user_id = self.createTestUser()
        response = self.client.get(f'/profile/{AccountTests.TEST_USERNAME_TEMPLATE.format(user_id)}?last_id=1')
        self.assertEqual(response.status_code, 404)

    def test_visit_nonexistent_user_profile(self):
        response = self.client.get('/profile/nonexistent')
        self.assertEqual(response.status_code, 404)

    def test_get_nonexistent_profile_image(self):
        """Test retrieve nonexistent profile image"""
        response = self.client.get('/profile/image/nonexistent')
        self.assertEqual(response.status_code, 404)

    def test_get_unset_profile_image(self):
        """Test retrieve of unset profile image"""
        user_id = self.createTestUser()
        response = self.client.get(f'/profile/image/{user_id}')
        self.assertEqual(response.status_code, 200)
        default_profile_path = path.join(self.app.config['ASSETS_DIR_PATH'],'default_profile.jpg')
        with open(default_profile_path, 'rb') as default_profile:
            self.assertEqual(response.data, default_profile.read())

    def test_anonymous_forget_password(self):
        """Test that the forgot password page is accessible when not logged in"""
        response = self.client.get('/forget_password')
        self.assertEqual(response.status_code, 200)

    def test_logged_in_forget_password(self):
        """Test that the forgot password page redirects when logged in"""
        user_id = self.createTestUser()
        with self.logged_in_context(user_id):
            response = self.client.get('/forget_password')
            self.assertEqual(response.status_code, 302)
            self.assertEqual(response.location, '/')
