import cv2
from realsense_depth import *
import socket
import time

# Minimum width and height for black area detection
min_width = 50
min_height = 50

# Color configuration for black and red detection
min_contour_area = 100  # Minimum contour area for detection

# Define HSV ranges for black and red
lower_black = (0, 0, 0)
upper_black = (180, 255, 50)  # Adjust upper limit as needed

lower_red1 = (0, 70, 50)
upper_red1 = (15, 255, 255)
lower_red2 = (160, 70, 50)
upper_red2 = (180, 255, 255)

# Initialize camera
dc = DepthCamera()

# Socket setup to send signal
signal_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
receiver_address = ('localhost', 12345)

# Timer for black area detection
black_detection_interval = 0.5  # Interval in seconds
last_black_detection_time = 0

# Cached black area data
cached_black_data = None

while True:
    ret, depth_frame, color_frame, depth_info = dc.get_frame()
    hsvImage = cv2.cvtColor(color_frame, cv2.COLOR_BGR2HSV)

    # Check if it's time to re-detect black area
    current_time = time.time()
    # if current_time - last_black_detection_time > black_detection_interval:
    # Create mask for black detection
    mask_black = cv2.inRange(hsvImage, lower_black, upper_black)

    # Find contours for black areas
    contours_black, _ = cv2.findContours(mask_black, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Identify the largest black area that meets the width and height criteria
    max_contour = None
    max_contour_area = 0
    for contour_black in contours_black:
        area = cv2.contourArea(contour_black)
        if area > min_contour_area:
            x_black, y_black, w_black, h_black = cv2.boundingRect(contour_black)
            if w_black >= min_width and h_black >= min_height and area > max_contour_area:
                max_contour = contour_black
                max_contour_area = area

    if max_contour is not None:
        x_black, y_black, w_black, h_black = cv2.boundingRect(max_contour)
        cached_black_data = {
            "x": x_black,
            "y": y_black,
            "w": w_black,
            "h": h_black,
            "contour": max_contour
        }
    else:
        cached_black_data = None

    # last_black_detection_time = current_time

    # If black area is cached, process it
    if cached_black_data is not None:
        x_black = cached_black_data["x"]
        y_black = cached_black_data["y"]
        w_black = cached_black_data["w"]
        h_black = cached_black_data["h"]

        center_x_black = x_black + w_black // 2
        center_y_black = y_black + h_black // 2

        top_left_black = (x_black, y_black)
        top_right_black = (x_black + w_black, y_black)
        bottom_left_black = (x_black, y_black + h_black)
        bottom_right_black = (x_black + w_black, y_black + h_black)
        distance_black = round(depth_info.get_distance(x_black, y_black) * 100)

        # Draw green rectangle and display information
        cv2.rectangle(color_frame, (x_black, y_black), (x_black + w_black, y_black + h_black), (0, 255, 0), 5)
        cv2.circle(color_frame, (center_x_black, center_y_black), 5, (255, 0, 0), -1)  # Blue dot for center
        cv2.putText(color_frame, f"Black Center: ({center_x_black}, {center_y_black})",
                    (center_x_black - 50, center_y_black - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
        cv2.putText(color_frame, f"Corners: TL{top_left_black}, TR{top_right_black}, BL{bottom_left_black}, BR{bottom_right_black}",
                    (x_black, y_black - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

        # Send black area information via socket
        black_message = (f"Black Center: ({center_x_black}, {center_y_black}), "
                         f"Corners: TL{top_left_black}, TR{top_right_black}, "
                         f"BL{bottom_left_black}, BR{bottom_right_black}, Distance: {distance_black} cm")
        signal_socket.sendto(black_message.encode(), receiver_address)

        # Process non-red, non-black areas within the black region
        roi_hsv = hsvImage[y_black:y_black + h_black, x_black:x_black + w_black]
        mask_red_roi = cv2.bitwise_or(
            cv2.inRange(roi_hsv, lower_red1, upper_red1),
            cv2.inRange(roi_hsv, lower_red2, upper_red2)
        )
        mask_non_red = cv2.bitwise_not(mask_red_roi)
        mask_other_colors = cv2.bitwise_and(mask_non_red, cv2.bitwise_not(mask_black[y_black:y_black + h_black, x_black:x_black + w_black]))

        contours_other, _ = cv2.findContours(mask_other_colors, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Find the largest non-red, non-black area
        largest_other_contour = None
        largest_other_area = 0

        for contour_other in contours_other:
            area = cv2.contourArea(contour_other)
            if area > min_contour_area and area > largest_other_area:
                largest_other_contour = contour_other
                largest_other_area = area

        # If the largest non-red, non-black area is found, process it
        if largest_other_contour is not None:
            x_other, y_other, w_other, h_other = cv2.boundingRect(largest_other_contour)
            x_absolute, y_absolute = x_black + x_other, y_black + y_other  # Absolute coordinates
            center_x = x_absolute + w_other // 2
            center_y = y_absolute + h_other // 2
            top_left = (x_absolute, y_absolute)
            top_right = (x_absolute + w_other, y_absolute)
            bottom_left = (x_absolute, y_absolute + h_other)
            bottom_right = (x_absolute + w_other, y_absolute + h_other)

            # Draw yellow rectangle and display information
            cv2.rectangle(color_frame, (x_absolute, y_absolute), (x_absolute + w_other, y_absolute + h_other), (0, 255, 255), 5)
            cv2.circle(color_frame, (center_x, center_y), 5, (0, 0, 255), -1)
            cv2.putText(color_frame, f"Yellow Center: ({center_x}, {center_y})", 
                        (center_x - 50, center_y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

            # Send yellow area information via socket
            yellow_message = (f"Yellow Center: ({center_x}, {center_y}) /  TL{top_left}, TR{top_right}, "
                              f"BL{bottom_left}, BR{bottom_right}")
            signal_socket.sendto(yellow_message.encode(), receiver_address)
        else:
            # Send message if no yellow area is detected
            signal_socket.sendto("No yellow area detected".encode(), receiver_address)

    else:
        # Send message if no black area is detected
        signal_socket.sendto("No black area detected".encode(), receiver_address)

    # Display frame
    cv2.imshow("Color frame", color_frame)
    key = cv2.waitKey(1)
    if key == 27:
        dc.release()
        break

cv2.destroyAllWindows()
signal_socket.close()
