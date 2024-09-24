import os
import dynamixel_sdk as dxl
import keyboard  # 키보드 입력을 처리하는 라이브러리
import time

# Control table address
ADDR_TORQUE_ENABLE = 64
ADDR_GOAL_VELOCITY = 104
ADDR_PRESENT_VELOCITY = 128
ADDR_OPERATING_MODE = 11

# Data Byte Length
LEN_GOAL_VELOCITY = 4
LEN_PRESENT_VELOCITY = 4

# Protocol version
PROTOCOL_VERSION = 2.0

# Default setting
DXL_ID = 11  # 사용할 모터 ID
BAUDRATE = 57600
DEVICENAME = '/dev/ttyUSB0'  # Linux 포트

TORQUE_ENABLE = 1  # Enable Torque
TORQUE_DISABLE = 0  # Disable Torque
VELOCITY_CW = 200  # 시계 방향 속도
VELOCITY_CCW = -200  # 반시계 방향 속도
VELOCITY_ZERO = 0  # 속도 정지

portHandler = dxl.PortHandler(DEVICENAME)
packetHandler = dxl.PacketHandler(PROTOCOL_VERSION)

# 포트 열기
if portHandler.openPort():
    print("Succeeded to open the port")
else:
    print("Failed to open the port")
    quit()

# 통신 속도 설정
if portHandler.setBaudRate(BAUDRATE):
    print("Succeeded to change the baudrate")
else:
    print("Failed to change the baudrate")
    quit()

# 모터를 Wheel Mode로 설정
def set_wheel_mode(dxl_id):
    # Wheel Mode 설정 (Operating Mode를 1로 설정)
    dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, dxl_id, ADDR_OPERATING_MODE, 1)
    if dxl_comm_result != dxl.COMM_SUCCESS:
        print(f"{packetHandler.getTxRxResult(dxl_comm_result)}")
    elif dxl_error != 0:
        print(f"{packetHandler.getRxPacketError(dxl_error)}")
    else:
        print(f"Dynamixel {dxl_id} is in Wheel Mode.")

# 모터 속도 설정
def set_motor_velocity(dxl_id, velocity):
    # 목표 속도 설정
    dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, dxl_id, ADDR_GOAL_VELOCITY, velocity)
    if dxl_comm_result != dxl.COMM_SUCCESS:
        print(f"{packetHandler.getTxRxResult(dxl_comm_result)}")
    elif dxl_error != 0:
        print(f"{packetHandler.getRxPacketError(dxl_error)}")
    else:
        print(f"Set Dynamixel {dxl_id} velocity to {velocity}.")

# Torque Enable
def enable_torque(dxl_id):
    dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, dxl_id, ADDR_TORQUE_ENABLE, TORQUE_ENABLE)
    if dxl_comm_result != dxl.COMM_SUCCESS:
        print(f"{packetHandler.getTxRxResult(dxl_comm_result)}")
    elif dxl_error != 0:
        print(f"{packetHandler.getRxPacketError(dxl_error)}")
    else:
        print(f"Torque enabled for Dynamixel {dxl_id}")

# Torque Disable
def disable_torque(dxl_id):
    dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, dxl_id, ADDR_TORQUE_ENABLE, TORQUE_DISABLE)
    if dxl_comm_result != dxl.COMM_SUCCESS:
        print(f"{packetHandler.getTxRxResult(dxl_comm_result)}")
    elif dxl_error != 0:
        print(f"{packetHandler.getRxPacketError(dxl_error)}")
    else:
        print(f"Torque disabled for Dynamixel {dxl_id}")

# Wheel Mode 설정
set_wheel_mode(DXL_ID)

# Torque Enable
enable_torque(DXL_ID)

# 무한 루프 안에서 키 입력을 감지하여 모터를 제어
try:
    while True:
        if keyboard.is_pressed('p'):  # 'p' 키가 눌리면 왼쪽으로 회전
            set_motor_velocity(DXL_ID, VELOCITY_CCW)
        elif keyboard.is_pressed('o'):  # 'o' 키가 눌리면 오른쪽으로 회전
            set_motor_velocity(DXL_ID, VELOCITY_CW)
        else:
            # 아무 키도 안 눌리면 정지
            set_motor_velocity(DXL_ID, VELOCITY_ZERO)
        
        time.sleep(0.1)  # CPU 과부하 방지를 위한 sleep

except KeyboardInterrupt:
    # 프로그램 종료 시 모터 정지 및 포트 닫기
    set_motor_velocity(DXL_ID, VELOCITY_ZERO)
    disable_torque(DXL_ID)
    portHandler.closePort()
    print("Program exited safely.")
