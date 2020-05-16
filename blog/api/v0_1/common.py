from flask import jsonify, request, make_response

from blog.utils.check import check_username, check_login, check_email
from blog.utils.posts import get_posts, get_favourites, check_favourite, save_post, remove_post
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
        return make_response('NO USER', 422)
    else:
        posts = get_favourites(user)
        return jsonify(posts)


@app.route(f'{PATH}/post/', methods=['GET'])
def api_post_get():
    id = request.args.get('id')
    post = find_post_by_id(id)

    if not post:
        return make_response('NO POST', 422)
    else:
        return jsonify(post)


@app.route(f'{PATH}/favourite/', methods=['GET'])
def api_favourite_get():
    user = get_user()
    post_id = request.form.get('post')
    post = find_post_by_id(post_id)
    added = check_favourite(user, post)

    if not post:
        return make_response('NO POST', 422)
    if not user:
        return make_response('NO USER', 422)
    if added:
        return make_response('IS FAVOURITE', 200)
    else:
        return make_response('NOT FAVOURITE', 200)


@app.route(f'{PATH}/favourite/', methods=['PUT'])
def api_favourite_post():
    user = get_user()
    post_id = request.form.get('post')
    post = find_post_by_id(post_id)

    if not post:
        return make_response('NO POST', 422)
    if not user:
        return make_response('NO USER', 422)
    else:
        return save_post(user, post)


@app.route(f'{PATH}/favourite/', methods=['DELETE'])
def api_favourite_delete():
    user = get_user()
    post_id = request.form.get('post')
    post = find_post_by_id(post_id)

    if not post:
        return make_response('NO POST', 422)
    if not user:
        return make_response('NO USER', 422)
    else:
        return remove_post(user, post)


@app.route(f'{PATH}/check_username/', methods=['GET'])
def api_username_exists_get():
    username = request.form.get('username').strip()
    username = username.strip() if username else None
    username_syntax_ok = check_username_syntax(username)

    if not username:
        return make_response('NO USERNAME', 422)
    elif not username_syntax_ok:
        return make_response('INVALID SYNTAX', 200)
    elif check_username(username):
        return make_response('ALREADY EXISTS', 200)
    else:
        return make_response('OK', 200)


@app.route(f'{PATH}/check_login/', methods=['GET'])
def api_login_exists_get():
    login = request.form.get('login')
    login = login.strip() if login else None

    if not login:
        return make_response('NO LOGIN', 422)
    elif check_login(login):
        return make_response('OK', 200)
    else:
        return make_response('NOT FOUND', 200)


@app.route(f'{PATH}/check_email/', methods=['GET'])
def api_email_exists_get():
    email = request.form.get('email')
    email = email.strip() if email else None
    email_syntax_ok = check_email_syntax(email)

    if not email:
        return make_response('NO EMAIL', 422)
    elif not email_syntax_ok:
        return make_response('INVALID SYNTAX', 200)
    elif check_email(email):
        return make_response('ALREADY EXISTS', 200)
    else:
        return make_response('OK', 200)
