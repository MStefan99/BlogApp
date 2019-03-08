from flask import jsonify, request

from blog.utils.check import check_username, check_login, check_email
from blog.utils.posts import get_posts, get_favourites, check_favourite, save_post, remove_post
from blog.utils.search import find_post_by_link, find_post_by_id
from blog.utils.syntax_check import check_username_syntax, check_email_syntax
from blog.utils.users import get_user
from blog_app import app

URL = 'api'
VERSION = 'v0.1'
PATH = f'/{URL}/{VERSION}'


#  WARNING: JSONPLUS NEEDS TO BE INSTALLED FOR API TO WORK CORRECTLY!


@app.route(f'{PATH}/posts/', methods=['GET'])
def api_posts_get():
    posts = get_posts()
    return jsonify(posts)


@app.route(f'{PATH}/favourites/', methods=['GET'])
def api_favourites_get():
    user = get_user()
    posts = get_favourites(user)
    return jsonify(posts)


@app.route(f'{PATH}/post/<string:post_link>/', methods=['GET'])
def api_post_get(post_link):
    user = get_user()
    post = find_post_by_link(post_link)
    is_favourite = check_favourite(user, post) if user else False
    return jsonify(post, is_favourite)


@app.route(f'{PATH}/favourite/', methods=['GET'])
def api_favourite_get():
    user = get_user()
    post_id = request.form.get('post')
    post = find_post_by_id(post_id)
    added = check_favourite(user, post)

    if not post:
        return 'NO POST'
    if not user:
        return 'NO USER'
    if added:
        return 'IS FAVOURITE'
    else:
        return 'NOT FAVOURITE'


@app.route(f'{PATH}/favourite/', methods=['PUT'])
def api_favourite_post():
    user = get_user()
    post_id = request.form.get('post')
    post = find_post_by_id(post_id)

    if not post:
        return 'NO POST'
    if not user:
        return 'NO USER'
    else:
        return save_post(user, post)


@app.route(f'{PATH}/favourite/', methods=['DELETE'])
def api_favourite_delete():
    user = get_user()
    post_id = request.form.get('post')
    post = find_post_by_id(post_id)

    if not post:
        return 'NO POST'
    if not user:
        return 'NO USER'
    else:
        return remove_post(user, post)


@app.route(f'{PATH}/check_username/', methods=['GET'])
def api_username_exists_get():
    username = request.form.get('username').strip()
    username_syntax_ok = check_username_syntax(username)

    if not username:
        return 'NO USERNAME'
    elif not username_syntax_ok:
        return 'INVALID SYNTAX'
    elif check_username(username):
        return 'ALREADY EXISTS'
    else:
        return 'OK'


@app.route(f'{PATH}/check_login/', methods=['GET'])
def api_login_exists_get():
    login = request.form.get('login').strip()

    if not login:
        return 'NO LOGIN'
    elif check_login(login):
        return 'OK'
    else:
        return 'NOT FOUND'


@app.route(f'{PATH}/check_email/', methods=['GET'])
def api_email_exists_get():
    email = request.form.get('email').strip()
    email_syntax_ok = check_email_syntax(email)

    if not email:
        return 'NO EMAIL'
    if not email_syntax_ok:
        return 'INVALID SYNTAX'
    if check_email(email):
        return 'ALREADY EXISTS'
    else:
        return 'OK'
