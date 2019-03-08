from flask import render_template
from blog.utils import syntax_check
from blog.utils.posts import *
from blog.utils.users import *
from blog.utils.search import *
from blog_app import app

DATABASE = psycopg2.connect(user='flask', password='blogappflask', database='blog',
                            cursor_factory=psycopg2.extras.NamedTupleCursor)
DATABASE.autocommit = True


@app.route('/sign in/')
def web_web_sign_in():
    cookie_id = request.cookies.get(COOKIE_NAME)

    if cookie_id:
        user = find_user_by_cookie(cookie_id)
        if user:
            return redirect('/account/', code=302)
        else:
            return redirect('/logout/', code=302)
    else:
        return render_template('user/select.html')


@app.route('/login/')
def web_login():
    return render_template('user/login.html')


@app.route('/register/')
def web_register():
    return render_template('user/register.html')


@app.route('/logout/')
def web_logout():
    resp = make_response(redirect('/', code=302))
    resp.set_cookie(COOKIE_NAME, 'Bye!', expires=0)

    return resp


@app.route('/account/')
def web_account():
    user = get_user()

    if user:
        return render_template('user/account.html', user=user)
    else:
        return render_template('status/error.html', code='logged_out')


@app.route('/settings/')
def web_settings():
    user = get_user()

    if user:
        return render_template('user/settings.html')
    else:
        return render_template('status/error.html', code='logged_out')


@app.route('/recover_create/')
def web_recover_create():
    return render_template('user/recover-create.html')


@app.route('/recover/')
def web_recover():
    key = request.args.get('key')
    return render_template('user/recover.html', key=key)


@app.route('/delete/')
def web_delete():
    return render_template('user/delete.html')


@app.route('/delete_confirm/')
def web_delete_confirm():
    user = get_user()

    if not user:
        return render_template('status/error.html', code='logged_out')
    else:
        delete_user(user)
        return redirect('/logout/', code=302)


@app.route('/')
@app.route('/posts/')
def web_posts():
    posts = get_posts()
    current_page = request.args.get('page')

    if not current_page:
        current_page = 0
    else:
        current_page = int(current_page)
    pages_number = len(posts) // 10 + 1

    if len(posts) > 10:
        posts = posts[current_page * 10:current_page * 10 + 10]

    return render_template('posts/posts.html', posts=posts, current_page=current_page, pages_number=pages_number)


@app.route('/post/<string:post_link>/')
def web_post(post_link):
    user = get_user()
    post = find_post_by_link(post_link)
    is_favourite = check_favourite(user, post)

    return render_template('posts/post.html', post=post, is_favourite=is_favourite,
                           tags=post.tags.split(','))


@app.route('/favourites/')
def web_favourites():
    user = get_user()
    if not user:
        return render_template('status/error.html', code='logged_out')

    posts = get_favourites(user)
    if not posts:
        return render_template('posts/favourites.html', code='no_posts')
    current_page = request.args.get('page')

    if not current_page:
        current_page = 0
    else:
        current_page = int(current_page)
    pages_number = len(posts) // 10 + 1

    if len(posts) > 10:
        posts = posts[current_page * 10:current_page * 10 + 10]
    print(pages_number)

    return render_template('posts/favourites.html', posts=posts, current_page=current_page, pages_number=pages_number)


@app.route('/verify/')
def web_verify():
    key = request.args.get('key')
    if verify_email(key):
        return render_template('status/success.html', code='verification_success')
    else:
        return render_template('status/error.html', code='verification_failed')


@app.route('/secret/')
def web_secret():
    return render_template('status/secret.html')


if __name__ == '__main__':
    app.run()
