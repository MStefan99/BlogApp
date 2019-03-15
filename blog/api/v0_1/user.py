from flask import request, make_response, jsonify

from blog.globals import COOKIE_NAME
from blog.utils import syntax_check
from blog.utils.check import check_username, check_email
from blog.utils.hash import generate_hash
from blog.utils.search import find_user_by_login, find_user_by_recover_key
from blog.utils.users import password_correct, add_user, create_recover_link, update_user, get_user, verify_email, \
    delete_user
from blog_app import app
from .path import PATH


@app.route(f'{PATH}/login/', methods=['POST'])
def api_login_post():
    login = request.form.get('login')
    login = login.strip() if login else None
    current_password = request.form.get('current-password')
    user = find_user_by_login(login)

    if not login or not current_password:
        return make_response('MISSING ARGS', 422)
    elif not user:
        return make_response('INVALID LOGIN', 422)
    elif user and password_correct(user, current_password):
        resp = make_response('OK', 200)
        resp.set_cookie(COOKIE_NAME, user['cookieid'], max_age=60 * 60 * 24 * 30)
        return resp
    else:
        return make_response('WRONG PASSWORD', 422)


@app.route(f'{PATH}/register/', methods=['PUT'])
def api_register_put():
    username = request.form.get('username')
    email = request.form.get('email')
    new_password = request.form.get('new-password')

    username_exists = check_username(username)
    email_exists = check_email(email)
    email_syntax_ok = syntax_check.check_email_syntax(email)
    username_syntax_ok = syntax_check.check_username_syntax(username)
    password_syntax_ok = syntax_check.check_password_syntax(new_password)
    form_filled = username and new_password and email

    if not form_filled:
        return make_response('MISSING ARGS', 422)
    elif not email_syntax_ok:
        return make_response('INVALID EMAIL SYNTAX', 422)
    elif not username_syntax_ok:
        return make_response('INVALID USERNAME SYNTAX', 422)
    elif not password_syntax_ok:
        return make_response('INVALID PASSWORD SYNTAX', 422)
    elif username_exists:
        return make_response('USERNAME EXISTS', 422)
    elif email_exists:
        return make_response('EMAIL EXISTS', 422)
    else:
        cookie_id = generate_hash()
        add_user(username, email, new_password, cookie_id)
        resp = make_response(make_response('OK', 201))
        resp.set_cookie(COOKIE_NAME, cookie_id, max_age=60 * 60 * 24 * 30)
        return resp


@app.route(f'{PATH}/recover_create/', methods=['POST'])
def api_recover_create_post():
    login = request.form.get('login')
    user = find_user_by_login(login)

    if user:
        create_recover_link(user)
        return make_response('OK', 200)
    else:
        return make_response('NO USER', 422)


@app.route(f'{PATH}/recover/', methods=['PUT'])
def api_recover_put():
    key = request.form.get('key')
    user = find_user_by_recover_key(key)
    new_password = request.form.get('new-password')

    if not user:
        return make_response('NO USER', 422)
    elif not new_password:
        return make_response('MISSING ARGS', 422)
    else:
        cookie_id = generate_hash()
        update_user(user, password_reset=True, new_password=new_password, cookie_id=cookie_id)
        resp = make_response(make_response('OK', 200))
        resp.set_cookie(COOKIE_NAME, cookie_id, max_age=60 * 60 * 24 * 30)
        return resp


@app.route(f'{PATH}/settings/', methods=['POST'])
def api_settings_post():
    username = request.form.get('username')
    email = request.form.get('email')
    new_password = request.form.get('new-password')

    user = get_user()
    username_exists = check_username(username)
    email_exists = check_email(email)
    email_syntax_ok = syntax_check.check_email_syntax(email)
    username_syntax_ok = syntax_check.check_username_syntax(username)
    password_syntax_ok = syntax_check.check_password_syntax(new_password)

    if not user:
        return make_response('NO USER', 422)
    elif email and not email_syntax_ok:
        return make_response('INVALID EMAIL SYNTAX', 422)
    elif username and not username_syntax_ok:
        return make_response('INVALID USERNAME SYNTAX', 422)
    elif new_password and not password_syntax_ok:
        return make_response('INVALID PASSWORD SYNTAX', 422)
    elif username_exists:
        return make_response('USERNAME EXISTS', 422)
    elif email_exists:
        return make_response('EMAIL EXISTS', 422)

    if username:
        update_user(user, username=username)
    if email:
        update_user(user, email=email)
    if new_password:
        cookie_id = generate_hash()
        update_user(user, new_password=new_password, cookie_id=cookie_id)
        resp = make_response(make_response('OK', 200))
        resp.set_cookie(COOKIE_NAME, cookie_id, max_age=60 * 60 * 24 * 30)
        return resp

    return make_response('OK', 200)


@app.route(f'{PATH}/account/', methods=['GET'])
def api_account_get():
    user = get_user()

    keys = 'username', 'email', 'verified'

    if not user:
        return make_response('NO USER', 422)
    else:
        return jsonify({key: user[key] for key in keys})


@app.route(f'{PATH}/delete/', methods=['PUT'])
def api_delete_put():
    user = get_user()

    if not user:
        return make_response('NO USER', 422)
    else:
        delete_user(user)
        return make_response('OK', 200)


@app.route(f'{PATH}/verify/', methods=['PUT'])
def api_verify_post():
    key = request.form.get('key')
    if verify_email(key):
        return make_response('OK', 200)
    else:
        return make_response('NO USER', 422)
