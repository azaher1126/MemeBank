from io import BytesIO
from os import path
from werkzeug.datastructures import FileStorage

from .base_test_class import BaseTestClass

class MemeTests(BaseTestClass):
    def test_get_meme_image(self):
        """Test retrieving the image for a meme"""
        user_id = self.createTestUser()
        meme_id = self.createTestMeme(user_id, 'test meme')
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
        user_id = self.createTestUser()
        meme_id = self.createTestMeme(user_id, 'test meme')
        response = self.client.get(f'/meme/{meme_id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn(f'/meme/image/{meme_id}', response.text)

    def test_view_nonexistent_meme(self):
        response = self.client.get(f'/meme/1')
        self.assertEqual(response.status_code, 404)

    def test_meme_search(self):
        """Test searching for memes by tags"""
        user_id = self.createTestUser()
        meme_id = self.createTestMeme(user_id, 'testtag')
        response = self.client.get('/search?search=testtag')
        self.assertEqual(response.status_code, 200)
        self.assertIn('testtag', response.text)
        self.assertIn(f'data-meme-id="{meme_id}"', response.text)

    def test_meme_search_lazy_load(self):
        """Test search meme lazy loading"""
        user_id = self.createTestUser()
        expected_id = self.createTestMeme(user_id, 'testtag')
        last_id = self.createTestMeme(user_id, 'testtag')
        response = self.client.get(f'/search?search=testtag&last_id={last_id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn(f'data-meme-id="{expected_id}"', response.text)
        self.assertNotIn(f'data-meme-id="{last_id}"', response.text)

    def test_no_result_meme_search(self):
        """Test searching for memes by a nonexistent tag"""
        user_id = self.createTestUser()
        meme_id = self.createTestMeme(user_id, 'testtag')
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
        user_id = self.createTestUser()
        meme_id = self.createTestMeme(user_id, 'test meme')
        with self.logged_in_context(user_id):
            response = self.client.post('/api/toggleLike', data=dict(
                id=meme_id
            ))
            self.assertEqual(response.status_code, 200)
            self.assertIn("#unlike-icon", response.text)

    def test_unlike_meme(self):
        """Test unliking a meme"""
        user_id = self.createTestUser()
        meme_id = self.createTestMeme(user_id, 'test meme')
        self.likeMeme(meme_id, user_id)
        with self.logged_in_context(user_id):
            response = self.client.post('/api/toggleLike', data=dict(
                id=meme_id
            ))
            self.assertEqual(response.status_code, 200)
            self.assertIn("#like-icon", response.text)

    def test_toggleLike_logged_out(self):
        user_id = self.createTestUser()
        meme_id = self.createTestMeme(user_id, "test meme")
        response = self.client.post('/api/toggleLike', data=dict(
            id=meme_id
        ))
        self.assertEqual(response.status_code, 401)

    def test_toggleLike_invalid_request(self):
        user_id = self.createTestUser()
        with self.logged_in_context(user_id):
            response = self.client.post('/api/toggleLike', data=dict())
            self.assertEqual(response.status_code, 400)

    def test_toggleLike_nonexistent_meme(self):
        user_id = self.createTestUser()
        with self.logged_in_context(user_id):
            response = self.client.post('/api/toggleLike', data=dict(
                id=1
            ))
            self.assertEqual(response.status_code, 404)

    def test_upload_meme(self):
        user_id = self.createTestUser()
        meme_image = open(path.join(self.test_dir, 'test_meme.jpg'), 'rb')
        meme_file = FileStorage(
            stream=BytesIO(meme_image.read()),
            content_type='image/jpeg',
            filename='randomname.jpg'
        )
        meme_image.close()
        
        with self.logged_in_context(user_id):
            response = self.client.post('/upload', data= dict(
                meme=meme_file,
                tags='[{"value": "test meme"}]'
            ), content_type='multipart/form-data')
            self.assertEqual(response.status_code, 302)
            self.assertEqual(response.location, '/')

    def test_upload_meme_existent_tag(self):
        user_id = self.createTestUser()
        self.createTag("test meme")
        meme_image = open(path.join(self.test_dir, 'test_meme.jpg'), 'rb')
        meme_file = FileStorage(
            stream=BytesIO(meme_image.read()),
            content_type='image/jpeg',
            filename='randomname.jpg'
        )
        meme_image.close()
        
        with self.logged_in_context(user_id):
            response = self.client.post('/upload', data= dict(
                meme=meme_file,
                tags='[{"value": "test meme"}]'
            ), content_type='multipart/form-data')
            self.assertEqual(response.status_code, 302)
            self.assertEqual(response.location, '/')

    def test_upload_meme_missing_image(self):
        user_id = self.createTestUser()
        with self.logged_in_context(user_id):
            response = self.client.post('/upload', data= dict(
                tags='[{"value": "test meme"}]'
            ), content_type='multipart/form-data')
            self.assertEqual(response.status_code, 200)
            self.assertIn("Error in the Choose image field - This field is required.", response.text)

    def test_upload_meme_missing_tag(self):
        user_id = self.createTestUser()
        meme_image = open(path.join(self.test_dir, 'test_meme.jpg'), 'rb')
        meme_file = FileStorage(
            stream=BytesIO(meme_image.read()),
            content_type='image/jpeg',
            filename='randomname.jpg'
        )
        meme_image.close()
        
        with self.logged_in_context(user_id):
            response = self.client.post('/upload', data= dict(
                meme=meme_file,
            ), content_type='multipart/form-data')
            self.assertEqual(response.status_code, 200)
            self.assertIn("Error in the Tags field - This field is required.", response.text)

    def test_upload_meme_non_image(self):
        user_id = self.createTestUser()
        meme_file = FileStorage(
            stream=BytesIO(),
            content_type='image/jpeg',
            filename='randomname.jpg'
        )

        with self.logged_in_context(user_id):
            response = self.client.post('/upload', data= dict(
                meme=meme_file,
                tags='[{"value": "test meme"}]'
            ), content_type='multipart/form-data')
            self.assertEqual(response.status_code, 200)
            self.assertIn("The uploaded meme is not in a supported format. Please upload a proper image.", response.text)

    def test_delete_meme(self):
        user_id = self.createTestUser()
        meme_id = self.createTestMeme(user_id, 'test meme')
        with self.logged_in_context(user_id):
            response = self.client.post("/delete", data=dict(
                id=meme_id
            ), content_type='multipart/form-data')
            self.assertEqual(response.status_code, 302)
            self.assertEqual(response.location, '/')
    
    def test_delete_meme_logged_out(self):
        user_id = self.createTestUser()
        meme_id = self.createTestMeme(user_id, "test meme")
        response = self.client.post("/delete", data=dict(
            id=meme_id
        ), content_type='multipart/form-data')
        self.assertEqual(response.status_code, 302)
        self.assertStartsWith(response.location, "/login")
    
    def test_delete_meme_invalid_request(self):
        user_id = self.createTestUser()
        self.createTestMeme(user_id, 'test meme')
        with self.logged_in_context(user_id):
            response = self.client.post("/delete", data=dict(), content_type='multipart/form-data')
            self.assertEqual(response.status_code, 302)
            with self.client.session_transaction() as session:
                messages = session["_flashes"]
                self.assertGreater(len(messages), 0)
                self.assertIn("There was an error while processing your request, please try again.", [x[1] for x in messages])

    def test_delete_nonexistent_meme(self):
        user_id = self.createTestUser()
        with self.logged_in_context(user_id):
            response = self.client.post("/delete", data=dict(
                id=1
            ), content_type='multipart/form-data')
            self.assertEqual(response.status_code, 302)
            with self.client.session_transaction() as session:
                messages = session["_flashes"]
                self.assertGreater(len(messages), 0)
                self.assertIn("Unable to locate meme, it may have been deleted.", [x[1] for x in messages])

    def test_delete_other_user_meme(self):
        first_user_id = self.createTestUser()
        second_user_id = self.createTestUser()
        meme_id = self.createTestMeme(first_user_id, "test meme")
        with self.logged_in_context(second_user_id):
            response = self.client.post("/delete", data=dict(
                id=meme_id
            ), content_type='multipart/form-data')
            self.assertEqual(response.status_code, 401)
