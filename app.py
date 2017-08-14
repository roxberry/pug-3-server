from __future__ import division
from __future__ import print_function  # use python 3 syntax but make it compatible with python 2

import requests
from flask import Flask, Blueprint, jsonify, request

import gopigo3  # import the GoPiGo3 drivers

GPG = gopigo3.GoPiGo3()

dev = Blueprint('dev', __name__, template_folder='templates')


@dev.route('/')
def index():
    """GET to generate a list of endpoints and their docstrings"""
    urls = dict([(r.rule, Flask.current_app.view_functions.get(r.endpoint).func_doc)
                 for r in Flask.current_app.url_map.iter_rules()
                 if not r.rule.startswith('/static')])
    return Flask.render_template('index.html', urls=urls)


app = Flask(__name__)


@app.route('/fwd', methods={'GET'})
def fwd():
    GPG.fwd()
    return 'PUG3 moves forward'


@app.route('/set_motor_power', methods={'GET'})
def set_motor_power():
    return "set_motor_power"


@app.route('/led', methods={'GET'})
def led():
    """Calls the LED function.

    GET: LED flashes.
         Returns HTTP 200 on success; body is payload as-is.
         Returns HTTP 404 when data does not exist.
    """
    return "LED blinking"


@app.route('/tools', methods={'GET'})
def tools():
    url = 'http://localhost:3001/api/schedulerapi/processrun/resources'
    resp = requests.get(url, auth=('user', 'pass'))
    return jsonify(resp.json())


@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Not Found: ' + request.url
    }
    resp = jsonify(message)
    resp.status_code = 404

    return resp


app.error_handler_spec[None][404] = not_found


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=54321)
