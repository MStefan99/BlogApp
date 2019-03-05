from flask import jsonify
from blog_app import app
from blog.utils.posts import *

VERSION = 'v0.1'


@app.route('/api/v0.1/posts/', methods=['GET'])
def get():
    posts = get_posts()
    return jsonify(posts)

