import RPi.GPIO as GPIO
from misc import Side


class GripsVibrator:
    RIGHT_VIBRATOR_PIN = 23
    LEFT_VIBRATOR_PIN = 24

    _is_vibrating = False

    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.RIGHT_VIBRATOR_PIN, GPIO.OUT)
        GPIO.setup(self.LEFT_VIBRATOR_PIN, GPIO.OUT)

    def vibrate(self, side):
        if not self._is_vibrating:
            if side == Side.LEFT:
                GPIO.output(self.LEFT_VIBRATOR_PIN, GPIO.HIGH)
            elif side == Side.RIGHT:
                GPIO.output(self.RIGHT_VIBRATOR_PIN, GPIO.HIGH)
            elif side == Side.MIDDLE:
                GPIO.output(self.RIGHT_VIBRATOR_PIN, GPIO.HIGH)
                GPIO.output(self.LEFT_VIBRATOR_PIN, GPIO.HIGH)
            self._is_vibrating = True

    def stop_vibrate(self):
        if self._is_vibrating:
            GPIO.output(self.RIGHT_VIBRATOR_PIN, GPIO.LOW)
            GPIO.output(self.LEFT_VIBRATOR_PIN, GPIO.LOW)
            self._is_vibrating = False

    def __del__(self):
        GPIO.cleanup()
