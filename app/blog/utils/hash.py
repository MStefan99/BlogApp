import uuid


def generate_hash():
    new_hash = uuid.uuid4()
    return str(new_hash)


def check_hash(hash_value):
    print('check_hash method is deprecated and will be removed in future versions')


def add_hash(hash_value):
    print('add_hash method is deprecated and will be removed in future versions')


def delete_hash(*hashes):
    print('delete_hash method is deprecated and will be removed in future versions')
    # Not used
