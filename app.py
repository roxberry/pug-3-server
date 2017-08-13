from flask import Flask, jsonify, request
import requests

app = Flask(__name__)


@app.route('/', methods={'GET'})
def api_root():
    data = {
        'hello': 'world-v5',
        'number': 6
    }
    resp = jsonify(data)
    resp.status_code = 200
    resp.headers['Link'] = 'http://actu8.io'

    return resp


@app.route('/fwd', methods={'GET'})
def fwd():
    return 'PUG3 moves forward'


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
