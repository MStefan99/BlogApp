from flask import Flask, render_template, request, make_response, redirect
from passlib.hash import pbkdf2_sha512
import datetime
import random
import string
import mysql.connector

app = Flask(__name__)

DATABASE = mysql.connector.connect(user='flask', password='MySQLPassword',
                                   database='Blog', auth_plugin='mysql_native_password')
CURSOR = DATABASE.cursor()
CURSOR.execute('''create table if not exists posts
(
    ID int auto_increment
        primary key,
    Title varchar(256) not null,
    Tagline varchar(512) not null,
    Image varchar(512) null,
    Splash varchar(512) null,
    Theme_Color char(7) null,
    Link varchar(512) not null,
    Author varchar(256) not null,
    Content text not null,
    Date datetime not null,
    Tags text null
);

create table if not exists users
(
    Username varchar(255) not null,
    Password varchar(255) not null,
    CookieID char(255) not null,
    Email varchar(255) not null,
    ID int auto_increment
        primary key,
    constraint users_CookieID_uindex
        unique (CookieID),
    constraint users_Email_uindex
        unique (Email),
    constraint users_Username_uindex
        unique (Username)
);

create table if not exists favourites
(
    User_ID int not null,
    Post_ID int not null,
    Date_Added datetime not null,
    constraint Favourites_Post_ID_uindex
        unique (Post_ID),
    constraint Favourites_posts_ID_fk
        foreign key (Post_ID) references posts (ID),
    constraint Favourites_users_ID_fk
        foreign key (User_ID) references users (ID)
);

alter table favourites
    add primary key (Post_ID);
    ''', multi=True)


@app.route('/')
def hello_world():
    if request.cookies.get('MSTID'):
        CURSOR.execute('SELECT * from Users')
        users = CURSOR.fetchall()

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
    username = request.form.get('login')
    current_password = request.form.get('current-password')
    CURSOR.execute('SELECT * from Users')
    users = CURSOR.fetchall()
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
    new_password = request.form.get('new-password')
    repeat_new_password = request.form.get('repeat-new-password')
    email = request.form.get('email')
    CURSOR.execute('SELECT * from Users')
    users = CURSOR.fetchall()

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

    else:
        cookie_id = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(255))
        password_hash = pbkdf2_sha512.encrypt(new_password, rounds=200000, salt_size=64)
        CURSOR.execute('INSERT INTO Users (Username, Password, CookieID, Email) VALUES(%s, %s, %s, %s)',
                       (username, password_hash, cookie_id, email))
        DATABASE.commit()
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
    CURSOR.execute('SELECT * from Users')
    users = CURSOR.fetchall()
    for user in users:
        if request.cookies.get('MSTID') == user[2]:
            return render_template('account.html', username=user[0])
    return render_template('error.html', code='logged_out')


@app.route('/settings/')
def settings():
    CURSOR.execute('SELECT * from Users')
    users = CURSOR.fetchall()
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
    CURSOR.execute('SELECT * from Users')
    users = CURSOR.fetchall()

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

    if username:
        CURSOR.execute('UPDATE Users SET Username = %s WHERE ID = %s', (username, user_id))
        DATABASE.commit()

    if email:
        CURSOR.execute('UPDATE Users SET Email = %s WHERE ID = %s', (email, user_id))
        DATABASE.commit()

    if new_password:
        password_hash = pbkdf2_sha512.encrypt(new_password, rounds=200000, salt_size=64)
        cookie_id = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(255))
        CURSOR.execute('UPDATE Users SET Password = %s, CookieID = %s WHERE ID = %s',
                       (password_hash, cookie_id, user_id))
        DATABASE.commit()
        resp = make_response(render_template('success.html', code='edit_success'))
        resp.set_cookie('MSTID', cookie_id, max_age=60*60*24*30)
        return resp

    return render_template('success.html', code='edit_success')


@app.route('/delete/')
def delete():
    return render_template('delete.html')


@app.route('/delete_confirm/')
def delete_confirm():
    CURSOR.execute('SELECT * from Users')
    users = CURSOR.fetchall()
    username = None

    for user in users:
        if request.cookies.get('MSTID') == user[2]:
            username = user[0]

    # Redirecting user to login page if he logged out
    if not username:
        return render_template('error.html', code='logged_out')

    CURSOR.execute('DELETE FROM Users WHERE Username = %s', (username,))
    DATABASE.commit()
    return redirect('/', code=302)


@app.route('/posts/')
def posts():
    CURSOR.execute('SELECT * FROM Posts ORDER BY Date DESC')
    blog_posts = CURSOR.fetchall()
    return render_template('posts.html', posts=blog_posts)


@app.route('/post/')
def post():
    post_link = request.args.get('post')
    CURSOR.execute('SELECT * FROM Posts')
    blog_posts = CURSOR.fetchall()
    CURSOR.execute('SELECT * from Users')
    users = CURSOR.fetchall()
    user_id = None

    for user in users:
        if request.cookies.get('MSTID') == user[2]:
            user_id = user[4]

    for blog_post in blog_posts:
        if blog_post[6] == post_link:
            CURSOR.execute('SELECT * FROM Posts JOIN Favourites '
                           'WHERE Favourites.Post_ID = Posts.ID '
                           'AND Favourites.User_ID = %s AND Post_ID = %s',
                           (user_id, blog_post[0]))
            is_favourite = bool(CURSOR.fetchall())
            return render_template('post.html', theme_color=blog_post[5], post=blog_post, is_favourite=is_favourite)


@app.route('/favourites/')
def favourites():
    CURSOR.execute('SELECT * from Users')
    users = CURSOR.fetchall()
    user_id = None

    for user in users:
        if request.cookies.get('MSTID') == user[2]:
            user_id = user[4]
    CURSOR.execute('SELECT * FROM Posts JOIN Favourites '
                   'WHERE Favourites.Post_ID = Posts.ID and Favourites.User_ID = %s '
                   'ORDER BY Favourites.Date_Added DESC', (user_id,))
    blog_posts = CURSOR.fetchall()
    if not user_id:
        return render_template('error.html', code='logged_out')
    if not blog_posts:
        return render_template('favourites.html', code='no_posts')

    return render_template('favourites.html', posts=blog_posts)


@app.route('/add_post/')
def add_post():
    post_id = request.args.get('post')
    CURSOR.execute('SELECT * from Users')
    users = CURSOR.fetchall()
    for user in users:
        if request.cookies.get('MSTID') == user[2]:
            user_id = user[4]
            time = datetime.datetime.now()
            CURSOR.execute('INSERT INTO Favourites(User_ID, Post_ID, Date_Added) VALUES (%s, %s, %s)',
                           (user_id, post_id, time.strftime('%Y-%m-%d %H:%M:%S')))
            DATABASE.commit()
    return "OK"


@app.route('/del_post/')
def del_post():
    post_id = request.args.get('post')
    CURSOR.execute('SELECT * from Users')
    users = CURSOR.fetchall()
    for user in users:
        if request.cookies.get('MSTID') == user[2]:
            user_id = user[4]
            CURSOR.execute('DELETE FROM Favourites WHERE User_ID = %s AND Post_ID = %s',
                           (user_id, post_id))
            DATABASE.commit()
    return 'OK'


if __name__ == '__main__':
    app.run()
