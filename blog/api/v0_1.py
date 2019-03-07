from flask import jsonify
from blog_app import app
from blog.utils.posts import *

URL = 'api'
VERSION = 'v0.1'
PATH = f'/{URL}/{VERSION}'

#  WARNING: JSONPLUS NEEDS TO BE INSTALLED FOR API TO WORK CORRECTLY


@app.route(f'{PATH}/posts/', methods=['GET'])
def api_posts_get():
    posts = get_posts()
    return jsonify(posts)


@app.route(f'{PATH}/post/<string:post_link>')
def api_post_get(post_link):
    # TODO: add the rest of api methods
    pass


