from flask import Flask
app = Flask(__name__)

import blog.web.web
import blog.api.v0_1
