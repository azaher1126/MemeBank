# MemeBank

MemeBank is website built on top of Flask to deliver an exceptional meme sharing experience for users!
It allows users to share and browse memes. Users can then like and comment on memes to share their thoughts on feelings.

## How To Run

To run the package you must install the dependencies using:

```shell
pip install -r requirements.txt
```

### Running the Development Web Server

1. Install the project dependencies using the command above.
2. Create a .env file in the root of the repository following the .env.example present in the respository.
3. Run the `main.py` in the root of the repository.
4. Navigate to `http://127.0.0.1:5000` in any web browser.

### Running Unit Tests

1. Install the project dependencies using the command above.
2. Run the `run_tests.py` in the root of the repository.
3. It will use coverage to analysis the code coverage of the unit tests and provide a html report in the `htmlcov` directory.

### Reset All User Content

Delete `website/database/database.db` and delete all images from `website/uploads/memes`
