from camera import Camera
from surroundings_screen import SurroundingsScreen
from vehicles_detector import VehiclesDetector
from objects_detector import ObjectsDetector
from grips_vibrator import GripsVibrator
from misc import Status


def main():
    camera = Camera()
    surroundings_screen = SurroundingsScreen(camera)

    try:
        vehicles_detector = VehiclesDetector(camera)
    except FileNotFoundError as e:
        surroundings_screen.display_error(str(e))
    else:
        objects_detector = ObjectsDetector()
        grips_vibrator = GripsVibrator()
        camera.start()
        surroundings_screen.start()
        while True:
            try:
                if objects_detector.scan():
                    status = Status.NO_STATUS
                    while status != Status.NO_VEHICLES:
                        status, vehicle_side = vehicles_detector.detect()
                        if status == Status.VEHICLE_APPROACHING:
                            grips_vibrator.vibrate(vehicle_side)
                        else:
                            grips_vibrator.stop_vibrate()
            except KeyboardInterrupt:
                camera.stop()
                surroundings_screen.stop()
                break
            except Exception as e:
                camera.stop()
                surroundings_screen.stop()
                surroundings_screen.display_error(str(e))
                break


if __name__ == "__main__":
    main()
