import random
import string
from blog.globals import DATABASE


def generate_hash():
    while True:
        new_hash = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.ascii_lowercase + string.digits)
                           for _ in range(255))
        if not check_hash(new_hash):
            add_hash(new_hash)
            break
    return new_hash


def check_hash(hash_value):
    cursor = DATABASE.cursor()
    cursor.execute('select hash from hashes')
    hashes = cursor.fetchall()
    return hash_value in hashes


def add_hash(hash_value):
    cursor = DATABASE.cursor()
    cursor.execute('insert into hashes(hash) values (%s)', (hash_value,))


def delete_hash(*hashes):
    for hash_value in hashes:
        cursor = DATABASE.cursor()
        cursor.execute('delete from hashes where hash = %s', (hash_value,))
