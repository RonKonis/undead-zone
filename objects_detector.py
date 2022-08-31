import time
import RPi.GPIO as GPIO


class ObjectsDetector:
    RADAR_ECHO_PIN = 14
    RADAR_TRIGGER_PIN = 15
    RADIO_WAVES_SPEED = 299792458
    MIN_DISTANCE = 12

    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.RADAR_ECHO_PIN, GPIO.IN)
        GPIO.setup(self.RADAR_TRIGGER_PIN, GPIO.OUT)

    def scan(self):
        object_distance = self._measure_distance()
        return object_distance <= self.MIN_DISTANCE

    def _measure_distance(self):
        GPIO.output(self.RADAR_TRIGGER_PIN, GPIO.HIGH)
        time.sleep(0.00001)
        GPIO.output(self.RADAR_TRIGGER_PIN, GPIO.LOW)

        pulse_start = time.time()
        while GPIO.input(self.RADAR_ECHO_PIN) == GPIO.LOW:
            pulse_start = time.time()
        pulse_end = time.time()
        while GPIO.input(self.RADAR_ECHO_PIN) == GPIO.HIGH:
            pulse_end = time.time()
        pulse_duration = pulse_end - pulse_start
        return round((self.RADIO_WAVES_SPEED * pulse_duration) / 2, 2)

    def __del__(self):
        GPIO.cleanup()
