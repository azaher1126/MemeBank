from typing import IO, Optional
from pathlib import Path
from PIL import Image
from PIL._typing import StrOrBytesPath
import os

IMAGES = tuple('jpg jpe jpeg png gif svg bmp webp'.split())

def configure_uploads(base_path: str):
    try:
        path = Path(base_path)
        path.mkdir(exist_ok=True)
    except:
        raise ValueError("The base uploads path provided does not have valid path syntax!")

    ImageUploadSet.base_path = base_path

class ImageUploadSet():
    base_path: Optional[str] = None

    def __init__(self, destination: str):
        try:
            Path(destination)
        except:
            raise ValueError("The destination provided does not have valid path syntax!")

        self._destination_folder = destination

    @property
    def destination(self) -> str:
        if ImageUploadSet.base_path is None:
            raise RuntimeError("The application is not properly configured. Please make sure to use `configure_uploads`.")
        
        full_path = os.path.join(ImageUploadSet.base_path, self._destination_folder)
        if not os.path.exists(full_path):
            os.mkdir(full_path)
        return full_path
    
    @property
    def extensions(self) -> tuple[str]:
        return IMAGES
    
    def save(self, image_data: StrOrBytesPath | IO[bytes], filename: str):
        try:
            Path(filename)
        except:
            raise ValueError("The filename provided does not have valid path syntax!")
        try:
            image = Image.open(image_data)
            full_path = os.path.join(self.destination, filename)
            if image.format != "JPEG":
                rgb_image = image.convert("RGB")
                image.close()
                image = rgb_image
        
            image.save(full_path, format="JPEG")
        except:
            raise ValueError("The uploaded meme is not in a supported format. Please upload a proper image.")