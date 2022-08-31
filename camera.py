import cv2
from time import sleep
from threading import Thread, Event


class Camera:
    _camera = None
    _frame = None
    _fps = 0
    _width = 0
    _height = 0
    _stop_event = Event()

    def __init__(self):
        self._stop_event.clear()
        self._connect()

    @property
    def fps(self):
        return self._fps

    @property
    def resolution(self):
        return self._width, self._height

    def is_connected(self):
        return self._camera and self._camera.isOpened() and self._fps > 0

    def start(self):
        Thread(target=self._capture, daemon=True).start()

    def stop(self):
        self._stop_event.set()
        sleep(0.1)

    def read(self):
        return self._frame if self.is_connected() else None

    def _connect(self):
        self._frame = None
        self._fps = 0
        self._width = 0
        self._height = 0
        if self._camera:
            self._disconnect()
        self._camera = cv2.VideoCapture(0)
        if self._camera and self._camera.isOpened():
            self._fps = self._camera.get(cv2.CAP_PROP_FPS)
            self._width = int(self._camera.get(cv2.CAP_PROP_FRAME_WIDTH))
            self._height = int(self._camera.get(cv2.CAP_PROP_FRAME_HEIGHT))

    def _disconnect(self):
        if self._camera:
            self._camera.release()
            self._camera = None

    def _capture(self):
        while not self._stop_event.is_set():
            if self.is_connected():
                ret, self._frame = self._camera.read()
                if not ret:
                    self._connect()
            else:
                self._connect()

    def __del__(self):
        self._disconnect()
