from flask import jsonify

from blog.utils.check import check_username, check_login, check_email
from blog.utils.posts import get_posts, get_favourites, save_post, remove_post
from blog.utils.search import find_post_by_id
from blog.utils.syntax_check import check_username_syntax, check_email_syntax
from blog.utils.users import get_user
from blog_app import app
from .path import PATH


@app.route(f'{PATH}/posts/', methods=['GET'])
def api_posts_get():
    posts = get_posts()
    return jsonify(posts)


@app.route(f'{PATH}/favourites/', methods=['GET'])
def api_favourites_get():
    user = get_user()

    if not user:
        return 'NO USER', 422
    else:
        posts = get_favourites(user)
        return jsonify(posts)


@app.route(f'{PATH}/posts/<post_id>/', methods=['GET'])
def api_post_get(post_id):
    post = find_post_by_id(post_id)

    if not post:
        return 'NO POST', 400
    else:
        return jsonify(post)


@app.route(f'{PATH}/posts/<post_id>/star/', methods=['PUT'])
def api_favourite_post(post_id):
    user = get_user()
    post = find_post_by_id(post_id)

    if not post:
        return 'NO POST', 400
    if not user:
        return 'NO USER', 422
    else:
        if save_post(user, post):
            return 'OK', 201
        else:
            return 'ALREADY EXISTS', 200


@app.route(f'{PATH}/posts/<post_id>/star/', methods=['DELETE'])
def api_favourite_delete(post_id):
    user = get_user()
    post = find_post_by_id(post_id)

    if not post:
        return 'NO POST', 400
    if not user:
        return 'NO USER', 422
    else:
        remove_post(user, post)
        return 'OK', 200


@app.route(f'{PATH}/check_username/<username>/', methods=['GET'])
def api_username_exists_get(username):
    if not check_username_syntax(username):
        return 'INVALID SYNTAX'
    elif check_username(username):
        return 'ALREADY EXISTS'
    else:
        return 'OK'


@app.route(f'{PATH}/check_login/<login>/', methods=['GET'])
def api_login_exists_get(login):
    if check_login(login):
        return 'ALREADY EXISTS'
    else:
        return 'OK'


@app.route(f'{PATH}/check_email/<email>/', methods=['GET'])
def api_email_exists_get(email):
    if not check_email_syntax(email):
        return 'INVALID SYNTAX'
    elif check_email(email):
        return 'ALREADY EXISTS'
    else:
        return 'OK'
