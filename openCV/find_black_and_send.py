import cv2
from realsense_depth import *
import time
import socket

# Color configuration for black detection
min_contour_area = 100  # Minimum contour area for detection

# Initialize camera
dc = DepthCamera()

# Socket setup to send signal
signal_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
receiver_address = ('localhost', 12345)

# Black detection tracking variables
black_detected_start_time = None
black_detection_duration = 3  # Duration in seconds for which black should be detected

# Define HSV range for black
lower_black = (0, 0, 0)
upper_black = (180, 255, 50)  # Adjust upper limit as needed

while True:
    ret, depth_frame, color_frame, depth_info = dc.get_frame()
    hsvImage = cv2.cvtColor(color_frame, cv2.COLOR_BGR2HSV)

    # Create mask for black detection
    mask = cv2.inRange(hsvImage, lower_black, upper_black)

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    black_detected = False
    detected_coordinates = None  # Store coordinates and distance if black is detected

    for contour in contours:
        if cv2.contourArea(contour) > min_contour_area:
            black_detected = True
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(color_frame, (x, y), (x + w, y + h), (0, 255, 0), 5)  # Draw green rectangle
            distance = round(depth_info.get_distance(x, y) * 100)
            detected_coordinates = (x, y, distance)
            cv2.putText(color_frame, f"Coordinate: ({x}, {y}) Distance: {distance} cm",
                        (x - 50, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

    # Check for continuous black detection
    if black_detected:
        x, y, distance = detected_coordinates
        message = f"Black detected for 3 seconds. Coordinate: ({x}, {y}), Distance: {distance} cm"
        signal_socket.sendto(message.encode(), receiver_address)
        black_detected_start_time = None  # Reset after sending signal
    else:
        # Send "Not Detected" if black is not detected
        signal_socket.sendto("Not Detected".encode(), receiver_address)
        black_detected_start_time = None

    cv2.imshow("Color frame", color_frame)
    key = cv2.waitKey(1)
    if key == 27:
        dc.release()
        break

cv2.destroyAllWindows()
signal_socket.close()
