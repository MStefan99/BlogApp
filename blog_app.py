from flask import Flask, render_template
from utils import *
from search import *

app = Flask(__name__)

DATABASE = psycopg2.connect(user='flask', password='blogappflask', database='blog',
                            cursor_factory=psycopg2.extras.NamedTupleCursor)
DATABASE.autocommit = True


@app.route('/select/')
def select():
    cookie_id = request.cookies.get(COOKIE_NAME)

    if cookie_id:
        user = find_user_by_cookie(cookie_id)
        if user:
            return redirect('/account/', code=302)
        return redirect('/logout/', code=302)

    return render_template('select.html')


@app.route('/login/')
def login():
    return render_template('login.html')


@app.route('/register/')
def register():
    return render_template('register.html')


@app.route('/login_processor/', methods=['POST'])
def login_processor():
    login = request.form.get('login').strip()
    current_password = request.form.get('current-password')
    user = find_user_by_login(login)

    if not login or not current_password:
        return render_template('error.html', code='form_not_filled')

    if user and password_correct(user, current_password):
        resp = make_response(render_template('success.html', code='login_success'))
        resp.set_cookie(COOKIE_NAME, user.cookieid, max_age=60 * 60 * 24 * 30)
        return resp

    if not user:
        return render_template('error.html', code='wrong_login')

    return render_template('error.html', code='wrong_password')


@app.route('/register_processor/', methods=['POST'])
def register_processor():
    username = request.form.get('username')
    email = request.form.get('email')
    new_password = request.form.get('new-password')
    repeat_new_password = request.form.get('repeat-new-password')
    username_exists = check_username(username)
    email_exists = check_email(email)
    form_filled = username and new_password and repeat_new_password and email

    if not form_filled:
        return render_template('error.html', code='form_not_filled')
    elif username_exists:
        return render_template('error.html', code='username_exists')
    elif email_exists:
        return render_template('error.html', code='email_exists')
    elif new_password != repeat_new_password:
        return render_template('error.html', code='passwords_do_not_match')
    elif ' ' in username or ' ' in email:
        return render_template('error.html', code='spaces_not_allowed')

    else:
        cookie_id = generate_hash()
        add_new_user(username, email, new_password, cookie_id)
        resp = make_response(render_template('success.html', code='register_success'))
        resp.set_cookie(COOKIE_NAME, cookie_id, max_age=60 * 60 * 24 * 30)
        return resp


@app.route('/logout/')
def logout():
    resp = make_response(redirect('/select/', code=302))
    resp.set_cookie(COOKIE_NAME, 'Bye!', expires=0)

    return resp


@app.route('/account/')
def account():
    user = get_user()

    if user:
        return render_template('account.html', user=user)
    return render_template('error.html', code='logged_out')


@app.route('/settings/')
def settings():
    user = get_user()

    if user:
        return render_template('settings.html')
    return render_template('error.html', code='logged_out')


@app.route('/recover_create/')
def recover_create():
    return render_template('recover-create.html')


@app.route('/recover/')
def recover():
    key = request.args.get('key')
    return render_template('recover.html', key=key)


@app.route('/recover_create_processor/', methods=["POST"])
def recover_create_processor():
    login = request.form.get('login')
    user = find_user_by_login(login)
    if user:
        create_recover_link(user)
        return render_template('success.html', code='recover_create_success')
    else:
        return render_template('error.html', code='wrong_login')


@app.route('/recover_processor/', methods=["POST"])
def recover_processor():
    key = request.form.get('key')
    user = find_user_by_recover_key(key)
    new_password = request.form.get('new-password')
    repeat_new_password = request.form.get('repeat-new-password')

    new_password_check = new_password == repeat_new_password
    if user:
        if not new_password:
            return render_template('error.html', code='form_not_filled')
        elif not new_password_check:
            return render_template('error.html', code='passwords_do_not_match')
        else:
            cookie_id = generate_hash()
            update_user(user, password_reset=True, new_password=new_password, cookie_id=cookie_id)
            resp = make_response(render_template('success.html', code='edit_success'))
            resp.set_cookie(COOKIE_NAME, cookie_id, max_age=60 * 60 * 24 * 30)
            return resp
    else:
        return render_template('error.html', code='user_not_found')


