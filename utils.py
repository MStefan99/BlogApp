from flask import request, make_response, redirect
from passlib.hash import pbkdf2_sha512
import psycopg2.extras
import random
import string
from mail import *
from datetime import *
from search import *

DATABASE = psycopg2.connect(user='flask', password='blogappflask', database='blog',
                            cursor_factory=psycopg2.extras.NamedTupleCursor)
DATABASE.autocommit = True
COOKIE_NAME = 'MSTID'


def generate_hash():
    return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.ascii_lowercase + string.digits)
                   for _ in range(255))


def add_new_user(username, email, new_password, cookie_id):
    cursor = DATABASE.cursor()
    link = generate_hash()

    password_hash = pbkdf2_sha512.encrypt(new_password, rounds=200000, salt_size=64)
    cursor.execute('INSERT INTO users (username, password, cookieid, email, verification_link) '
                   'VALUES(%s, %s, %s, %s, %s)',
                   (username, password_hash, cookie_id, email, link))
    send_mail(email, username, link, 'register')


def update_user(user, **kwargs):
    cursor = DATABASE.cursor()
    if 'username' in kwargs:
        cursor.execute('UPDATE users SET username = %s WHERE id = %s', (kwargs['username'], user.id))
        user.username = kwargs['username']

    if 'email' in kwargs:
        link = generate_hash()
        cursor.execute('UPDATE users SET email = %s, verification_link = %s, verified = FALSE '
                       'WHERE id = %s', (kwargs['email'], link, user.id))
        send_mail(kwargs['email'], user.username, link, 'email_changed')

    if 'new_password' and 'cookie_id' in kwargs:
        password_hash = pbkdf2_sha512.encrypt(kwargs['new_password'], rounds=200000, salt_size=64)
        cursor.execute('UPDATE users SET password = %s, cookieid = %s WHERE id = %s',
                       (password_hash, user.cookieid, user.id))


def delete_user(user):
    cursor = DATABASE.cursor()
    cursor.execute('DELETE FROM users WHERE id = %s', (user.id,))


def password_correct(user, password):
    return pbkdf2_sha512.verify(password, user.password)


def recover_create(user):
    cursor = DATABASE.cursor()
    link = generate_hash()
    cursor.execute('UPDATE users SET recovery_link = %s WHERE id = %s', (link, user.id))
    send_mail(user.email, user.username, link, 'password-recovery')


def check_cookie():
    cookie_id = request.cookies.get('MSTID')
    if cookie_id:
        user = find_user_by_cookie(cookie_id)
        resp = make_response(redirect(request.path, code=302))
        resp.set_cookie('MSTID', 'Bye!', expires=0)
        try:
            if not user.cookieid == cookie_id:
                return False
        except AttributeError:
            return False
    return True


def get_posts():
    cursor = DATABASE.cursor()
    cursor.execute('SELECT * FROM posts ORDER BY date DESC')
    return cursor.fetchall()


def check_favourite(user, post):
    cursor = DATABASE.cursor()
    if user and post:
        cursor.execute('SELECT * FROM posts JOIN favourites '
                       'ON (favourites.post_id = posts.id '
                       'AND favourites.user_id = %s AND post_id = %s)',
                       (user.id, post.id))
        return bool(cursor.fetchall())


def save_post(user, post):
    cursor = DATABASE.cursor()
    time = datetime.now()
    cursor.execute('INSERT INTO favourites(user_id, post_id, date_added) VALUES (%s, %s, %s)',
                   (user.id, post.id, time.strftime('%Y-%m-%d %H:%M:%S')))


def remove_post(user, post):
    cursor = DATABASE.cursor()
    time = datetime.now()
    cursor.execute('DELETE FROM favourites WHERE user_id = %s AND post_id = %s',
                   (user.id, post.id))


def get_user():
    return find_user_by_cookie(request.cookies.get(COOKIE_NAME))


def verify_email(key):
    cursor = DATABASE.cursor()
    cursor.execute('SELECT * FROM users WHERE verification_link = %s', (key,))
    user = cursor.fetchone()

    if user:
        cursor.execute('UPDATE users SET verification_link = NULL, verified = TRUE '
                       'WHERE id = %s', (user.id,))
        return True
    else:
        return False


