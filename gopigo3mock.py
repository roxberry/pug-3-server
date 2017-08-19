import math  # import math for math.pi constant
import time

FIRMWARE_VERSION_REQUIRED = "0.3.x"


class Enumeration(object):
    def __init__(self, names):  # or *names, with no .split()
        number = 0
        for line, name in enumerate(names.split('\n')):
            if name.find(",") >= 0:
                # strip out the spaces
                while name.find(" ") != -1:
                    name = name[:name.find(" ")] + name[(name.find(" ") + 1):]

                # strip out the commas
                while name.find(",") != -1:
                    name = name[:name.find(",")] + name[(name.find(",") + 1):]

                # if the value was specified
                if name.find("=") != -1:
                    number = int(float(name[(name.find("=") + 1):]))
                    name = name[:name.find("=")]

                # optionally print to confirm that it's working correctly
                # print "%40s has a value of %d" % (name, number)

                setattr(self, name, number)
                number = number + 1


class FirmwareVersionError(Exception):
    """Exception raised if the GoPiGo3 firmware needs to be updated"""


class SensorError(Exception):
    """Exception raised if a sensor is not yet configured when trying to read it"""


class I2CError(Exception):
    """Exception raised if there was an error on an I2C bus"""


class ValueError(Exception):
    """Exception raised if trying to read an invalid value"""


class GoPiGo3(object):
    WHEEL_BASE_WIDTH = 117  # distance (mm) from left wheel to right wheel. This works with the initial GPG3 prototype. Will need to be adjusted.
    WHEEL_DIAMETER = 66.5  # wheel diameter (mm)
    WHEEL_BASE_CIRCUMFERENCE = WHEEL_BASE_WIDTH * math.pi  # The circumference of the circle the wheels will trace while turning (mm)
    WHEEL_CIRCUMFERENCE = WHEEL_DIAMETER * math.pi  # The circumference of the wheels (mm)

    MOTOR_GEAR_RATIO = 120  # Motor gear ratio # 220 for Nicole's prototype
    ENCODER_TICKS_PER_ROTATION = 6  # Encoder ticks per motor rotation (number of magnet positions) # 16 for early prototypes
    MOTOR_TICKS_PER_DEGREE = (
        (MOTOR_GEAR_RATIO * ENCODER_TICKS_PER_ROTATION) / 360.0)  # encoder ticks per output shaft rotation degree

    GROVE_I2C_LENGTH_LIMIT = 16

    SPI_MESSAGE_TYPE = Enumeration("""
        NONE,

        GET_MANUFACTURER,
        GET_NAME,
        GET_HARDWARE_VERSION,
        GET_FIRMWARE_VERSION,
        GET_ID,

        SET_LED,

        GET_VOLTAGE_5V,
        GET_VOLTAGE_VCC,

        SET_SERVO,

        SET_MOTOR_PWM,

        SET_MOTOR_POSITION,
        SET_MOTOR_POSITION_KP,
        SET_MOTOR_POSITION_KD,

        SET_MOTOR_DPS,

        SET_MOTOR_LIMITS,

        OFFSET_MOTOR_ENCODER,

        GET_MOTOR_ENCODER_LEFT,
        GET_MOTOR_ENCODER_RIGHT,

        GET_MOTOR_STATUS_LEFT,
        GET_MOTOR_STATUS_RIGHT,

        SET_GROVE_TYPE,
        SET_GROVE_MODE,
        SET_GROVE_STATE,
        SET_GROVE_PWM_DUTY,
        SET_GROVE_PWM_FREQUENCY,

        GET_GROVE_VALUE_1,
        GET_GROVE_VALUE_2,
        GET_GROVE_STATE_1_1,
        GET_GROVE_STATE_1_2,
        GET_GROVE_STATE_2_1,
        GET_GROVE_STATE_2_2,
        GET_GROVE_VOLTAGE_1_1,
        GET_GROVE_VOLTAGE_1_2,
        GET_GROVE_VOLTAGE_2_1,
        GET_GROVE_VOLTAGE_2_2,
        GET_GROVE_ANALOG_1_1,
        GET_GROVE_ANALOG_1_2,
        GET_GROVE_ANALOG_2_1,
        GET_GROVE_ANALOG_2_2,

        START_GROVE_I2C_1,
        START_GROVE_I2C_2,
    """)

    GROVE_TYPE = Enumeration("""
        CUSTOM = 1,
        IR_DI_REMOTE,
        IR_EV3_REMOTE,
        US,
        I2C,
    """)

    GROVE_STATE = Enumeration("""
        VALID_DATA,
        NOT_CONFIGURED,
        CONFIGURING,
        NO_DATA,
        I2C_ERROR,
    """)

    LED_EYE_LEFT = 0x02
    LED_EYE_RIGHT = 0x01
    LED_BLINKER_LEFT = 0x04
    LED_BLINKER_RIGHT = 0x08
    LED_LEFT_EYE = LED_EYE_LEFT
    LED_RIGHT_EYE = LED_EYE_RIGHT
    LED_LEFT_BLINKER = LED_BLINKER_LEFT
    LED_RIGHT_BLINKER = LED_BLINKER_RIGHT
    LED_WIFI = 0x80  # Used to indicate WiFi status. Should not be controlled by the user.

    SERVO_1 = 0x01
    SERVO_2 = 0x02

    MOTOR_LEFT = 0x01
    MOTOR_RIGHT = 0x02

    MOTOR_FLOAT = -128

    GROVE_1_1 = 0x01
    GROVE_1_2 = 0x02
    GROVE_2_1 = 0x04
    GROVE_2_2 = 0x08

    GROVE_1 = GROVE_1_1 + GROVE_1_2
    GROVE_2 = GROVE_2_1 + GROVE_2_2

    GroveType = [0, 0]
    GroveI2CInBytes = [0, 0]

    GROVE_INPUT_DIGITAL = 0
    GROVE_OUTPUT_DIGITAL = 1
    GROVE_INPUT_DIGITAL_PULLUP = 2
    GROVE_INPUT_DIGITAL_PULLDOWN = 3
    GROVE_INPUT_ANALOG = 4
    GROVE_OUTPUT_PWM = 5
    GROVE_INPUT_ANALOG_PULLUP = 6
    GROVE_INPUT_ANALOG_PULLDOWN = 7

    GROVE_LOW = 0
    GROVE_HIGH = 1

    def __init__(self, addr=8, detect=True):
        self.SPI_Address = addr
        if detect:
            try:
                manufacturer = self.get_manufacturer()
                board = self.get_board()
                vfw = self.get_version_firmware()
            except IOError:
                raise IOError("No SPI response. GoPiGo3 with address %d not connected." % addr)
            if manufacturer != "Mock" or board != "GoPiGo3":
                raise IOError("GoPiGo3 with address %d not connected." % addr)
            if vfw.split('.')[0] != FIRMWARE_VERSION_REQUIRED.split('.')[0] or vfw.split('.')[1] != \
                    FIRMWARE_VERSION_REQUIRED.split('.')[1]:
                raise FirmwareVersionError("GoPiGo3 firmware needs to be version %s but is currently version %s" \
                                           % (FIRMWARE_VERSION_REQUIRED, vfw))


    def get_manufacturer(self):
        return "Mock"


    def get_board(self):
        return "GoPiGo3"


    def get_version_firmware(self):
        return "0.3.9"



