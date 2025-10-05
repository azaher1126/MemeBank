from typing import IO, Optional
from pathvalidate import is_valid_filepath, is_valid_filename, sanitize_filename
from PIL import Image, UnidentifiedImageError
from PIL._typing import StrOrBytesPath
import os

IMAGES = tuple('jpg jpe jpeg png gif svg bmp webp'.split())

def configure_uploads(base_path: str):
    if not is_valid_filepath(base_path, platform="auto"):
        raise ValueError(f"The base uploads path provided does not have valid path syntax! Provided: {base_path}")
    
    if not os.path.exists(base_path):
        os.makedirs(base_path)

    ImageUploadSet.base_path = base_path

class ImageUploadSet():
    base_path: Optional[str] = None

    def __init__(self, destination: str):
        self._destination_folder = sanitize_filename(destination)

    @property
    def destination(self) -> str:
        if ImageUploadSet.base_path is None:
            raise RuntimeError("The application is not properly configured. Please make sure to use `configure_uploads`.")
        
        full_path = os.path.join(ImageUploadSet.base_path, self._destination_folder)
        if not os.path.exists(full_path):
            os.makedirs(full_path)
        return full_path
    
    @property
    def extensions(self) -> tuple[str, ...]:
        return IMAGES
    
    def save(self, image_data: StrOrBytesPath | IO[bytes], filename: str):
        if not is_valid_filename(filename):
            raise ValueError("The filename provided does not have valid path syntax!")
        try:
            image = Image.open(image_data)
            full_path = os.path.join(self.destination, filename)
            if image.format != "JPEG":
                rgb_image = image.convert("RGB")
                image.close()
                image = rgb_image
        
            image.save(full_path, format="JPEG")
        except UnidentifiedImageError:
            raise ValueError("The uploaded meme is not in a supported format. Please upload a proper image.")
        
    def delete(self, filename: str):
        full_path = os.path.join(self.destination, filename)
        if os.path.exists(full_path):
            os.remove(full_path)