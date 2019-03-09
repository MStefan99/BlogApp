from flask import Flask

app = Flask(__name__)

from blog.web import web, internal, error, processors
from blog.api.v0_1 import common, user
