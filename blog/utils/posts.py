from datetime import datetime

import psycopg2

from blog.utils.users import DATABASE


def get_posts():
    cursor = DATABASE.cursor()
    cursor.execute('select * from posts '
                   'order by date desc')
    return cursor.fetchall()


def get_favourites(user):
    cursor = DATABASE.cursor()
    cursor.execute('select posts.* from posts join favourites '
                   'on (favourites.post_id = posts.id '
                   'and favourites.user_id = %s) '
                   'order by favourites.date_added desc', (user['id'],))
    return cursor.fetchall()


def check_favourite(user, post):
    cursor = DATABASE.cursor()
    if user and post:
        cursor.execute('select * from posts join favourites '
                       'on (favourites.post_id = posts.id '
                       'and favourites.user_id = %s '
                       'and post_id = %s)',
                       (user['id'], post['id']))
        return bool(cursor.fetchall())


def save_post(user, post):
    cursor = DATABASE.cursor()
    time = datetime.now()
    try:
        cursor.execute('insert into favourites(user_id, post_id, date_added) '
                       'values (%s, %s, %s)',
                       (user['id'], post['id'], time.strftime('%Y-%m-%d %H:%M:%S')))
    except psycopg2.IntegrityError:
        return 'ALREADY EXISTS'
    return 'OK'


def remove_post(user, post):
    cursor = DATABASE.cursor()
    cursor.execute('delete from favourites '
                   'where user_id = %s '
                   'and post_id = %s',
                   (user['id'], post['id']))
    return 'OK'


def search_posts_by_text(query):
    query = '%' + query + '%'
    cursor = DATABASE.cursor()
    cursor.execute('select * from posts '
                   'where content like %s '
                   'or title like %s '
                   'or tagline like %s '
                   'order by date desc',
                   (query, query, query))
    return cursor.fetchall()
