from flask import request, make_response, redirect
from passlib.hash import pbkdf2_sha512
import psycopg2.extras
import random
import string
from datetime import *
from search import *

DATABASE = psycopg2.connect(user='flask', password='blogappflask', database='blog',
                            cursor_factory=psycopg2.extras.NamedTupleCursor)
DATABASE.autocommit = True
COOKIE_NAME = 'MSTID'


def generate_cookie_id():
    return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(255))


def add_new_user(username, email, new_password, cookie_id):
    cursor = DATABASE.cursor()
    password_hash = pbkdf2_sha512.encrypt(new_password, rounds=200000, salt_size=64)
    cursor.execute('INSERT INTO Users (Username, Password, CookieID, Email) VALUES(%s, %s, %s, %s)',
                   (username, password_hash, cookie_id, email))


def update_user(user, **kwargs):
    cursor = DATABASE.cursor()
    if 'username' in kwargs:
        cursor.execute('UPDATE Users SET Username = %s WHERE ID = %s', (kwargs['username'], user.id))
    if 'email' in kwargs:
        cursor.execute('UPDATE Users SET Email = %s WHERE ID = %s', (kwargs['email'], user.id))
    if 'new_password' and 'cookie_id' in kwargs:
        password_hash = pbkdf2_sha512.encrypt(kwargs['new_password'], rounds=200000, salt_size=64)
        cursor.execute('UPDATE Users SET Password = %s, CookieID = %s WHERE ID = %s',
                       (password_hash, user.cookieid, user.id))


def delete_user(user):
    cursor = DATABASE.cursor()
    cursor.execute('DELETE FROM Users WHERE ID = %s', (user.id,))


def password_correct(user, password):
    return pbkdf2_sha512.verify(password, user.password)


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
    cursor.execute('SELECT * FROM Posts ORDER BY Date DESC')
    return cursor.fetchall()


def check_favourite(user, post):
    cursor = DATABASE.cursor()
    if user and post:
        cursor.execute('SELECT * FROM Posts JOIN Favourites '
                       'ON (Favourites.Post_ID = Posts.ID '
                       'AND Favourites.User_ID = %s AND Post_ID = %s)',
                       (user.id, post.id))
        return bool(cursor.fetchall())


def save_post(user, post):
    cursor = DATABASE.cursor()
    time = datetime.now()
    cursor.execute('INSERT INTO Favourites(User_ID, Post_ID, Date_Added) VALUES (%s, %s, %s)',
                   (user.id, post.id, time.strftime('%Y-%m-%d %H:%M:%S')))


def remove_post(user, post):
    cursor = DATABASE.cursor()
    time = datetime.now()
    cursor.execute('DELETE FROM Favourites WHERE User_ID = %s AND Post_ID = %s',
                   (user.id, post.id))


def get_user():
    return find_user_by_cookie(request.cookies.get(COOKIE_NAME))
