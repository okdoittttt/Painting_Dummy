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

        # Calculate corners of the bounding box
        top_left = (x_black, y_black)
        top_right = (x_black + w_black, y_black)
        bottom_left = (x_black, y_black + h_black)
        bottom_right = (x_black + w_black, y_black + h_black)

        # Prepare message with corner coordinates
        message = f"Corners: TL{top_left}, TR{top_right}, BL{bottom_left}, BR{bottom_right}, Distance: {distance} cm"
        
        # Send message with corners
        signal_socket.sendto(message.encode(), receiver_address)

        # Display corner information on the frame
        cv2.putText(color_frame, f"Corners: TL{top_left}, TR{top_right}, BL{bottom_left}, BR{bottom_right}",
                    (x_black, y_black - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

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
