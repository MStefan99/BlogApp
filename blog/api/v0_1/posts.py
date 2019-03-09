from flask import jsonify, request, make_response
from blog.utils.posts import get_posts, get_favourites, check_favourite, save_post, remove_post
from blog.utils.search import  find_post_by_id
from blog.utils.users import get_user
from blog_app import app
from .path import PATH


@app.route(f'{PATH}/posts/', methods=['GET'])
def api_posts_get():
    posts = get_posts()
    return jsonify(posts)


@app.route(f'{PATH}/favourites/', methods=['GET'])
def api_favourites_get():
    user = get_user()

    if not user:
        return make_response('NO USER', 422)
    else:
        posts = get_favourites(user)
        return jsonify(posts)


@app.route(f'{PATH}/post/', methods=['GET'])
def api_post_get():
    id = request.args.get('id')
    post = find_post_by_id(id)

    if not post:
        return make_response('NO POST', 422)
    else:
        return jsonify(post)


@app.route(f'{PATH}/favourite/', methods=['GET'])
def api_favourite_get():
    user = get_user()
    post_id = request.form.get('post')
    post = find_post_by_id(post_id)
    added = check_favourite(user, post)

    if not post:
        return make_response('NO POST', 422)
    if not user:
        return make_response('NO USER', 422)
    if added:
        return make_response('IS FAVOURITE', 200)
    else:
        return make_response('NOT FAVOURITE', 200)


@app.route(f'{PATH}/favourite/', methods=['PUT'])
def api_favourite_post():
    user = get_user()
    post_id = request.form.get('post')
    post = find_post_by_id(post_id)

    if not post:
        return make_response('NO POST', 422)
    if not user:
        return make_response('NO USER', 422)
    else:
        return save_post(user, post)


@app.route(f'{PATH}/favourite/', methods=['DELETE'])
def api_favourite_delete():
    user = get_user()
    post_id = request.form.get('post')
    post = find_post_by_id(post_id)

    if not post:
        return make_response('NO POST', 422)
    if not user:
        return make_response('NO USER', 422)
    else:
        return remove_post(user, post)
