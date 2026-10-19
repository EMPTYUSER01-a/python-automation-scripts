# Screen Object Detector & Automation Script

This is a Python-based script that uses Computer Vision (OpenCV) to detect objects of specific colors on the screen and automatically simulate keyboard/controller inputs to interact with them.

## Features
- Real-time screen capturing using `mss`.
- Image processing and object detection using `OpenCV` (HSV color filtering, contours).
- Automated input simulation using `pydirectinput` and `vgamepad` (virtual controller).
- Modular logic for target selection and movement.

## Technologies Used
- Python 3
- OpenCV (cv2)
- NumPy
- mss (Screen capture)
- PyAutoGUI / pydirectinput / vgamepad

## How it works
The script captures a specific region of the screen, converts the image to HSV color space, and finds contours matching the target colors. Once a target is found, it calculates the coordinates and simulates the required inputs to move towards and interact with the target.

## Usage
*(You can describe how to run it here, e.g., `python screen_object_detector.py`)*
