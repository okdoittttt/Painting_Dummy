import os
import sys
import termios
import tty
import time
import curses
from dynamixel_sdk import *  # Dynamixel SDK 라이브러리 사용

# 윈도우와 리눅스/맥에서 다른 키보드 입력 함수
if os.name == 'nt':  # 윈도우일 경우
    import msvcrt
    def getch():
        return msvcrt.getch().decode()
else:  # 리눅스/맥일 경우
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    def getch():
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

# ********* DYNAMIXEL 모델 정의 *********
MY_DXL = 'X_SERIES'  # 사용할 Dynamixel 모델

# 제어 테이블 주소 정의
if MY_DXL == 'X_SERIES' or MY_DXL == 'MX_SERIES':
    ADDR_OPERATING_MODE = 11  # 운영 모드 설정 주소
    ADDR_TORQUE_ENABLE = 64  # 토크 활성화 주소
    ADDR_GOAL_VELOCITY = 104  # 목표 속도 주소
    ADDR_PRESENT_POSITION = 132  # 현재 위치 주소
    DXL_MINIMUM_POSITION_VALUE = 0  # 최소 위치 값
    DXL_MAXIMUM_POSITION_VALUE = 4067  # 최대 위치 값
    BAUDRATE = 57600  # 통신 속도

# 통신에 필요한 기본 설정
PROTOCOL_VERSION = 2.0  # 프로토콜 버전
DXL_ID = 15  # 제어할 Dynamixel ID
DEVICENAME = '/dev/ttyUSB0'  # 포트 이름
TORQUE_ENABLE = 1  # 토크 활성화 값
TORQUE_DISABLE = 0  # 토크 비활성화 값
VELOCITY_CW = 50  # 시계 방향 속도
VELOCITY_CCW = -50  # 반시계 방향 속도
VELOCITY_STOP = 0  # 모터 정지 속도

# 포트와 패킷 핸들러 초기화
portHandler = PortHandler(DEVICENAME)
packetHandler = PacketHandler(PROTOCOL_VERSION)

# 포트 열기
if portHandler.openPort():
    print("Succeeded to open the port")
else:
    print("Failed to open the port")
    print("Press any key to terminate...")
    getch()
    quit()

# Baudrate 설정
if portHandler.setBaudRate(BAUDRATE):
    print("Succeeded to change the baudrate")
else:
    print("Failed to change the baudrate")
    print("Press any key to terminate...")
    getch()
    quit()

for dxl_id in range(11,16):
    dxl_comm_result, dxl_error = packetHandler.reboot(portHandler, dxl_id)
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error))

    print("[ID:%03d] reboot Succeeded\n" % dxl_id)


# 각 Dynamixel의 Wheel Mode 설정 및 토크 활성화
for dxl_id in range(10, 16):
    dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, dxl_id, ADDR_OPERATING_MODE, 1)
    if dxl_comm_result != COMM_SUCCESS:
        print(f"Failed to set wheel mode: {packetHandler.getTxRxResult(dxl_comm_result)}")
    elif dxl_error != 0:
        print(f"Error while setting wheel mode: {packetHandler.getRxPacketError(dxl_error)}")
    else:
        print(f"Dynamixel {dxl_id} is in Wheel Mode.")

    dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, dxl_id, ADDR_TORQUE_ENABLE, TORQUE_ENABLE)
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error))
    else:
        print(f"Dynamixel has been successfully connected DXL_ID : {dxl_id}")

    

# 모터를 제어하는 함수 관련 변수 설정
moving = False  # 기본적으로 이동 중 아님
moving_dx_id = 11  # 제어할 모터 ID
direction = VELOCITY_CW  # 기본 방향 시계 방향
current_direction = VELOCITY_STOP  # 현재 방향 정지 상태

# 두 모터를 동시에 제어하는 변수 설정
moving_forward = False  # 전진 중 아님
moving_dx_id_12 = 12  # 제어할 모터 ID
moving_dx_id_13 = 13  # 제어할 모터 ID
direction_12 = VELOCITY_CW  # 모터 12 시계 방향
direction_13 = VELOCITY_CW  # 모터 13 시계 방향
current_direction_12 = VELOCITY_STOP  # 모터 12 정지 상태
current_direction_13 = VELOCITY_STOP  # 모터 13 정지 상태


