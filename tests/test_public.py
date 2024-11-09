from base_test_class import BaseTestClass

class PublicTests(BaseTestClass):
    def test_home(self):
        """Test the home page"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
