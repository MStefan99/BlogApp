import psycopg2

DATABASE = psycopg2.connect(user='flask', password='blogappflask', database='blog',
                            cursor_factory=psycopg2.extras.NamedTupleCursor)
DATABASE.autocommit = True


def exists(list):
    if list:
        return True
    else:
        return False


def find_user_by_name(username):
    cursor = DATABASE.cursor()
    cursor.execute('select * from users where lower(username) = lower(%s)', (username,))
    user = cursor.fetchone()
    return user


def find_user_by_email(email):
    cursor = DATABASE.cursor()
    cursor.execute('select * from users where lower(email) = lower(%s) or '
                   'lower(verified_email) = lower(%s)', (email, email))
    user = cursor.fetchone()
    return user


def find_user_by_cookie(cookie_id):
    cursor = DATABASE.cursor()
    cursor.execute('select * from users where cookieid = %s', (cookie_id,))
    user = cursor.fetchone()
    return user


def find_user_by_login(login):
    login = login.lower()
    cursor = DATABASE.cursor()
    cursor.execute('select * from users where lower(username) = lower(%s) or '
                   'lower(email) = lower(%s)', (login, login))
    user = cursor.fetchone()
    return user


def find_user_by_recover_key(key):
    cursor = DATABASE.cursor()
    cursor.execute('select * from users where recovery_link = %s', (key,))
    user = cursor.fetchone()
    return user


def check_username(username):
    user = find_user_by_name(username)
    return exists(user)


def check_login(login):
    user = find_user_by_login(login)
    return exists(user)


def check_email(email):
    user = find_user_by_email(email)
    return exists(user)


def find_post_by_link(link):
    cursor = DATABASE.cursor()
    cursor.execute('select * from posts where link = %s', (link,))
    return cursor.fetchone()


def get_favourites(user):
    cursor = DATABASE.cursor()
    cursor.execute('select posts.* from posts join favourites '
                   'on (favourites.post_id = posts.id and favourites.user_id = %s) '
                   'order by favourites.date_added desc', (user.id,))
    return cursor.fetchall()


def find_post_by_id(id):
    cursor = DATABASE.cursor()
    cursor.execute('select * from posts where id = %s', (id,))
    return cursor.fetchone()
