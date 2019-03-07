from blog_app import app

from flask import render_template

# Error routes


@app.route('/check_email/', methods=['GET'])
@app.route('/check_username/', methods=['GET'])
@app.route('/add_post/', methods=['GET'])
@app.route('/del-post/', methods=['GET'])
@app.route('/register_processor/', methods=['GET'])
@app.route('/login_processor/', methods=['GET'])
@app.route('/smart sign in/', methods=['GET'])
@app.route('/settings_processor/', methods=['GET'])
def web_wrong_route():
    return render_template('status/error.html', code='wrong_route')


@app.errorhandler(404)
def web_page_not_found(error):
    title = 'Page not found!'
    message = 'Oops! It\'s not you, it\'s us! Seems like we\'ve lost this page somewhere in space...'
    return render_template('status/app_error.html', code=404, title=title, message=message, error=error), 404


@app.errorhandler(500)
def web_internal_error(error):
    title = 'Server error!'
    message = 'Oops! It\'s not you, it\'s us! Seems like our programmers messed up this page...'
    return render_template('status/app_error.html', code=500, title=title, message=message, error=error), 500
