from flask import Flask, make_response

app = Flask(__name__)


@app.errorhandler(404)
def api_page_not_found(error):
    return make_response('PAGE NOT FOUND', 404)


@app.errorhandler(500)
def api_internal_error(error):
    return make_response('INTERNAL ERROR', 500)
