import cv2
from realsense_depth import *
from util import get_limits
import time
import socket

# Color configuration
red = [0, 0, 255]
min_contour_area = 400  # Minimum contour area for detection

# Initialize camera
dc = DepthCamera()

# Socket setup to send signal
signal_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
receiver_address = ('localhost', 12345)

# Red detection tracking variables
red_detected_start_time = None
red_detection_duration = 3  # Duration in seconds for which red should be detected

while True:
    ret, depth_frame, color_frame, depth_info = dc.get_frame()
    hsvImage = cv2.cvtColor(color_frame, cv2.COLOR_BGR2HSV)
    lowerLimit, upperLimit = get_limits(color=red)
    mask = cv2.inRange(hsvImage, lowerLimit, upperLimit)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    red_detected = False
    detected_coordinates = None  # Store coordinates and distance if red is detected

    for contour in contours:
        if cv2.contourArea(contour) > min_contour_area:
            red_detected = True
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(color_frame, (x, y), (x + w, y + h), (0, 255, 0), 5)
            distance = round(depth_info.get_distance(x, y) * 100)
            detected_coordinates = (x, y, distance)
            cv2.putText(color_frame, f"Coordinate: ({x}, {y}) Distance: {distance}",
                        (x - 50, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

    # Check for continuous red detection
    if red_detected:
        x, y, distance = detected_coordinates
        message = f"Red detected for 3 seconds. Coordinate: ({x}, {y}), Distance: {distance} cm"
        signal_socket.sendto(message.encode(), receiver_address)
        red_detected_start_time = None  # Reset after sending signal
    else:
        # Send "Not Detected" if red is not detected
        signal_socket.sendto("Not Detected".encode(), receiver_address)
        red_detected_start_time = None

    cv2.imshow("Color frame", color_frame)
    key = cv2.waitKey(1)
    if key == 27:
        dc.release()
        break

cv2.destroyAllWindows()
signal_socket.close()