# 모터를 제어하는 함수
def move_and_forward():
    global moving_dx_id, direction, current_direction
    global moving_dx_id_12, moving_dx_id_13
    global direction_12, direction_13
    global current_direction_12, current_direction_13
    global moving, moving_forward

    # 단일 모터 제어
    if moving:
        if current_direction != direction:
            dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, moving_dx_id, ADDR_GOAL_VELOCITY, direction)
            if dxl_comm_result != COMM_SUCCESS:
                print(f"Failed to set velocity: {packetHandler.getTxRxResult(dxl_comm_result)}")
            elif dxl_error != 0:
                print(f"Error while setting velocity: {packetHandler.getRxPacketError(dxl_error)}")
            else:
                print(f"Set Dynamixel {moving_dx_id} velocity to {direction}.")
            current_direction = direction
    else:
        if current_direction != VELOCITY_STOP:
            dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, moving_dx_id, ADDR_GOAL_VELOCITY, VELOCITY_STOP)
            if dxl_comm_result != COMM_SUCCESS:
                print(f"Failed to stop motor: {packetHandler.getTxRxResult(dxl_comm_result)}")
            elif dxl_error != 0:
                print(f"Error while stopping motor: {packetHandler.getRxPacketError(dxl_error)}")
            else:
                print(f"Stopped Dynamixel {moving_dx_id}.")
            current_direction = VELOCITY_STOP

    # 두 모터 동시 제어
    if moving_forward:
        print(f"Current Position: {check_motor_position(12)}")
        if current_direction_12 != direction_12:
            dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, moving_dx_id_12, ADDR_GOAL_VELOCITY, direction_12)
            if dxl_comm_result != COMM_SUCCESS:
                print(f"Failed to set velocity: {packetHandler.getTxRxResult(dxl_comm_result)}")
            elif dxl_error != 0:
                print(f"Error while setting velocity: {packetHandler.getRxPacketError(dxl_error)}")
            else:
                print(f"Set Dynamixel {moving_dx_id_12} velocity to {direction_12}.")
            current_direction_12 = direction_12

        if current_direction_13 != direction_13:
            dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, moving_dx_id_13, ADDR_GOAL_VELOCITY, direction_13)
            if dxl_comm_result != COMM_SUCCESS:
                print(f"Failed to set velocity: {packetHandler.getTxRxResult(dxl_comm_result)}")
            elif dxl_error != 0:
                print(f"Error while setting velocity: {packetHandler.getRxPacketError(dxl_error)}")
            else:
                print(f"Set Dynamixel {moving_dx_id_13} velocity to {direction_13}.")
            current_direction_13 = direction_13
    else:
        if current_direction_12 != VELOCITY_STOP:
            dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, moving_dx_id_12, ADDR_GOAL_VELOCITY, VELOCITY_STOP)
            if dxl_comm_result != COMM_SUCCESS:
                print(f"Failed to stop motor: {packetHandler.getTxRxResult(dxl_comm_result)}")
            elif dxl_error != 0:
                print(f"Error while stopping motor: {packetHandler.getRxPacketError(dxl_error)}")
            else:
                print(f"Stopped Dynamixel {moving_dx_id_12}.")
            current_direction_12 = VELOCITY_STOP

        if current_direction_13 != VELOCITY_STOP:
            dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, moving_dx_id_13, ADDR_GOAL_VELOCITY, VELOCITY_STOP)
            if dxl_comm_result != COMM_SUCCESS:
                print(f"Failed to stop motor: {packetHandler.getTxRxResult(dxl_comm_result)}")
            elif dxl_error != 0:
                print(f"Error while stopping motor: {packetHandler.getRxPacketError(dxl_error)}")
            else:
                print(f"Stopped Dynamixel {moving_dx_id_13}.")
            current_direction_13 = VELOCITY_STOP

def check_motor_position(moving_dx_id) :
    dxl_present_position, dxl_comm_result, dxl_error = packetHandler.read4ByteTxRx(portHandler, moving_dx_id, ADDR_PRESENT_POSITION)
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error))
    print(f"Current Position : {dxl_present_position}.")
    return dxl_present_position
    

