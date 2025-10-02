from website.uploads.helpers.image_upload_set import ImageUploadSet, configure_uploads
from os import path
import unittest
import tempfile

class ImageUploadSetTests(unittest.TestCase):
    def setUp(self):
        ImageUploadSet.base_path = None
        self.test_dir = path.join(path.dirname(path.realpath(__file__)),'testData')
        return super().setUp()

    def test_non_configured_upload_set(self):
        image_set = ImageUploadSet("testing")
        self.assertRaises(RuntimeError, lambda: image_set.destination)

    def test_create_upload_dir(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            configure_uploads(tmpdir)
            image_set = ImageUploadSet("testing")
            image_set.destination

    def test_delete_nonexistent(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            configure_uploads(tmpdir)
            image_set = ImageUploadSet("testing")
            image_set.delete("nonexistent_file")
    
    def test_save_jpeg(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            configure_uploads(tmpdir)
            image_set = ImageUploadSet("testing")
            test_file_path = path.join(self.test_dir, "test_meme.jpg")
            with open(test_file_path, "rb") as file:
                image_set.save(file, "test_upload.jpg")
            self.assertTrue(path.exists(path.join(image_set.destination, "test_upload.jpg")))

    def test_save_png(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            configure_uploads(tmpdir)
            image_set = ImageUploadSet("testing")
            test_file_path = path.join(self.test_dir, "test_meme.png")
            with open(test_file_path, "rb") as file:
                image_set.save(file, "test_upload.jpg")
            self.assertTrue(path.exists(path.join(image_set.destination, "test_upload.jpg")))
