from .base_test_class import BaseTestClass

class SettingsTests(BaseTestClass):
    def test_profile_settings_accessible_logged_in(self):
        self.createTestUser()
        with self.logged_in_context():
            response = self.client.get('/settings/profile')
            self.assertEqual(response.status_code, 200)

    def test_profile_settings_accessible_anonymous(self):
        response = self.client.get('/settings/profile')
        self.assertEqual(response.status_code, 302)
        self.assertStartsWith(response.location, "/login")

    def test_account_settings_accessible_logged_in(self):
        self.createTestUser()
        with self.logged_in_context():
            response = self.client.get('/settings/account')
            self.assertEqual(response.status_code, 200)

    def test_account_settings_accessible_anonymous(self):
        response = self.client.get('/settings/account')
        self.assertEqual(response.status_code, 302)
        self.assertStartsWith(response.location, "/login")