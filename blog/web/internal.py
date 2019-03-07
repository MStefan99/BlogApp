from blog_app import app

from blog.utils.posts import *
from blog.utils.users import *

# Internal routes


@app.route('/add_post/', methods=['POST'])
def web_add_post():
    user = get_user()
    post_id = request.form.get('post')
    post = find_post_by_id(post_id)

    save_post(user, post)
    return 'OK'


@app.route('/del_post/', methods=['POST'])
def web_del_post():
    user = get_user()
    post_id = request.form.get('post')
    post = find_post_by_id(post_id)

    remove_post(user, post)
    return 'OK'


@app.route('/check_username/', methods=['POST'])
def web_username_exists():
    username = request.form.get('username').strip()

    if not username:
        return ''
    elif check_username(username):
        return 'error;Username already taken'
    else:
        return 'ok;Username is free'


@app.route('/check_login/', methods=['POST'])
def web_login_exists():
    login = request.form.get('login').strip()

    if not login:
        return ''
    elif check_login(login):
        return 'ok;'
    else:
        return 'error;User not found'


@app.route('/check_email/', methods=['POST'])
def web_email_exists():
    email = request.form.get('email').strip()

    if check_email(email):
        return 'error;Email already exists'
    else:
        return 'ok;'
