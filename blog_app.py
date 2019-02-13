from flask import Flask, render_template, request, make_response, redirect
from passlib.hash import pbkdf2_sha512
import datetime
import random
import string
import psycopg2

app = Flask(__name__)

DATABASE = psycopg2.connect(user='flask', password='blogappflask', database='blog')
DATABASE.autocommit = True


@app.route('/select/')
def hello_world():
    if request.cookies.get('MSTID'):
        cursor = DATABASE.cursor()
        cursor.execute('SELECT * from Users')
        users = cursor.fetchall()

        # Redirecting logged in users
        for user in users:
            if request.cookies.get('MSTID') == user[2]:
                return redirect('/account/', code=302)
    return render_template('select.html')


@app.route('/login/')
def login():
    return render_template('login.html')


@app.route('/register/')
def register():
    return render_template('register.html')


@app.route('/login_processor/', methods=['POST'])
def login_processor():
    username = request.form.get('login').strip()
    current_password = request.form.get('current-password')
    cursor = DATABASE.cursor()
    cursor.execute('SELECT * from Users')
    users = cursor.fetchall()
    user_found = False

    if not username or not current_password:
        return render_template('error.html', code='form_not_filled')

    for user in users:
        user_found = username.lower() == user[0].lower() or username == user[3]
        if user_found and pbkdf2_sha512.verify(current_password, user[1]):
            resp = make_response(render_template('success.html', code='login_success'))
            resp.set_cookie('MSTID', user[2], max_age=60*60*24*30)
            return resp
        if user_found:
            break

    if not user_found:
        return render_template('error.html', code='wrong_login')

    return render_template('error.html', code='wrong_password')


@app.route('/register_processor/', methods=['POST'])
def register_processor():
    username = request.form.get('username')
    email = request.form.get('email')
    new_password = request.form.get('new-password')
    repeat_new_password = request.form.get('repeat-new-password')
    cursor = DATABASE.cursor()
    cursor.execute('SELECT * from Users')
    users = cursor.fetchall()

    username_exists = username in [user[0] for user in users]
    email_exists = email in [user[3] for user in users]
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
        cookie_id = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(255))
        password_hash = pbkdf2_sha512.encrypt(new_password, rounds=200000, salt_size=64)
        cursor.execute('INSERT INTO Users (Username, Password, CookieID, Email) VALUES(%s, %s, %s, %s)',
                       (username, password_hash, cookie_id, email))
        resp = make_response(render_template('success.html', code='register_success'))
        resp.set_cookie('MSTID', cookie_id, max_age=60*60*24*30)
        return resp


@app.route('/logout/')
def logout():
    resp = make_response(redirect('/', code=302))
    resp.set_cookie('MSTID', 'Bye!', expires=0)
    return resp


@app.route('/account/')
def account():
    cursor = DATABASE.cursor()
    cursor.execute('SELECT * from Users')
    users = cursor.fetchall()
    for user in users:
        if request.cookies.get('MSTID') == user[2]:
            return render_template('account.html', username=user[0])
    return render_template('error.html', code='logged_out')


@app.route('/settings/')
def settings():
    cursor = DATABASE.cursor()
    cursor.execute('SELECT * from Users')
    users = cursor.fetchall()
    for user in users:
        if request.cookies.get('MSTID') == user[2]:
            return render_template('settings.html')
    return render_template('error.html', code='logged_out')


@app.route('/settings_processor/', methods=['POST'])
def settings_processor():
    username = request.form.get('username')
    email = request.form.get('email')
    repeat_email = request.form.get('repeat-email')
    new_password = request.form.get('new-password')
    repeat_new_password = request.form.get('repeat-new-password')
    cursor = DATABASE.cursor()
    cursor.execute('SELECT * from Users')
    users = cursor.fetchall()

    new_password_check = new_password == repeat_new_password
    email_check = email == repeat_email
    username_exists = username in [user[0] for user in users]
    email_exists = email in [user[3] for user in users]
    user_id = None

    for user in users:
        if request.cookies.get('MSTID') == user[2]:
            user_id = user[4]

    # Redirecting user to login page if he logged out
    if not user_id:
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
        cursor.execute('UPDATE Users SET Username = %s WHERE ID = %s', (username, user_id))

    if email:
        cursor.execute('UPDATE Users SET Email = %s WHERE ID = %s', (email, user_id))

    if new_password:
        password_hash = pbkdf2_sha512.encrypt(new_password, rounds=200000, salt_size=64)
        cookie_id = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(255))
        cursor.execute('UPDATE Users SET Password = %s, CookieID = %s WHERE ID = %s',
                       (password_hash, cookie_id, user_id)) 
        resp = make_response(render_template('success.html', code='edit_success'))
        resp.set_cookie('MSTID', cookie_id, max_age=60*60*24*30)
        return resp

    return render_template('success.html', code='edit_success')


