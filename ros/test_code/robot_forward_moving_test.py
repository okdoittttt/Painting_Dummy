import os
import sys
import termios
import tty
import time
import curses
import threading
from dynamixel_sdk import *  # Uses Dynamixel SDK library

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

#********* DYNAMIXEL Model definition *********
MY_DXL = 'X_SERIES'

# Control table address
if MY_DXL == 'X_SERIES' or MY_DXL == 'MX_SERIES':
    ADDR_OPERATING_MODE = 11
    ADDR_TORQUE_ENABLE = 64
    ADDR_GOAL_VELOCITY = 104
    ADDR_PRESENT_POSITION = 132
    DXL_MINIMUM_POSITION_VALUE = 0
    DXL_MAXIMUM_POSITION_VALUE = 4067
    BAUDRATE = 57600

PROTOCOL_VERSION = 2.0
DXL_ID = 15
DEVICENAME = '/dev/ttyUSB0'
TORQUE_ENABLE = 1
TORQUE_DISABLE = 0
VELOCITY_CW = 50  # 시계 방향 속도
VELOCITY_CCW = -50  # 반시계 방향 속도
VELOCITY_STOP = 0  # 모터 정지 속도

portHandler = PortHandler(DEVICENAME)
packetHandler = PacketHandler(PROTOCOL_VERSION)

if portHandler.openPort():
    print("Succeeded to open the port")
else:
    print("Failed to open the port")
    print("Press any key to terminate...")
    getch()
    quit()

if portHandler.setBaudRate(BAUDRATE):
    print("Succeeded to change the baudrate")
else:
    print("Failed to change the baudrate")
    print("Press any key to terminate...")
    getch()
    quit()

for dxl_id in range(11, 16):
    
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

# move_thread 에서 동작을 감지하여 모터를 회전시키는 함수
moving = False
moving_dx_id = 11
direction = VELOCITY_CW
lock_move = threading.Lock()  # move 전용 락
current_direction = VELOCITY_STOP  # 현재 모터가 설정된 속도

moving_forward = False
moving_dx_id_12 = 12
moving_dx_id_13 = 13
direction_12 = VELOCITY_CW
direction_13 = VELOCITY_CW
lock_forward_move = threading.Lock()  # forward_move 전용 락
current_direction_12 = VELOCITY_STOP
current_direction_13 = VELOCITY_STOP

def move():
    global moving_dx_id, direction, current_direction
    current_dxl_id = moving_dx_id
    while True:
        with lock_move:
            if moving:
                dxl_present_position, dxl_comm_result, dxl_error = packetHandler.read4ByteTxRx(portHandler, moving_dx_id, ADDR_PRESENT_POSITION)
                if dxl_comm_result != COMM_SUCCESS:
                    print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
                elif dxl_error != 0:
                    print("%s" % packetHandler.getRxPacketError(dxl_error))

                print("current_motor_state : " + str(dxl_present_position))

                if current_dxl_id != moving_dx_id:
                    current_dxl_id = moving_dx_id
                if current_direction != direction:
                    # 모터의 속도가 이전 속도와 다를 때만 속도 명령을 전송
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
                    # 모터를 정지시키기 위해 속도를 0으로 설정
                    dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, moving_dx_id, ADDR_GOAL_VELOCITY, VELOCITY_STOP)
                    if dxl_comm_result != COMM_SUCCESS:
                        print(f"Failed to stop motor: {packetHandler.getTxRxResult(dxl_comm_result)}")
                    elif dxl_error != 0:
                        print(f"Error while stopping motor: {packetHandler.getRxPacketError(dxl_error)}")
                    else:
                        print(f"Stopped Dynamixel {moving_dx_id}.")
                    current_direction = VELOCITY_STOP

        time.sleep(0.05)  # CPU 과부하 방지를 위한 sleep 시간 조정


def moveForward():
    global moving_dx_id_12, moving_dx_id_13
    global direction_12, direction_13
    global current_direction_12, current_direction_13

    while True:
        with lock_forward_move:
            if moving_forward:

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

        time.sleep(0.05)  # CPU 과부하 방지를 위한 sleep 시간 조정

# 키 입력을 받는 curses 함수
def main(stdscr):
    global moving, moving_forward
    global direction, direction_12, direction_13
    global moving_dx_id

    stdscr.nodelay(True)
    stdscr.clear()
    stdscr.addstr(0, 0, "Press 'p' to move left, 'o' to move right, release to stop.")
    stdscr.refresh()

    # 백그라운드에서 모터를 제어하는 move 스레드 실행
    move_thread = threading.Thread(target=move)
    move_thread.daemon = True
    move_thread.start()

    forward_thread = threading.Thread(target=moveForward)
    forward_thread.daemon = True
    forward_thread.start()

    while True:
        key = stdscr.getch()
        if key == ord('d'):
            with lock_move:
                moving = True
                moving_dx_id = 11
                direction = VELOCITY_CW
        elif key == ord('a'):
            with lock_move:
                moving = True
                moving_dx_id = 11
                direction = VELOCITY_CCW
        elif key == ord('w'):
            with lock_forward_move:
                moving_forward = True
                direction_12 = VELOCITY_CW
                direction_13 = VELOCITY_CCW
        elif key == ord('s'):
            with lock_forward_move:
                moving_forward = True
                direction_12 = VELOCITY_CCW
                direction_13 = VELOCITY_CW
        elif key == ord('i'):
            with lock_move:
                moving = True
                moving_dx_id = 13
                direction = VELOCITY_CCW
        elif key == ord('k'):
            with lock_move:
                moving = True
                moving_dx_id = 13
                direction = VELOCITY_CW
        elif key == ord('o'):
            with lock_move:
                moving = True
                moving_dx_id = 14
                direction = VELOCITY_CCW
        elif key == ord('l'):
            with lock_move:
                moving = True
                moving_dx_id = 14
                direction = VELOCITY_CW

        elif key == curses.ERR:
            with lock_move:
                moving = False
            with lock_forward_move:
                moving_forward = False

        if key == 27:  # ESC key to exit
            break

        time.sleep(0.1)

curses.wrapper(main)

# 모든 Dynamixel 모터의 토크 비활성화
for dxl_id in range(11, 16):
    dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, dxl_id, ADDR_TORQUE_ENABLE, TORQUE_DISABLE)
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error))

portHandler.closePort()
