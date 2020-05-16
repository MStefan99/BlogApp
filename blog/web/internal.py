from flask import request

from blog.utils.check import check_username, check_login, check_email
from blog.utils.posts import save_post, remove_post
from blog.utils.search import find_post_by_id
from blog.utils.syntax_check import check_email_syntax, check_username_syntax
from blog.utils.users import get_user
from blog_app import app


# Internal routes


@app.route('/add_post/', methods=['POST'])
def web_add_post():
    user = get_user()
    post_id = request.form.get('post')
    post = find_post_by_id(post_id)

    if save_post(user, post):
        return 'OK', 201
    else:
        return 'ALREADY EXISTS', 422


@app.route('/del_post/', methods=['POST'])
def web_del_post():
    user = get_user()
    post_id = request.form.get('post')
    post = find_post_by_id(post_id)

    if remove_post(user, post):
        return 'OK', 200
    else:
        return 'ALREADY EXISTS', 422


@app.route('/check_username/', methods=['POST'])
def web_username_exists():
    username = request.form.get('username')
    username = username.strip() if username else None
    username_syntax_ok = check_username_syntax(username)

    if not username:
        return 'NO USERNAME'
    elif not username_syntax_ok:
        return 'INVALID SYNTAX'
    elif check_username(username):
        return 'ALREADY EXISTS'
    else:
        return 'OK'


@app.route('/check_login/', methods=['POST'])
def web_login_exists():
    login = request.form.get('login')
    login = login.strip() if login else None

    if not login:
        return 'NO LOGIN'
    elif check_login(login):
        return 'OK'
    else:
        return 'NOT FOUND'


@app.route('/check_email/', methods=['POST'])
def web_email_exists():
    email = request.form.get('email')
    email = email.strip() if email else None
    email_syntax_ok = check_email_syntax(email)

    if not email:
        return 'NO EMAIL'
    elif not email_syntax_ok:
        return 'INVALID SYNTAX'
    elif check_email(email):
        return 'ALREADY EXISTS'
    else:
        return 'OK'
