from flask import request, make_response

from blog.utils.check import check_username, check_login, check_email
from blog.utils.syntax_check import check_username_syntax, check_email_syntax
from blog_app import app
from .path import PATH


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
