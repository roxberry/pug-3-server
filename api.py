from configparser import ConfigParser
from flask import Blueprint, jsonify
import os


config_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'config.cfg')

config = ConfigParser()
config.read(config_file)
environment = config.get('main', 'env')

if environment == 'development':
    from gopigo3mock import GoPiGo3
    gpg3 = GoPiGo3()
elif environment == 'prototype':
    from gopigo3 import GoPiGo3
    gpg3 = GoPiGo3()


api = Blueprint('api', 'api', url_prefix='/api')


@api.route('/info', methods={'GET'})
def info():
    # return read_status()
    i = {"manufacturer": gpg3.get_manufacturer(), "board": gpg3.get_board(), "version": gpg3.get_version_firmware()}
    return jsonify(i)


@api.route('/fwd', methods={'GET'})
def fwd():
    """ Calls the MOVE_FORWARD function

    GET: Move forward
    :return:
    """
    return 'PUG3 moves forward'


@api.route('/set_motor_power', methods={'GET'})
def set_motor_power():
    """ Calls the SET_MOTOR_POWER

    GET: Motor
    """
    return "set_motor_power"


@api.route('/led', methods={'GET'})
def led():
    """Calls the LED function.

    GET: LED flashes.
         Returns HTTP 200 on success; body is payload as-is.
         Returns HTTP 404 when data does not exist.
    """
    return 'blink'
