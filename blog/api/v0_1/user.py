from flask import request, make_response

from blog.utils import syntax_check
from blog.utils.check import check_username, check_email
from blog.utils.hash import generate_hash
from blog.utils.search import find_user_by_login, find_user_by_recover_key
from blog.utils.users import password_correct, add_new_user, create_recover_link, update_user, get_user, verify_email, \
    delete_user
from blog_app import app, COOKIE_NAME
from .path import PATH


@app.route(f'{PATH}/login/', methods=['POST'])
def api_login_post():
    login = request.form.get('login')
    login = login.strip() if login else None
    current_password = request.form.get('current-password')
    user = find_user_by_login(login)

    if not login or not current_password:
        return make_response('MISSING ARGS', 400)
    elif not user:
        return make_response('INVALID LOGIN', 400)
    elif user and password_correct(user, current_password):
        resp = make_response('OK', 200)
        resp.set_cookie(COOKIE_NAME, user.cookieid, max_age=60 * 60 * 24 * 30)
        return resp
    else:
        return make_response('WRONG PASSWORD', 400)
    

@app.route(f'{PATH}/register/', methods=['PUT'])
def api_register_put():
    username = request.form.get('username')
    email = request.form.get('email')
    new_password = request.form.get('new-password')
    repeat_new_password = request.form.get('repeat-new-password')

    username_exists = check_username(username)
    email_exists = check_email(email)
    email_syntax_ok = syntax_check.check_email_syntax(email)
    username_syntax_ok = syntax_check.check_username_syntax(username)
    password_syntax_ok = syntax_check.check_password_syntax(new_password)
    form_filled = username and new_password and repeat_new_password and email

    if not form_filled:
        return make_response('MISSING ARGS', 400)
    elif not email_syntax_ok:
        return make_response('INVALID EMAIL SYNTAX', 400)
    elif not username_syntax_ok:
        return make_response('INVALID USERNAME SYNTAX', 400)
    elif not password_syntax_ok:
        return make_response('INVALID PASSWORD SYNTAX', 400)
    elif username_exists:
        return make_response('USERNAME EXISTS', 400)
    elif email_exists:
        return make_response('EMAIL EXISTS', 400)
    elif new_password != repeat_new_password:
        return make_response('PASSWORDS DO NOT MATCH', 400)
    else:
        cookie_id = generate_hash()
        add_new_user(username, email, new_password, cookie_id)
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
        return make_response('NO USER', 400)


@app.route(f'{PATH}/recover/', methods=['PUT'])
def api_recover_put():
    key = request.form.get('key')
    user = find_user_by_recover_key(key)
    new_password = request.form.get('new-password')
    repeat_new_password = request.form.get('repeat-new-password')

    new_password_check = new_password == repeat_new_password

    if not user:
        return make_response('NO USER', 400)
    elif not new_password or not repeat_new_password:
        return make_response('MISSING ARGS', 400)
    elif not new_password_check:
        return make_response('PASSWORDS DO NOT MATCH', 400)
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
    repeat_email = request.form.get('repeat-email')
    new_password = request.form.get('new-password')
    repeat_new_password = request.form.get('repeat-new-password')

    user = get_user()
    new_password_check = new_password == repeat_new_password
    email_check = email == repeat_email
    username_exists = check_username(username)
    email_exists = check_email(email)
    email_syntax_ok = syntax_check.check_email_syntax(email)
    username_syntax_ok = syntax_check.check_username_syntax(username)
    password_syntax_ok = syntax_check.check_password_syntax(new_password)

    if not user:
        return make_response('NO USER', 400)
    elif email and not email_syntax_ok:
        return make_response('INVALID EMAIL SYNTAX', 400)
    elif username and not username_syntax_ok:
        return make_response('INVALID USERNAME SYNTAX', 400)
    elif new_password and not password_syntax_ok:
        return make_response('INVALID PASSWORD SYNTAX', 400)
    if not new_password_check:
        return make_response('PASSWORDS DO NOT MATCH', 400)
    elif not email_check:
        return make_response('EMAILS DO NOT MATCH', 400)
    elif username_exists:
        return make_response('USERNAME EXISTS', 400)
    elif email_exists:
        return make_response('EMAIL EXISTS', 400)

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


@app.route(f'{PATH}/delete/', methods=['PUT'])
def api_delete_put():
    user = get_user()

    if not user:
        return make_response('NO USER', 400)
    else:
        delete_user(user)
        return make_response('OK', 200)


@app.route(f'{PATH}/verify/', methods=['PUT'])
def api_verify_post():
    key = request.form.get('key')
    if verify_email(key):
        return make_response('OK', 200)
    else:
        return make_response('NO USER', 400)
