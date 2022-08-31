# Undead Zone
## A universal safety device for pedestrian conveyances.
<div align="center">
<img src="images/model.png" alt="Model">

[![Python 3.8](https://img.shields.io/badge/Python-3.8-yellow.svg)](https://www.python.org/) [![License: MIT](https://img.shields.io/badge/License-MIT-brightgreen.svg)](https://opensource.org/licenses/MIT)
</div>

## Features
- Image Processing - detects vehicles.
- Real-Time Video - displays the dead zone.
- Object Detection - detects nearby objects (helps accuracy).
- Grips Vibration - alerts from dangerous vehicles.

## Algorithm
First, the camera starts capturing images, which are displayed asynchronously on the screen.<br>
After that, a radar signal is sent to check for nearby objects. If something is picked up, the program starts processing the captured images.<br>
If the detected object is not a vehicle, the image processing stops, and the radar operation continues. Otherwise, the program checks whether the detected vehicle poses a possible danger to the user.<br>
If it does not pose a danger, the program continues to process the captured images. If the program has perceived that the vehicle may pose a danger to the user, it activates the grips vibration mechanism to alert the user of the possible danger.<br>
As soon as the user is out of danger, the grips vibration mechanism stops.

## Flow Chart
<img src="images/flow_chart.png" alt="Flow Chart">

## Device Diagram
<img src="images/device_diagram.png" alt="Device Diagram">

## License
Distributed under the MIT License. See LICENSE.txt for more information.
