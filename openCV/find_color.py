import cv2
from realsense_depth import *
from util import get_limits

red = [0, 0, 255]
# 최소 컨투어 면적을 설정 (너무 작은 점을 무시)
min_contour_area = 400    # 이 값을 조정하여 감지할 객체의 최소 크기를 설정하세요

# Intel Realsense 카메라 초기화
dc = DepthCamera()

while True:
    # 카메라 프레임 읽기
    ret, depth_frame, color_frame, depth_info = dc.get_frame()

    # BGR에서 HSV로 변환
    hsvImage = cv2.cvtColor(color_frame, cv2.COLOR_BGR2HSV)

    # 빨간색 범위에 해당하는 마스크 생성
    lowerLimit, upperLimit = get_limits(color=red)
    mask = cv2.inRange(hsvImage, lowerLimit, upperLimit)

    # 마스크에서 컨투어 찾기
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        if cv2.contourArea(contour) > min_contour_area:
            # 컨투어에서 모멘트 계산
            M = cv2.moments(contour)

            # 무게중심 (centroid) 좌표 계산
            # if M['m00'] != 0:
            #     center_x = int(M['m10'] / M['m00'])
            #     center_y = int(M['m01'] / M['m00'])
            # else:
            #     center_x, center_y = 0, 0

            # 컨투어에서 사각형 경계 구하기
            x, y, w, h = cv2.boundingRect(contour)

            # 사각형 그리기
            cv2.rectangle(color_frame, (x, y), (x + w, y + h), (0, 255, 0), 5)

            # 중심 좌표 표시 (원의 중심에 점 찍기)
            # cv2.circle(color_frame, (center_x, center_y), 5, (255, 0, 0), -1)

            # 좌표 표시 (왼쪽 상단에 점 찍기)
            cv2.circle(color_frame, (x, y), 5, (255, 0, 0), -1)
            # 좌표 텍스트로 화면에 출력
            #distance = depth_frame[center_x, center_y]
            # cv2.putText(color_frame, f"Center: ({center_x}, {center_y})",
            #             (center_x - 50, center_y - 10), cv2.FONT_HERSHEY_SIMPLEX,
            #             0.5, (255, 255, 255), 2)

            # 좌표 텍스트로 화면에 출력
            distance = round(depth_info.get_distance(x,y) * 100)
            cv2.putText(color_frame, f"Coordinate: ({x}, {y}) Distance: {distance}",
                            (x - 50, y - 10), cv2.FONT_HERSHEY_SIMPLEX,
                            0.5, (255, 255, 255), 2)


    # 결과 화면에 출력
    cv2.imshow("Color frame", color_frame)
    #cv2.imshow("Depth frame", depth_frame)
    # ESC 키 입력 시 루프 종료
    key = cv2.waitKey(1)
    if key == 27:
        dc.release()
        break

# 리소스 해제
cv2.destroyAllWindows()
