import pyrealsense2 as rs  # Intel RealSense 라이브러리로, RealSense 카메라 기능에 접근하기 위한 라이브러리
import numpy as np  # 배열 연산을 위한 NumPy 라이브러리

class DepthCamera:
    def __init__(self):
        # 카메라 파이프라인 초기화
        self.pipeline = rs.pipeline()
        config = rs.config()  # 카메라 설정을 지정하기 위한 설정 객체 생성

        # 장치 정보를 가져오기 위한 래퍼
        pipeline_wrapper = rs.pipeline_wrapper(self.pipeline)
        pipeline_profile = config.resolve(pipeline_wrapper)  # 현재 장치에 대한 설정을 해결
        device = pipeline_profile.get_device()  # 파이프라인에서 장치 객체 가져오기
        device_product_line = str(device.get_info(rs.camera_info.product_line))  # 장치의 제품 라인 정보 가져오기

        # 깊이 스트림과 컬러 스트림 활성화 (깊이는 16비트 형식, 컬러는 BGR 형식)
        config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)  # 해상도 640x480, 30 FPS로 깊이 스트림 설정
        config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)  # 해상도 640x480, 30 FPS로 컬러 스트림 설정

        # 위 설정으로 카메라 파이프라인 시작
        self.pipeline.start(config)

    def get_frame(self):
        # 일관된 프레임 세트(깊이와 컬러 둘 다)를 기다림
        frames = self.pipeline.wait_for_frames()
        depth_frame = frames.get_depth_frame()  # 깊이 프레임 가져오기
        color_frame = frames.get_color_frame()  # 컬러 프레임 가져오기

        # 프레임을 NumPy 배열로 변환
        depth_image = np.asanyarray(depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())

        # 프레임이 성공적으로 캡처되었는지 확인
        if not depth_frame or not color_frame:
            return False, None, None  # 프레임 중 하나라도 없으면 False 반환
        return True, depth_image, color_image  # 깊이와 컬러 이미지가 있으면 True와 함께 반환

    def release(self):
        # 카메라 파이프라인 중지 (리소스 정리)
        self.pipeline.stop()