from flask import Flask

app = Flask(__name__)

import blog.web.imports
import blog.api.v0_1.imports

__all__ = ['app', 'blog']
