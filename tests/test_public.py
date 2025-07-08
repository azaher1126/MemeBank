from .base_test_class import BaseTestClass

class PublicTests(BaseTestClass):
    def test_home_no_memes(self):
        """Test the home page without memes"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('memes', response.text)

    def test_home_with_memes(self):
        """Test homepage with memes"""
        self.createTestUser()
        meme_id = self.createTestMeme('test meme')
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('memes', response.text)
        self.assertIn(f'meme_{meme_id}', response.text)

    def test_home_meme_lazy_load(self):
        self.createTestUser()
        expected_id = self.createTestMeme('test meme one')
        last_id = self.createTestMeme('test meme two')
        response = self.client.get(f'/?last_id={last_id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn(f'meme_{expected_id}', response.text)
        self.assertNotIn(f'meme_{last_id}', response.text)

    def test_about(self):
        """Test the about page"""
        response = self.client.get('/about')
        self.assertEqual(response.status_code, 200)
        self.assertIn('About', response.text)
