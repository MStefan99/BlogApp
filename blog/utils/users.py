from flask import request, redirect
from passlib.hash import pbkdf2_sha512

from blog.globals import DATABASE, COOKIE_NAME
from blog.mail.mail import send_mail
from blog.utils.hash import generate_hash, delete_hash
from blog.utils.search import find_user_by_cookie


def add_new_user(username, email, new_password, cookie_id):
    cursor = DATABASE.cursor()
    link = generate_hash()

    password_hash = pbkdf2_sha512.encrypt(new_password, rounds=200000, salt_size=64)
    cursor.execute('insert into users (username, password, cookieid, email, verification_link) '
                   'values (?, ?, ?, ?, ?)',
                   [username, password_hash, cookie_id, email, link])
    DATABASE.commit()
    send_mail(email, username, link, 'register')


def update_user(user, password_reset=False, **kwargs):
    cursor = DATABASE.cursor()
    if 'username' in kwargs:
        cursor.execute('update users set username = ? where id = ?', [kwargs['username'], user['id']])
        DATABASE.commit()
        user['username'] = kwargs['username']

    if 'email' in kwargs:
        link = generate_hash()
        if user['verification_link']:
            delete_hash(user['verification_link'])
        cursor.execute('update users set email = ?, verification_link = ?, verified = false '
                       'where id = ?', [kwargs['email'], link, user['id']])
        DATABASE.commit()
        send_mail(kwargs['email'], user['username'], link, 'email_change')

    if 'new_password' and 'cookie_id' in kwargs:
        password_hash = pbkdf2_sha512.encrypt(kwargs['new_password'], rounds=200000, salt_size=64)
        delete_hash(user['cookieid'])
        cursor.execute('update users set password = ?, cookieid = ? where id = ?',
                       [password_hash, user['cookieid'], user['id']])
        DATABASE.commit()
        if password_reset:
            delete_hash(user['recovery_link'])
            cursor.execute('update users set recovery_link = null where id = ?', [user['id']])


def delete_user(user):
    cursor = DATABASE.cursor()
    delete_hash(user['cookieid'], user['recovery_link'], user['verification_link'])
    cursor.execute('delete from users where id = ?', [user['id']])
    DATABASE.commit()


def password_correct(user, password):
    return pbkdf2_sha512.verify(password, user['password'])


def create_recover_link(user):
    cursor = DATABASE.cursor()
    link = generate_hash()
    if user['recovery_link']:
        delete_hash(user['recovery_link'])
    cursor.execute('update users set recovery_link = ? where id = ?', [link, user['id']])
    DATABASE.commit()

    send_mail(user['verified_email'] if user['verified_email'] else user['email'], user['username'], link,
              'password-recovery')


def check_cookie():
    cookie_id = request.cookies.get('MSTID')
    if cookie_id:
        user = find_user_by_cookie(cookie_id)
        resp = redirect(request.path, code=302)
        resp.set_cookie('MSTID', 'Bye!', expires=0)
        try:
            if not user['cookieid'] == cookie_id:
                return False
        except AttributeError:
            return False
    return True


def get_user():
    return find_user_by_cookie(request.cookies.get(COOKIE_NAME))


def verify_email(key):
    cursor = DATABASE.cursor()
    cursor.execute('select * from users where verification_link = ?', [key])
    user = cursor.fetchone()

    if user:
        delete_hash(user['verification_link'])
        cursor.execute('update users set verification_link = null, verified = true, verified_email = ? '
                       'where id = ?', [user['email'], user['id']])
        DATABASE.commit()
        return True
    else:
        return False
