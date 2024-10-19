from website import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)


'''Human-Computer Interaction Comment.
Accounts could be put in place to keep track of who uploads memes,
likes, comments and settings. The user interface could be changed 
to account for a large number of memes, since currently the website 
shows all the memes on the homepage. Another HCI improvment would 
be storing what kind of memes the user is most interested in based
on likes/comments/views. The ability to upload more than one more
meme at a time could be added to make it easier for users to 
upload more memes to the website.'''

'''Airtifical Inteligence Comment.
AI could be used to make the home page personalized for each user 
using the information in their account to come up what memes the 
user likes. AI could also be used to scrap the internet and 
automatically add more memes to the website that would appeal to
the user base. Generating tags that is most commonly liked accross
the user base and creating meme recomendations and tag recomendations
could be done using AI. AI could be used to detected key objects in
images and use the information alongside common tags to automically
tag memes.
'''