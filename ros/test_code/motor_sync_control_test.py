import os
import sys
import termios
import tty
import time
import curses
import threading
from dynamixel_sdk import *  # Dynamixel SDK를 사용하여 모터 제어

# Windows와 Unix 시스템에서 각각 다른 방식으로 키 입력을 받기 위해 getch 함수 정의
if os.name == 'nt':
    import msvcrt
    def getch():
        return msvcrt.getch().decode()
else:
    import sys, tty, termios
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    def getch():
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

# ********* DYNAMIXEL Model definition *********
MY_DXL = 'X_SERIES'  # Dynamixel 모델 설정

# Control table address: Dynamixel 제어 테이블 주소 설정
if MY_DXL == 'X_SERIES' or MY_DXL == 'MX_SERIES':
    ADDR_TORQUE_ENABLE = 64  # 모터 토크 제어 주소
    ADDR_GOAL_POSITION = 116  # 목표 위치 주소
    ADDR_PRESENT_POSITION = 132  # 현재 위치 주소
    DXL_MINIMUM_POSITION_VALUE = 0  # 최소 위치 값
    DXL_MAXIMUM_POSITION_VALUE = 4067  # 최대 위치 값
    BAUDRATE = 57600  # 통신 속도 설정

PROTOCOL_VERSION = 2.0  # 프로토콜 버전
DXL_ID = 15  # Dynamixel ID 설정 (이 코드에서는 사용되지 않음)
DEVICENAME = '/dev/ttyUSB0'  # 연결할 장치 이름 (리눅스 환경의 시리얼 포트)
TORQUE_ENABLE = 1  # 모터 활성화
TORQUE_DISABLE = 0  # 모터 비활성화

# 포트 및 패킷 핸들러 생성
portHandler = PortHandler(DEVICENAME)
packetHandler = PacketHandler(PROTOCOL_VERSION)

# 포트 오픈 확인
if portHandler.openPort():
    print("Succeeded to open the port")
else:
    print("Failed to open the port")
    print("Press any key to terminate...")
    getch()
    quit()

# 통신 속도 설정 확인
if portHandler.setBaudRate(BAUDRATE):
    print("Succeeded to change the baudrate")
else:
    print("Failed to change the baudrate")
    print("Press any key to terminate...")
    getch()
    quit()

# 모터 ID 11과 12의 토크 활성화
for dxl_id in range(11, 13):
    dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, dxl_id, ADDR_TORQUE_ENABLE, TORQUE_ENABLE)
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error))
    else:
        print(f"Dynamixel has been successfully connected DXL_ID : {dxl_id}")

# 모터 11, 12의 상태를 위한 글로벌 변수 설정
moving_11 = False  # 모터 11 움직임 여부
moving_dx_id_11 = 11  # 모터 11 ID
direction_11 = 1  # 모터 11의 이동 방향

moving_12 = False  # 모터 12 움직임 여부
moving_dx_id_12 = 12  # 모터 12 ID
direction_12 = 1  # 모터 12의 이동 방향

lock_11 = threading.Lock()  # 모터 11 제어에 사용되는 쓰레드 락
lock_12 = threading.Lock()  # 모터 12 제어에 사용되는 쓰레드 락

# 모터 11을 제어하는 함수
def move11():
    global moving_dx_id_11, direction_11, moving_dx_id_12, direction_12

    # 모터 11, 12의 현재 위치 읽기
    dxl_present_position_11, dxl_comm_result_11, dxl_error_11 = packetHandler.read4ByteTxRx(portHandler, moving_dx_id_11, ADDR_PRESENT_POSITION)
    if dxl_comm_result_11 != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result_11))
    elif dxl_error_11 != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error_11))

    move_step_11 = dxl_present_position_11

    dxl_present_position_12, dxl_comm_result_12, dxl_error_12 = packetHandler.read4ByteTxRx(portHandler, moving_dx_id_12, ADDR_PRESENT_POSITION)
    if dxl_comm_result_12 != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result_12))
    elif dxl_error != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error_12))

    move_step_12 = dxl_present_position_12  

    while True:
        with lock_11:  # 쓰레드 안전성 확보
            if moving_11:  # 모터 11이 움직일 때
                move_step_11 += 13 * direction_11  # 이동 단계 설정
                move_step_12 += 13 * direction_12  # 모터 12도 함께 이동
                
                # 위치 값 제한
                if move_step_11 >= 4067:
                    move_step_11 = 4067
                elif move_step_11 < 0 :
                    move_step_11 = 0

                if move_step_12 >= 4067:
                    move_step_12 = 4067
                elif move_step_12 < 0 :
                    move_step_12 = 0

                # 목표 위치로 모터 이동
                dxl_comm_result_11, dxl_error_11 = packetHandler.write4ByteTxRx(portHandler, moving_dx_id_11, ADDR_GOAL_POSITION, move_step_11)
                if dxl_comm_result_11 != COMM_SUCCESS:
                    print("%s" % packetHandler.getTxRxResult(dxl_comm_result_11))
                elif dxl_error_11 != 0:
                    print("%s" % packetHandler.getRxPacketError(dxl_error_11))
                
                dxl_comm_result_12, dxl_error_12 = packetHandler.write4ByteTxRx(portHandler, moving_dx_id_11, ADDR_GOAL_POSITION, move_step_12)
                if dxl_comm_result_12 != COMM_SUCCESS:
                    print("%s" % packetHandler.getTxRxResult(dxl_comm_result_12))
                elif dxl_error_12 != 0:
                    print("%s" % packetHandler.getRxPacketError(dxl_error_12))

                print(f"${move_step_11} / ${move_step_12}")  # 현재 위치 출력

        time.sleep(0.01)

