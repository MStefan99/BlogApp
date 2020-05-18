from flask import Blueprint, request, make_response, jsonify

from blog.globals import COOKIE_NAME
from blog.utils import syntax_check
from blog.utils.check import check_username, check_email
from blog.utils.hash import generate_hash
from blog.utils.search import find_user_by_login, find_user_by_recover_key
from blog.utils.users import password_correct, add_new_user, create_recover_link, update_user, get_user, verify_email, \
    delete_user

api_v01_user = Blueprint('api v0.1 user', __name__)


@api_v01_user.route(f'/users/<login>/', methods=['GET'])
def api_login_post(login):
    current_password = request.form.get('current-password')
    user = find_user_by_login(login)

    if not current_password:
        return 'NO PASSWORD', 400
    elif not user:
        return 'NO USER', 422
    elif user and password_correct(user, current_password):
        resp = make_response('OK', 200)
        resp.set_cookie(COOKIE_NAME, user['cookieid'], max_age=60 * 60 * 24 * 30)
        return resp
    else:
        return 'WRONG PASSWORD', 422


@api_v01_user.route(f'/users/', methods=['POST'])
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
        return 'MISSING ARGS', 400
    elif not email_syntax_ok:
        return 'INVALID EMAIL SYNTAX', 400
    elif not username_syntax_ok:
        return 'INVALID USERNAME SYNTAX', 400
    elif not password_syntax_ok:
        return 'INVALID PASSWORD SYNTAX', 400
    elif username_exists:
        return 'USERNAME EXISTS', 422
    elif email_exists:
        return 'EMAIL EXISTS', 422
    else:
        cookie_id = generate_hash()
        add_new_user(username, email, new_password, cookie_id)
        resp = make_response('OK', 201)
        resp.set_cookie(COOKIE_NAME, cookie_id, max_age=60 * 60 * 24 * 30)
        return resp


@api_v01_user.route(f'/users/<login>/recover/', methods=['POST'])
def api_recover_create_post(login):
    user = find_user_by_login(login)

    if user:
        create_recover_link(user)
        return 'OK', 200
    else:
        return 'NO USER', 422


@api_v01_user.route(f'/users/<key>/recover/', methods=['PATCH'])
def api_recover_put(key):
    user = find_user_by_recover_key(key)
    new_password = request.form.get('new-password')

    if not user:
        return 'NO USER', 422
    elif not new_password:
        return 'NO PASSWORD', 400
    elif not syntax_check.check_password_syntax(new_password):
        return 'INVALID PASSWORD SYNTAX', 400
    else:
        cookie_id = generate_hash()
        update_user(user, password_reset=True, new_password=new_password, cookie_id=cookie_id)
        resp = make_response('OK', 200)
        resp.set_cookie(COOKIE_NAME, cookie_id, max_age=60 * 60 * 24 * 30)
        return resp


@api_v01_user.route(f'/users/', methods=['PUT'])
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
        return 'NO USER', 422
    elif email and not email_syntax_ok:
        return 'INVALID EMAIL SYNTAX', 400
    elif username and not username_syntax_ok:
        return 'INVALID USERNAME SYNTAX', 400
    elif new_password and not password_syntax_ok:
        return 'INVALID PASSWORD SYNTAX', 400
    elif username_exists:
        return 'USERNAME EXISTS', 422
    elif email_exists:
        return 'EMAIL EXISTS', 422

    if username:
        update_user(user, username=username)
    if email:
        update_user(user, email=email)
    if new_password:
        cookie_id = generate_hash()
        update_user(user, new_password=new_password, cookie_id=cookie_id)
        resp = make_response('OK', 200)
        resp.set_cookie(COOKIE_NAME, cookie_id, max_age=60 * 60 * 24 * 30)
        return resp

    return 'OK', 200


@api_v01_user.route(f'/users/', methods=['GET'])
def api_account_get():
    user = get_user()
    keys = 'username', 'email', 'verified'

    if not user:
        return 'NO USER', 422
    else:
        return jsonify({key: user[key] for key in keys})


@api_v01_user.route(f'/users/', methods=['DELETE'])
def api_delete_put():
    user = get_user()

    if not user:
        return 'NO USER', 422
    else:
        delete_user(user)
        return 'OK', 200


@api_v01_user.route(f'/users/<key>/verify/', methods=['PATCH'])
def api_verify_post(key):
    if verify_email(key):
        return 'OK', 200
    else:
        return 'NO USER', 422
