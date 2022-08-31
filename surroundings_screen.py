import cv2
import numpy
from time import sleep
from threading import Thread, Event


class SurroundingsScreen:
    DEFAULT_WIDTH = 640
    DEFAULT_HEIGHT = 480

    TITLE = "Undead Zone"
    DEFAULT_LOCATION = (3, 30)
    FONT = cv2.FONT_HERSHEY_SIMPLEX
    FONT_SCALE = 0.8
    COLOR = (0, 255, 0)
    THICKNESS = 2

    ERROR_NO_CAMERA = "Can't Find Camera...\n" \
                      "Please Make Sure It's Connected."

    _camera = None
    _stop_event = Event()

    def __init__(self, camera):
        self._camera = camera
        self._stop_event.clear()

    def display_error(self, error_message):
        error_message += "\nPlease Try to Restart the Device.\n" \
                         "If This Keeps Happening,\n" \
                         "Please Contact the Manufacturer."
        self._display_error_message(error_message)
        cv2.waitKey(0)

    def start(self):
        sleep(3)
        Thread(target=self._display, daemon=True).start()

    def stop(self):
        self._stop_event.set()
        sleep(0.1)

    def _display(self):
        while not self._stop_event.is_set():
            frame = self._camera.read()
            if frame is not None:
                self._put_text(frame, f"FPS: {self._camera.fps}", self.DEFAULT_LOCATION)
                cv2.imshow(self.TITLE, frame)
            else:
                self._display_error_message(self.ERROR_NO_CAMERA)
            cv2.waitKey(1)

    def _display_error_message(self, error_message):
        width, height = self.DEFAULT_WIDTH, self.DEFAULT_HEIGHT
        if self._camera.is_connected():
            width, height = self._camera.resolution
        blank_image = numpy.zeros(shape=[height, width, 3], dtype=numpy.uint8)
        for i, line in enumerate(error_message.split('\n')):
            location = (self.DEFAULT_LOCATION[0], self.DEFAULT_LOCATION[1] * (i + 1))
            self._put_text(blank_image, line, location)
        cv2.imshow(self.TITLE, blank_image)

    def _put_text(self, frame, text, location):
        cv2.putText(frame, text, location, self.FONT, self.FONT_SCALE, self.COLOR, self.THICKNESS)

    def __del__(self):
        cv2.destroyAllWindows()
