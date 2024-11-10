from base_test_class import BaseTestClass

class PublicTests(BaseTestClass):
    def test_home(self):
        """Test the home page"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('memes', response.text)

    def test_about(self):
        """Test the about page"""
        response = self.client.get('/about')
        self.assertEqual(response.status_code, 200)
        self.assertIn('About', response.text)
