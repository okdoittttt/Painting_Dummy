import cv2
from realsense_depth import *
import time
import socket

# Color configuration for black and red detection
min_contour_area = 100  # Minimum contour area for detection

# Initialize camera
dc = DepthCamera()

# Socket setup to send signal
signal_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
receiver_address = ('localhost', 12345)

# Define HSV ranges for black and red
lower_black = (0, 0, 0)
upper_black = (180, 255, 50)  # Adjust upper limit as needed

# Define wide HSV range for red
lower_red1 = (0, 70, 50)
upper_red1 = (15, 255, 255)
lower_red2 = (160, 70, 50)
upper_red2 = (180, 255, 255)

while True:
    ret, depth_frame, color_frame, depth_info = dc.get_frame()
    hsvImage = cv2.cvtColor(color_frame, cv2.COLOR_BGR2HSV)

    # Create mask for black detection
    mask_black = cv2.inRange(hsvImage, lower_black, upper_black)

    # Create masks for red detection using the two red ranges
    mask_red1 = cv2.inRange(hsvImage, lower_red1, upper_red1)
    mask_red2 = cv2.inRange(hsvImage, lower_red2, upper_red2)
    mask_red = cv2.bitwise_or(mask_red1, mask_red2)  # Combine both masks

    # Find contours for black areas
    contours_black, _ = cv2.findContours(mask_black, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    max_contour = None
    max_contour_area = 0

    # Identify the largest black area
    for contour_black in contours_black:
        area = cv2.contourArea(contour_black)
        if area > min_contour_area and area > max_contour_area:
            max_contour = contour_black
            max_contour_area = area

    # If a large black area is detected, process it
    if max_contour is not None:
        x_black, y_black, w_black, h_black = cv2.boundingRect(max_contour)
        cv2.rectangle(color_frame, (x_black, y_black), (x_black + w_black, y_black + h_black), (0, 255, 0), 5)  # Draw green rectangle for the largest black area
        distance = round(depth_info.get_distance(x_black, y_black) * 100)

        # Check for non-red, non-black areas within the largest black area
        roi_hsv = hsvImage[y_black:y_black + h_black, x_black:x_black + w_black]
        
        # Mask for detecting non-red, non-black areas
        mask_non_red = cv2.bitwise_not(mask_red[y_black:y_black + h_black, x_black:x_black + w_black])
        mask_non_black = cv2.bitwise_not(mask_black[y_black:y_black + h_black, x_black:x_black + w_black])
        mask_other_colors = cv2.bitwise_and(mask_non_red, mask_non_black)  # Areas that are neither red nor black

        # Find contours of non-red, non-black areas within the black region
        contours_other, _ = cv2.findContours(mask_other_colors, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Variable to check if any non-red, non-black area is detected
        non_red_non_black_detected = False

        for contour_other in contours_other:
            if cv2.contourArea(contour_other) > min_contour_area:
                non_red_non_black_detected = True
                x_other, y_other, w_other, h_other = cv2.boundingRect(contour_other)
                x_absolute, y_absolute = x_black + x_other, y_black + y_other  # Convert to absolute coordinates
                cv2.rectangle(color_frame, (x_absolute, y_absolute), (x_absolute + w_other, y_absolute + h_other), (0, 255, 255), 5)  # Yellow box for non-red, non-black within black

        # Send message based on whether non-red, non-black areas were detected
        if non_red_non_black_detected:
            message = f"Largest black area detected at ({x_black}, {y_black}), Distance: {distance} cm. 빨간색이 아닌 영역이 검은색 내부에 있습니다."
        else:
            message = f"Largest black area detected at ({x_black}, {y_black}), Distance: {distance} cm."
        signal_socket.sendto(message.encode(), receiver_address)
        cv2.putText(color_frame, f"Coordinate: ({x_black}, {y_black}) Distance: {distance} cm",
                    (x_black - 50, y_black - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

    else:
        # Send "Not Detected" if no large black area is found
        signal_socket.sendto("Not Detected".encode(), receiver_address)

    cv2.imshow("Color frame", color_frame)
    key = cv2.waitKey(1)
    if key == 27:
        dc.release()
        break

cv2.destroyAllWindows()
signal_socket.close()
