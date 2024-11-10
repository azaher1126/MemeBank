from dataclasses import dataclass
from flask_login import current_user

from ..database.meme_model import Meme
from .tag_model import convert_to_tagtype, TagType

@dataclass
class MemeType():
    id:int
    url:str
    tags: list[TagType]
    liked: bool
    likes: int
    user_id: int
    username: str
    date: str

    def __init__(self, meme: Meme):
        '''Takes a meme from the database and converts it into
        a MemeType object.'''
        self.id = meme.id
        self.url = f'/meme/image/{meme.id}'
        self.tags = convert_to_tagtype(meme.tags)
        self.liked = current_user in meme.users_liked
        self.likes = len(meme.users_liked)
        self.user_id = meme.user_id
        self.username = meme.uploader.username
        self.date = meme.date.isoformat()
    
def convert_to_memetype(memes: list[Meme]) -> list[MemeType]:
        '''Converts a list of memes from the database into a list of memes 
        of type MemeType.'''
        return [MemeType(meme) for meme in memes]