# 모터 12 제어 함수
def move12():
    global moving_dx_id_12, direction_12
    dxl_present_position_12, dxl_comm_result_12, dxl_error_12 = packetHandler.read4ByteTxRx(portHandler, moving_dx_id_12, ADDR_PRESENT_POSITION)
    if dxl_comm_result_12 != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result_12))
    elif dxl_error != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error_12))

    move_step = dxl_present_position_12

    while True:
        with lock_12:
            if moving_12:  # 모터 12가 움직일 때
                move_step += 13 * direction_12  # 이동 단계 설정

                # 위치 값 제한
                if move_step >= 4067:
                    move_step = 4067
                elif move_step < 0:
                    move_step = 0

                dxl_comm_result_12, dxl_error_12 = packetHandler.write4ByteTxRx(portHandler, moving_dx_id_12, ADDR_GOAL_POSITION, move_step)
                print(move_step)
                if dxl_comm_result_12 != COMM_SUCCESS:
                    print("%s" % packetHandler.getTxRxResult(dxl_comm_result_12))
                elif dxl_error != 0:
                    print("%s" % packetHandler.getRxPacketError(dxl_error_12))
        time.sleep(0.01)

# curses를 이용해 키보드 입력을 처리하는 함수
def main(stdscr):
    global moving_11, moving_12, direction_11, direction_12, moving_dx_id_11, moving_dx_id_12

    stdscr.nodelay(True)  # 입력 대기 없이 바로 처리
    stdscr.clear()
    stdscr.addstr(0, 0, "Press and hold the 'q' key to increase and 'a' key to decrease. Release to stop.")
    stdscr.addstr(1, 0, "Press and hold the 'w' key to increase and 's' key to decrease. Release to stop.")

    # 현재 위치 출력
    dxl_present_position_11, dxl_comm_result_11, dxl_error_11 = packetHandler.read4ByteTxRx(portHandler, moving_dx_id_11, ADDR_PRESENT_POSITION)
    stdscr.addstr(5, 0, f"{moving_dx_id_11} : {direction_11} / {dxl_present_position_11}")
    if dxl_comm_result_11 != COMM_SUCCESS:
        stdscr.addstr(6, 0, f"{packetHandler.getTxRxResult(dxl_comm_result_11)}")
    elif dxl_error_11 != 0:
        stdscr.addstr(6, 0, f"{packetHandler.getTxRxResult(dxl_error_11)}")

    dxl_present_position_12, dxl_comm_result_12, dxl_error_12 = packetHandler.read4ByteTxRx(portHandler, moving_dx_id_12, ADDR_PRESENT_POSITION)
    stdscr.addstr(5, 0, f"{moving_dx_id_12} : {direction_12} / {dxl_present_position_12}")
    if dxl_comm_result_12 != COMM_SUCCESS:
        stdscr.addstr(6, 0, f"{packetHandler.getTxRxResult(dxl_comm_result_12)}")
    elif dxl_error_12 != 0:
        stdscr.addstr(6, 0, f"{packetHandler.getTxRxResult(dxl_error_12)}")

    stdscr.refresh()

    # 각 모터에 대한 제어 쓰레드 시작
    count_thread_11 = threading.Thread(target=move11)
    count_thread_11.daemon = True
    count_thread_11.start()

    count_thread_12 = threading.Thread(target=move12)
    count_thread_12.daemon = True
    count_thread_12.start()
    
    while True:
        key = stdscr.getch()

        # 키보드 입력에 따라 모터 제어
        if key == ord('q'):
            with lock_11:
                moving_11 = True
                moving_12 = True
                direction_11 = 1
                direction_12 = 1
        elif key == ord('a'):
            with lock_11:
                moving_11 = True
                moving_12 = True
                direction_11 = -1
                direction_12 = -1
        elif key == ord('w'):
            with lock_12:
                moving_12 = True
                direction_12 = 1
        elif key == ord('s'):
            with lock_12:
                moving_12 = True
                direction_12 = -1
        else:
            with lock_11:
                moving_11 = False
            with lock_12:
                moving_12 = False

        if key == 27:  # ESC 키가 눌리면 종료
            break

        time.sleep(0.1)

# curses.wrapper는 curses 라이브러리를 안전하게 초기화 및 종료하는 방법
curses.wrapper(main)

# 프로그램 종료 후 토크 비활성화
for dxl_id in range(11, 13):
    dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, dxl_id, ADDR_TORQUE_ENABLE, TORQUE_DISABLE)
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error))

portHandler.closePort()  # 포트 닫기
