from .meme_model import convert_to_memetype

class UserType():

    def __init__(self, user):
        self.id = user.id
        self.email = user.email
        self.first_name = user.first_name
        self.last_name = user.last_name
        self.username = user.username
        self.memes = convert_to_memetype(user.memes)