@app.route('/settings_processor/', methods=['POST'])
def settings_processor():
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

    if not user:
        return redirect('/logout/', code=302)

    if not new_password_check:
        return render_template('error.html', code='passwords_do_not_match')
    elif not email_check:
        return render_template('error.html', code='emails_do_not_match')
    elif username_exists:
        return render_template('error.html', code='username_exists')
    elif email_exists:
        return render_template('error.html', code='email_exists')
    elif (username and ' ' in username) or (email and ' ' in email):
        return render_template('error.html', code='spaces_not_allowed')

    if username:
        update_user(user, username=username)

    if email:
        update_user(user, email=email)

    if new_password:
        cookie_id = generate_hash()
        update_user(user, new_password=new_password, cookie_id=cookie_id)
        resp = make_response(render_template('success.html', code='edit_success'))
        resp.set_cookie(COOKIE_NAME, cookie_id, max_age=60 * 60 * 24 * 30)
        return resp

    return render_template('success.html', code='edit_success')


@app.route('/delete/')
def delete():
    return render_template('delete.html')


@app.route('/delete_confirm/')
def delete_confirm():
    user = get_user()

    if not user:
        return render_template('error.html', code='logged_out')
    delete_user(user)

    return redirect('/logout/', code=302)


@app.route('/')
@app.route('/posts/')
def posts():
    posts = get_posts()
    current_page = request.args.get('page')

    if not current_page:
        current_page = 0
    else:
        current_page = int(current_page)
    pages_number = len(posts) // 10 + 1

    if len(posts) > 10:
        posts = posts[current_page * 10:current_page * 10 + 10]

    return render_template('posts.html', posts=posts, current_page=current_page, pages_number=pages_number)


@app.route('/post/<string:post_link>')
def post(post_link):
    user = get_user()
    post = find_post_by_link(post_link)
    is_favourite = check_favourite(user, post)

    return render_template('post.html', post=post, is_favourite=is_favourite,
                           tags=post.tags.split(","))


@app.route('/favourites/')
def favourites():
    user = get_user()
    if not user:
        return render_template('error.html', code='logged_out')

    posts = get_favourites(user)
    if not posts:
        return render_template('favourites.html', code='no_posts')
    current_page = request.args.get('page')

    if not current_page:
        current_page = 0
    else:
        current_page = int(current_page)
    pages_number = len(posts) // 10 + 1

    if len(posts) > 10:
        posts = posts[current_page * 10:current_page * 10 + 10]
    print(pages_number)

    return render_template('favourites.html', posts=posts, current_page=current_page, pages_number=pages_number)


@app.route('/verify/')
def verify():
    key = request.args.get('key')
    if verify_email(key):
        return render_template('success.html', code='verification_success')
    else:
        return render_template('error.html', code='verification_failed')


# Error routes

@app.route('/check_email/', methods=["GET"])
@app.route('/check_username/', methods=["GET"])
@app.route('/add_post/', methods=["GET"])
@app.route('/del-post/', methods=["GET"])
@app.route('/register_processor/', methods=["GET"])
@app.route('/login_processor/', methods=["GET"])
@app.route('/settings_processor/', methods=["GET"])
def wrong_route():
    return render_template('error.html', code='wrong_route')


# Internal routes

@app.route('/add_post/', methods=["POST"])
def add_post():
    user = get_user()
    post_id = request.form.get('post')
    post = find_post_by_id(post_id)

    save_post(user, post)
    return "OK"


@app.route('/del_post/', methods=["POST"])
def del_post():
    user = get_user()
    post_id = request.form.get('post')
    post = find_post_by_id(post_id)

    remove_post(user, post)
    return "OK"


@app.route('/check_username/', methods=["POST"])
def u_exists():
    username = request.form.get('username').strip()

    if not username:
        return ''

    if check_username(username):
        return 'error;Username already taken'
    return 'ok;Username is free'


@app.route('/check_login/', methods=["POST"])
def l_exists():
    login = request.form.get('login').strip()

    if not login:
        return ''

    if check_login(login):
        return 'ok;'
    return 'error;User not found'


@app.route('/check_email/', methods=["POST"])
def e_exists():
    email = request.form.get('email').strip()

    if check_email(email):
        return 'error;Email already exists'
    return 'ok;'


if __name__ == '__main__':
    app.run()
