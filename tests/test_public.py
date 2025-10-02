from .base_test_class import BaseTestClass

class PublicTests(BaseTestClass):
    def test_home_no_memes(self):
        """Test the home page without memes"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('memes', response.text)

    def test_home_with_memes(self):
        """Test homepage with memes"""
        user_id = self.createTestUser()
        meme_id = self.createTestMeme(user_id, 'test meme')
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('memes', response.text)
        self.assertIn(f'data-meme-id="{meme_id}"', response.text)

    def test_home_meme_lazy_load(self):
        user_id = self.createTestUser()
        expected_id = self.createTestMeme(user_id, 'test meme one')
        last_id = self.createTestMeme(user_id, 'test meme two')
        response = self.client.get(f'/?last_id={last_id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn(f'data-meme-id="{expected_id}"', response.text)
        self.assertNotIn(f'data-meme-id="{last_id}"', response.text)

    def test_home_meme_lazy_load_nonexistent(self):
        response = self.client.get(f'/?last_id=1')
        self.assertEqual(response.status_code, 404)

    def test_about(self):
        """Test the about page"""
        response = self.client.get('/about')
        self.assertEqual(response.status_code, 200)
        self.assertIn('About', response.text)
