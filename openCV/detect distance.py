import cv2
import pyrealsense2
from pyscreeze import pixel

from realsense_depth import *

# 캠 위치의 400, 300 위치의 지점의 RGB와 거리(mm) 측정
point = (400, 300)

def show_distance(event, x, y, args, params):
    global point
    point = (x, y)

# Intel Realsense 카메라 초기화
dc = DepthCamera()

while True:
    # 카메라 초기화 함수
    ret, depth_frame, color_frame = dc.get_frame()

    # 400, 300 위치에 점을 표시
    cv2.circle(color_frame, point, 4, (0, 0, 255))

    # 카메라의 거리와 픽셀의 색을 추출하여 초기화
    distance = depth_frame[point[1], point[0]]
    pixel_color = color_frame[point[1], point[0]]
    print(f'픽셀 위치 ({point[0]}, {point[1]})의 색상: B={pixel_color[0]}, G={pixel_color[1]}, R={pixel_color[2]} 과 거리 = {distance}mm')

    # 카메라 출력
    cv2.imshow("depth frame", depth_frame)
    cv2.imshow("Color frame", color_frame)

    key = cv2.waitKey(1)
    if key == 27:
        break