@app.route('/delete/')
def delete():
    return render_template('delete.html')


@app.route('/delete_confirm/')
def delete_confirm():
    cursor = DATABASE.cursor()
    cursor.execute('SELECT * from Users')
    users = cursor.fetchall()
    user_id = None

    for user in users:
        if request.cookies.get('MSTID') == user[2]:
            user_id = user[4]

    # Redirecting user to login page if he logged out
    if not user_id:
        return render_template('error.html', code='logged_out')

    cursor.execute('DELETE FROM Users WHERE ID = %s', (user_id,))
    return redirect('/', code=302)


@app.route('/')
@app.route('/posts/')
def posts():
    cursor = DATABASE.cursor()
    cursor.execute('SELECT * FROM Posts ORDER BY Date DESC')
    blog_posts = cursor.fetchall()
    return render_template('posts.html', posts=blog_posts)


@app.route('/post/<string:post_link>')
def post(post_link):
    cursor = DATABASE.cursor()
    cursor.execute('SELECT * FROM Posts')
    blog_posts = cursor.fetchall()
    cursor.execute('SELECT * from Users')
    users = cursor.fetchall()
    user_id = None

    for user in users:
        if request.cookies.get('MSTID') == user[2]:
            user_id = user[4]

    for blog_post in blog_posts:
        if blog_post[6] == post_link:
            cursor.execute('SELECT * FROM Posts JOIN Favourites '
                           'ON (Favourites.Post_ID = Posts.ID '
                           'AND Favourites.User_ID = %s AND Post_ID = %s)',
                           (user_id, blog_post[0]))
            is_favourite = bool(cursor.fetchall())
            cursor.close()
            return render_template('post.html', theme_color=blog_post[5], post=blog_post, is_favourite=is_favourite,
                                   tags=blog_post[10].split(","))


@app.route('/favourites/')
def favourites():
    cursor = DATABASE.cursor()
    cursor.execute('SELECT * from Users')
    users = cursor.fetchall()
    user_id = None

    for user in users:
        if request.cookies.get('MSTID') == user[2]:
            user_id = user[4]
    cursor.execute('SELECT * FROM Posts JOIN Favourites '
                   'ON (Favourites.Post_ID = Posts.ID and Favourites.User_ID = %s) '
                   'ORDER BY Favourites.Date_Added DESC', (user_id,))
    blog_posts = cursor.fetchall()
    cursor.close()
    if not user_id:
        return render_template('error.html', code='logged_out')
    if not blog_posts:
        return render_template('favourites.html', code='no_posts')

    return render_template('favourites.html', posts=blog_posts)


@app.route('/add_post/')
def add_post():
    post_id = request.args.get('post')
    cursor = DATABASE.cursor()
    cursor.execute('SELECT * from Users')
    users = cursor.fetchall()
    for user in users:
        if request.cookies.get('MSTID') == user[2]:
            user_id = user[4]
            time = datetime.datetime.now()
            cursor.execute('INSERT INTO Favourites(User_ID, Post_ID, Date_Added) VALUES (%s, %s, %s)',
                           (user_id, post_id, time.strftime('%Y-%m-%d %H:%M:%S')))
    return "OK"


@app.route('/del_post/')
def del_post():
    post_id = request.args.get('post')
    cursor = DATABASE.cursor()
    cursor.execute('SELECT * from Users')
    users = cursor.fetchall()
    for user in users:
        if request.cookies.get('MSTID') == user[2]:
            user_id = user[4]
            cursor.execute('DELETE FROM Favourites WHERE User_ID = %s AND Post_ID = %s',
                           (user_id, post_id)) 
    cursor.close()
    return 'OK'


@app.route('/check_username/')
def check_username():
    username = request.args.get('username').strip()
    if not username:
        return ''
    cursor = DATABASE.cursor()
    cursor.execute('SELECT * from Users')
    users = cursor.fetchall()
    cursor.close()

    if username.lower() in [user[0].lower() for user in users]:
        return 'error;Username already taken'
    return 'ok;Username is free'


@app.route('/check_email/')
def check_email():
    email = request.args.get('email').strip()
    cursor = DATABASE.cursor()
    cursor.execute('SELECT * from Users')
    users = cursor.fetchall()
    cursor.close()

    if email.lower() in [user[3].lower() for user in users]:
        return 'error;Email already exists'
    return 'ok;'


if __name__ == '__main__':
    app.run()
