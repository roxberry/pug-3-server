from __future__ import print_function  # use python 3 syntax but make it compatible with python 2
from __future__ import division

from flask import Flask, jsonify, request
import time     # import the time library for the sleep function
import gopigo3  # import the GoPiGo3 drivers
import requests


GPG = gopigo3.GoPiGo3()

app = Flask(__name__)


@app.route('/', methods={'GET'})
def api_root():
    data = {
        'hello': 'world-v7',
        'number': 7
    }
    resp = jsonify(data)
    resp.status_code = 200
    resp.headers['Link'] = 'http://actu8.io'

    return resp


@app.route('/fwd', methods={'GET'})
def fwd():
    return 'PUG3 moves forward'


@app.route('/led', methods={'GET'})
def led():
    count = 0
    while count < 10:
        count = count + 1
        for i in range(11):  # count from 0-10
            GPG.set_led(GPG.LED_EYE_LEFT, i, i, i)  # set the LED brightness (0 to 255)
            GPG.set_led(GPG.LED_EYE_RIGHT, 10 - i, 10 - i, 10 - i)  # set the LED brightness (255 to 0)
            GPG.set_led(GPG.LED_BLINKER_LEFT, (i * 25))  # set the LED brightness (0 to 255)
            GPG.set_led(GPG.LED_BLINKER_RIGHT, ((10 - i) * 25))  # set the LED brightness (255 to 0)
            time.sleep(
                0.02)  # delay for 0.02 seconds (20ms) to reduce CPU load & give time to see the LED pulsing.

        GPG.set_led(GPG.LED_WIFI, 0, 0, 10)

        for i in range(11):  # count from 0-10
            GPG.set_led(GPG.LED_EYE_LEFT, 10 - i, 10 - i, 10 - i)  # set the LED brightness (255 to 0)
            GPG.set_led(GPG.LED_EYE_RIGHT, i, i, i)  # set the LED brightness (0 to 255)
            GPG.set_led(GPG.LED_BLINKER_LEFT, ((10 - i) * 25))  # set the LED brightness (0 to 255)
            GPG.set_led(GPG.LED_BLINKER_RIGHT, (i * 25))  # set the LED brightness (255 to 0)
            time.sleep(
                0.02)  # delay for 0.02 seconds (20ms) to reduce CPU load & give time to see the LED pulsing.

        GPG.set_led(GPG.LED_WIFI, 0, 0, 0)

    GPG.reset_all()
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
