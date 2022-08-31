import os
import time
import cv2
from misc import Status, Side


class VehiclesDetector:
    VEHICLES_HAAR_CASCADE_FILE_PATH = "misc/vehicles.xml"
    MAX_VELOCITY = 10 / 3.6  # 10 [km/h] in [m/s]
    AVERAGE_VEHICLE_WIDTH = 2.19456
    FOCAL_LENGTH = 60
    FRAME_WIDTH = 480
    BLUR_SIZE = (5, 5)
    SCALE_FACTOR = 1.5

    _camera = None
    _vehicles_haar_cascade = None

    def __init__(self, camera):
        self._camera = camera
        self._load_vehicles_haar_cascade()

    def detect(self):
        status = Status.NO_STATUS
        vehicle_side = None
        frame = self._camera.read()
        if frame is not None:
            start_time = time.time()
            vehicles = self._find_vehicles(frame)
            if len(vehicles) > 0:
                start_distances = self._measure_distances(vehicles)
                frame = self._camera.read()
                if frame is not None:
                    elapsed_time = time.time() - start_time
                    vehicles = self._find_vehicles(frame)
                    end_distances = self._measure_distances(vehicles)
                    is_approaching_vehicle, vehicle_index = self._is_approaching_vehicle(start_distances, end_distances, elapsed_time)
                    if is_approaching_vehicle:
                        vehicle_side = self._find_vehicle_side(vehicles[vehicle_index])
                        status = Status.VEHICLE_APPROACHING
                    else:
                        status = Status.VEHICLE_NOT_APPROACHING
            else:
                status = Status.NO_VEHICLES
        return status, vehicle_side

    def _load_vehicles_haar_cascade(self):
        if not os.path.exists(self.VEHICLES_HAAR_CASCADE_FILE_PATH):
            raise FileNotFoundError(f"Can't Find '{self.VEHICLES_HAAR_CASCADE_FILE_PATH}'...")
        self._vehicles_haar_cascade = cv2.CascadeClassifier(self.VEHICLES_HAAR_CASCADE_FILE_PATH)

    def _find_vehicles(self, frame):
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray_blurred_frame = cv2.GaussianBlur(gray_frame, self.BLUR_SIZE, cv2.BORDER_CONSTANT)
        return self._vehicles_haar_cascade.detectMultiScale(gray_blurred_frame, self.SCALE_FACTOR)

    def _measure_distances(self, vehicles):
        distances = []
        for (x, y, w, h) in vehicles:
            distances.append((self.AVERAGE_VEHICLE_WIDTH * self.FOCAL_LENGTH) / w)
        return distances

    def _is_approaching_vehicle(self, start_distances, end_distances, delta_time):
        for i, (start_distance, end_distance) in enumerate(zip(start_distances, end_distances)):
            velocity = (start_distance - end_distance) / delta_time
            if velocity >= self.MAX_VELOCITY:
                return True, i
        return False, None

    def _find_vehicle_side(self, vehicle):
        vehicle_middle = (vehicle[0] + vehicle[2]) / 2
        if vehicle_middle < self.FRAME_WIDTH / 3:
            return Side.RIGHT
        elif vehicle_middle > self.FRAME_WIDTH * (2 / 3):
            return Side.LEFT
        return Side.MIDDLE
