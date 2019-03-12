from flask import Flask, make_response

app = Flask(__name__)


@app.errorhandler(500)
def api_internal_error(error):
    return make_response('INTERNAL ERROR', 500)
