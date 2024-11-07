from flask_login import current_user
import json

from ..database.meme_model import Meme
from .tag_model import convert_to_tagtype

class MemeType():
    def __init__(self, meme: Meme):
        '''Takes a meme from the database and converts it into
        a MemeType object.'''
        self.id = meme.id
        self.url = meme.url
        self.tags = convert_to_tagtype(meme.tags)
        self.liked = current_user in meme.users_liked
        self.likes = len(meme.users_liked)
        self.user_id = meme.user_id
        self.username = meme.uploader.username
        self.date = meme.date.isoformat()

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)
    
def convert_to_memetype(memes: list[Meme]) -> list[MemeType]:
        '''Converts a list of memes from the database into a list of memes 
        of type MemeType.'''
        if len(memes) == 0:
            return []
        if len(memes) == 1:
            return [MemeType(memes[0])]
        meme = memes[0]
        del memes[0]
        return [MemeType(meme)] + convert_to_memetype(memes)