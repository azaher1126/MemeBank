from flask import Flask
from .views import views

def intialize_controllers(app: Flask):    
    app.register_blueprint(views)