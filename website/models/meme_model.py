import json

from ..database.meme_model import Meme

class MemeType():
    def __init__(self, meme):
        '''Takes a meme from the database and converts it into
        a MemeType object.'''
        self.id = meme.id
        self.url = meme.url
        tags = []
        for tag in meme.tags.split():
            tags.append(tag)
        self.tags = tags
        self.liked = []
        if meme.liked != '':
            self.liked = json.loads(meme.liked)
        self.likes = len(self.liked)
        self.user_id = meme.user_id
        self.username = meme.username
        self.date = meme.date.isoformat()

    @staticmethod
    def convert_to_memetype(memes: list[Meme]) -> list:
        '''Converts a list of memes from the database into a list of memes 
        of type MemeType.'''
        if len(memes) == 0:
            return []
        if len(memes) == 1:
            return [MemeType(memes[0])]
        meme = memes[0]
        del memes[0]
        return [MemeType(meme)] + MemeType.convert_to_memetype(memes)

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)