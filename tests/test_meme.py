from io import BytesIO
from os import path
from werkzeug.datastructures import FileStorage

from .base_test_class import BaseTestClass

class MemeTests(BaseTestClass):
    def test_get_meme_image(self):
        """Test retrieving the image for a meme"""
        self.createTestUser()
        meme_id = self.createTestMeme('test meme')
        response = self.client.get(f'/meme/image/{meme_id}')
        self.assertEqual(response.status_code, 200)
        test_meme_image = path.join(self.test_dir, 'test_meme.jpg')
        with open(test_meme_image, 'rb') as meme_image:
            self.assertEqual(response.data, meme_image.read())

    def test_get_nonexisent_meme_image(self):
        """Test retrieving the image for a nonexistent meme"""
        response = self.client.get('/meme/image/nonexistent')
        self.assertEqual(response.status_code, 404)

    def test_view_meme(self):
        """Test viewing a meme page"""
        self.createTestUser()
        meme_id = self.createTestMeme('test meme')
        response = self.client.get(f'/meme/{meme_id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn(f'/meme/image/{meme_id}', response.text)

    def test_meme_search(self):
        """Test searching for memes by tags"""
        self.createTestUser()
        meme_id = self.createTestMeme('testtag')
        response = self.client.get('/search?search=testtag')
        self.assertEqual(response.status_code, 200)
        self.assertIn('testtag', response.text)
        self.assertIn(f'meme_{meme_id}', response.text)

    def test_meme_search_lazy_load(self):
        """Test search meme lazy loading"""
        self.createTestUser()
        expected_id = self.createTestMeme('testtag')
        last_id = self.createTestMeme('testtag')
        response = self.client.get(f'/search?search=testtag&last_id={last_id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn(f'meme_{expected_id}', response.text)
        self.assertNotIn(f'meme_{last_id}', response.text)

    def test_no_result_meme_search(self):
        """Test searching for memes by a nonexistent tag"""
        self.createTestUser()
        meme_id = self.createTestMeme('testtag')
        response = self.client.get('/search?search=nonexistent')
        self.assertEqual(response.status_code, 200)
        self.assertIn('nonexistent', response.text)
        self.assertNotIn('testtag', response.text)
        self.assertNotIn(f'meme_{meme_id}', response.text)

    def test_invalid_search(self):
        """Test search without a query"""
        response = self.client.get('/search')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.location, '/')

    def test_like_meme(self):
        """Test liking a meme"""
        self.createTestUser()
        meme_id = self.createTestMeme('test meme')
        with self.logged_in_context():
            response = self.client.post('/api/like', data=dict(
                id=meme_id
            ))
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.content_type, 'application/json')

    def test_unlike_meme(self):
        """Test unliking a meme"""
        self.createTestUser()
        meme_id = self.createTestMeme('test meme')
        with self.logged_in_context():
            response = self.client.post('/api/unlike', data=dict(
                id=meme_id
            ))
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.content_type, 'application/json')

    def test_upload_meme(self):
        self.createTestUser()
        meme_image = open(path.join(self.test_dir, 'test_meme.jpg'), 'rb')
        meme_file = FileStorage(
            stream=BytesIO(meme_image.read()),
            content_type='image/jpeg',
            filename='randomname.jpg'
        )
        meme_image.close()
        
        with self.logged_in_context():
            response = self.client.post('/upload', data= dict(
                meme=meme_file,
                tags='test meme'
            ), content_type='multipart/form-data')
            self.assertEqual(response.status_code, 302)
            self.assertEqual(response.location, '/')