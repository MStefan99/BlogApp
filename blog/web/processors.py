from flask import render_template, request, make_response, redirect

from blog.globals import COOKIE_NAME
from blog.utils import syntax_check
from blog.utils.check import check_username, check_email
from blog.utils.hash import generate_hash
from blog.utils.search import find_user_by_login, find_user_by_recover_key
from blog.utils.users import password_correct, add_new_user, create_recover_link, update_user, get_user, verify_email, \
    delete_user
from blog_app import app


@app.route('/smart sign in/', methods=['POST'])
def web_select_processor():
    login = request.form.get('login')
    user = find_user_by_login(login)

    if user:
        username = user['username']
        current_password = request.form.get('current-password')
        return render_template('user/login.html', login=username, password=current_password)
    else:
        return render_template('user/register.html', login=login)


@app.route('/login_processor/', methods=['POST'])
def web_login_processor():
    login = request.form.get('login')
    login = login.strip() if login else None
    current_password = request.form.get('current-password')
    user = find_user_by_login(login)

    if not login or not current_password:
        return render_template('status/error.html', code='form_not_filled')
    elif not user:
        return render_template('status/error.html', code='wrong_login')
    elif user and password_correct(user, current_password):
        resp = make_response(render_template('status/success.html', code='login_success'))
        resp.set_cookie(COOKIE_NAME, user['cookieid'], max_age=60 * 60 * 24 * 30)
        return resp
    else:
        return render_template('status/error.html', code='wrong_password')


@app.route('/register_processor/', methods=['POST'])
def web_register_processor():
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
        return render_template('status/error.html', code='form_not_filled')
    elif not email_syntax_ok:
        return render_template('status/error.html', code='wrong_email_syntax')
    elif not username_syntax_ok:
        return render_template('status/error.html', code='wrong_username_syntax')
    elif not password_syntax_ok:
        return render_template('status/error.html', code='wrong_password_syntax')
    elif username_exists:
        return render_template('status/error.html', code='username_exists')
    elif email_exists:
        return render_template('status/error.html', code='email_exists')
    elif new_password != repeat_new_password:
        return render_template('status/error.html', code='passwords_do_not_match')
    else:
        cookie_id = generate_hash()
        add_new_user(username, email, new_password, cookie_id)
        resp = make_response(render_template('status/success.html', code='register_success'))
        resp.set_cookie(COOKIE_NAME, cookie_id, max_age=60 * 60 * 24 * 30)
        return resp


@app.route('/recover_create_processor/', methods=['POST'])
def web_recover_create_processor():
    login = request.form.get('login')
    user = find_user_by_login(login)

    if user:
        create_recover_link(user)
        return render_template('status/success.html', code='recover_create_success')
    else:
        return render_template('status/error.html', code='wrong_login')


@app.route('/recover_processor/', methods=['POST'])
def web_recover_processor():
    key = request.form.get('key')
    user = find_user_by_recover_key(key)
    new_password = request.form.get('new-password')
    repeat_new_password = request.form.get('repeat-new-password')

    new_password_check = new_password == repeat_new_password

    if not user:
        return render_template('status/error.html', code='user_not_found')
    elif not new_password or not repeat_new_password:
        return render_template('status/error.html', code='form_not_filled')
    elif not new_password_check:
        return render_template('status/error.html', code='passwords_do_not_match')
    else:
        cookie_id = generate_hash()
        update_user(user, password_reset=True, new_password=new_password, cookie_id=cookie_id)
        resp = make_response(render_template('status/success.html', code='edit_success'))
        resp.set_cookie(COOKIE_NAME, cookie_id, max_age=60 * 60 * 24 * 30)
        return resp


@app.route('/settings_processor/', methods=['POST'])
def web_settings_processor():
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
        return redirect('/logout/', code=302)
    elif email and not email_syntax_ok:
        return render_template('status/error.html', code='wrong_email_syntax')
    elif username and not username_syntax_ok:
        return render_template('status/error.html', code='wrong_username_syntax')
    elif new_password and not password_syntax_ok:
        return render_template('status/error.html', code='wrong_password_syntax')
    if not new_password_check:
        return render_template('status/error.html', code='passwords_do_not_match')
    elif not email_check:
        return render_template('status/error.html', code='emails_do_not_match')
    elif username_exists:
        return render_template('status/error.html', code='username_exists')
    elif email_exists:
        return render_template('status/error.html', code='email_exists')

    if username:
        update_user(user, username=username)
    if email:
        update_user(user, email=email)
    if new_password:
        cookie_id = generate_hash()
        update_user(user, new_password=new_password, cookie_id=cookie_id)
        resp = make_response(render_template('status/success.html', code='edit_success'))
        resp.set_cookie(COOKIE_NAME, cookie_id, max_age=60 * 60 * 24 * 30)
        return resp

    return render_template('status/success.html', code='edit_success')


@app.route('/delete_confirm/')
def web_delete_confirm():
    user = get_user()

    if not user:
        return render_template('status/error.html', code='logged_out')
    else:
        delete_user(user)
        return redirect('/logout/', code=302)


@app.route('/verify/')
def web_verify():
    key = request.args.get('key')
    if verify_email(key):
        return render_template('status/success.html', code='verification_success')
    else:
        return render_template('status/error.html', code='verification_failed')
