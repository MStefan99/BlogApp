from blog_app import app

from blog.utils.posts import *
from blog.utils.users import *

# Internal routes


@app.route('/add_post/', methods=['POST'])
def web_add_post():
    user = get_user()
    post_id = request.form.get('post')
    post = find_post_by_id(post_id)

    return save_post(user, post)


@app.route('/del_post/', methods=['POST'])
def web_del_post():
    user = get_user()
    post_id = request.form.get('post')
    post = find_post_by_id(post_id)

    return remove_post(user, post)


@app.route('/check_username/', methods=['POST'])
def web_username_exists():
    username = request.form.get('username').strip()

    if not username:
        return 'NO USERNAME'
    elif check_username(username):
        return 'ALREADY EXISTS'
    else:
        return 'OK'


@app.route('/check_login/', methods=['POST'])
def web_login_exists():
    login = request.form.get('login').strip()

    if not login:
        return 'NO LOGIN'
    elif check_login(login):
        return 'OK'
    else:
        return 'NOT FOUND'


@app.route('/check_email/', methods=['POST'])
def web_email_exists():
    email = request.form.get('email').strip()

    if not email:
        return 'NO EMAIL'
    if check_email(email):
        return 'ALREADY EXISTS'
    else:
        return 'OK'