def initiallize_poze(dx_id) :
    move_to_front=VELOCITY_CCW
    move_to_back=VELOCITY_CW
    check_current_poze_start = 200
    check_current_poze_end = 2000
    limit_range_start_to_front = 0
    limit_range_end_to_front = 10
    limit_range_start_to_back = 4000
    limit_range_end_to_back = 4010
    
    if (dx_id == 13) :
        move_to_front=VELOCITY_CW
        move_to_back=VELOCITY_CCW
        check_current_poze_start = 0
        check_current_poze_end = 910
        limit_range_start_to_front = 929
        limit_range_end_to_front = 939
        limit_range_start_to_back = 929
        limit_range_end_to_back = 939

    if check_current_poze_start <= check_motor_position(dx_id) <= check_current_poze_end :
        while True :
            dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, dx_id, ADDR_GOAL_VELOCITY, move_to_front)
            if dxl_comm_result != COMM_SUCCESS:
                print(f"Failed to set velocity: {packetHandler.getTxRxResult(dxl_comm_result)}")
            elif dxl_error != 0:
                print(f"Error while setting velocity: {packetHandler.getRxPacketError(dxl_error)}")
            else :
                print(f"Moving {dx_id} CCW...")

            if limit_range_start_to_front <= check_motor_position(dx_id) <= limit_range_end_to_front :
                dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, dx_id, ADDR_GOAL_VELOCITY, 0)
                if dxl_comm_result != COMM_SUCCESS:
                    print(f"Failed to set velocity: {packetHandler.getTxRxResult(dxl_comm_result)}")
                elif dxl_error != 0:
                    print(f"Error while setting velocity: {packetHandler.getRxPacketError(dxl_error)}")
                else :
                    print(f"STOP {dx_id} CCW!!")
                break
            

    elif check_current_poze_end < check_motor_position(dx_id) :
        while True :
            dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, dx_id, ADDR_GOAL_VELOCITY, move_to_back)
            if dxl_comm_result != COMM_SUCCESS:
                print(f"Failed to set velocity: {packetHandler.getTxRxResult(dxl_comm_result)}")
            elif dxl_error != 0:
                print(f"Error while setting velocity: {packetHandler.getRxPacketError(dxl_error)}")
            else :
                print(f"Moving {dx_id} CW...")

            if limit_range_start_to_back <= check_motor_position(dx_id) <= limit_range_end_to_back :
                dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, dx_id, ADDR_GOAL_VELOCITY, 0)
                if dxl_comm_result != COMM_SUCCESS:
                    print(f"Failed to set velocity: {packetHandler.getTxRxResult(dxl_comm_result)}")
                elif dxl_error != 0:
                    print(f"Error while setting velocity: {packetHandler.getRxPacketError(dxl_error)}")
                else :
                    print(f"STOP {dx_id} CW!!")

                break
            # time.sleep(0.1)
            

# 키보드 입력 처리 함수 (curses 사용)
def main(stdscr):
    global moving, moving_forward
    global direction, direction_12, direction_13
    global moving_dx_id

    stdscr.nodelay(True)
    stdscr.clear()
    stdscr.addstr(0, 0, "Press 'p' to move left, 'o' to move right, release to stop.")
    stdscr.refresh()
    stdscr.addstr(1,0, str(check_motor_position(13)))
    
    
    initiallize_poze(12)
    initiallize_poze(11)
    initiallize_poze(13)

    while True:
        key = stdscr.getch()
        if key == ord('d'):
            moving = True
            moving_dx_id = 11
            direction = VELOCITY_CW
        elif key == ord('a'):
            moving = True
            moving_dx_id = 11
            direction = VELOCITY_CCW
        elif key == ord('w'):
            moving_forward = True
            direction_12 = VELOCITY_CW
            direction_13 = VELOCITY_CCW
        elif key == ord('s'):
            moving_forward = True
            direction_12 = VELOCITY_CCW
            direction_13 = VELOCITY_CW
        elif key == ord('i'):
            moving = True
            moving_dx_id = 13
            direction = VELOCITY_CCW
        elif key == ord('k'):
            moving = True
            moving_dx_id = 13
            direction = VELOCITY_CW
        elif key == ord('o'):
            moving = True
            moving_dx_id = 14
            direction = VELOCITY_CCW
        elif key == ord('l'):
            moving = True
            moving_dx_id = 14
            direction = VELOCITY_CW

        elif key == curses.ERR:
            moving = False
            moving_forward = False

        if key == 27:  # ESC key to exit
            break

        # 모터 제어 함수 호출
        move_and_forward()

        time.sleep(0.1)

curses.wrapper(main)

# 모든 Dynamixel 모터의 토크 비활성화
for dxl_id in range(11, 16):
    dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, dxl_id, ADDR_TORQUE_ENABLE, TORQUE_DISABLE)
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error))

# 포트 닫기
portHandler.closePort()
