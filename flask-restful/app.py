from flask import Flask
from flask_restful import Api
from resources.page import Page

app = Flask(__name__)
api = Api(app)

api.add_resource(Page, '/page')