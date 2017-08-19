from __future__ import division
from __future__ import print_function  # use python 3 syntax but make it compatible with python 2

from flask import Flask, Blueprint, jsonify, request
from api import api
from dev import dev


app = Flask(__name__)
app.register_blueprint(dev)
app.register_blueprint(api)


# @app.errorhandler(404)
# def not_found(error=None):
#     message = {
#         'status': 404,
#         'message': 'Not Found: ' + request.url
#     }
#     resp = jsonify(message)
#     resp.status_code = 404
#
#     return resp
#
#
# app.error_handler_spec[None][404] = not_found


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=54321)
