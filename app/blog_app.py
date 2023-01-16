from flask import Flask

from blog.api.v0_1.common import api_v01_common
from blog.api.v0_1.error import api_v01_error
from blog.api.v0_1.user import api_v01_user
from blog.web.error import web_error
from blog.web.internal import web_internal
from blog.web.processors import web_processors
from blog.web.web import web_pages

app = Flask(__name__)
app.register_blueprint(web_pages)
app.register_blueprint(web_processors)
app.register_blueprint(web_internal)
app.register_blueprint(web_error)

app.register_blueprint(api_v01_common, url_prefix='/api/v0.1')
app.register_blueprint(api_v01_user, url_prefix='/api/v0.1')
app.register_blueprint(api_v01_error, url_prefix='/api/v0.1')

if __name__ == '__main__':
    app.run()
