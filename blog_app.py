from flask import Flask

app = Flask(__name__)
COOKIE_NAME = 'MSTID'

import blog.web.web
import blog.api.v0_1
import blog.web.internal
import blog.web.error
import blog.web.processors
