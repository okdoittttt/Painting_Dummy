from fastapi import FastAPI
from dynamixel_sdk import *  # Dynamixel SDK 라이브러리 사용

app = FastAPI()

# ********* DYNAMIXEL 모델 정의 *********
MY_DXL = 'X_SERIES'

ADDR_OPERATING_MODE = 11
ADDR_TORQUE_ENABLE = 64
ADDR_GOAL_VELOCITY = 104
ADDR_PRESENT_POSITION = 140  # 현재 위치 주소
BAUDRATE = 57600
PROTOCOL_VERSION = 2.0
DEVICENAME = '/dev/ttyUSB0'
TORQUE_ENABLE = 1
TORQUE_DISABLE = 0
VELOCITY_CW = 50
VELOCITY_CCW = -50
VELOCITY_STOP = 0

# Initialize Port and PacketHandler
portHandler = PortHandler(DEVICENAME)
packetHandler = PacketHandler(PROTOCOL_VERSION)

# Open Port
if not portHandler.openPort():
    raise Exception("Failed to open the port")

if not portHandler.setBaudRate(BAUDRATE):
    raise Exception("Failed to set the baudrate")

# Dynamixel IDs to control
moving_dx_id_11 = 11
moving_dx_id_12 = 12
moving_dx_id_13 = 13
moving_dx_id_14 = 14

# Reboot each Dynamixel
for dxl_id in range(11, 16):
    dxl_comm_result, dxl_error = packetHandler.reboot(portHandler, dxl_id)
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error))

    print("[ID:%03d] reboot Succeeded\n" % dxl_id)

# Set wheel mode and torque for each Dynamixel motor
for dxl_id in [10, 11, 12, 13, 14, 15]:
    packetHandler.write1ByteTxRx(portHandler, dxl_id, ADDR_OPERATING_MODE, 1)
    packetHandler.write1ByteTxRx(portHandler, dxl_id, ADDR_TORQUE_ENABLE, TORQUE_ENABLE)

def check_motor_position(moving_dx_id):
    dxl_present_position, dxl_comm_result, dxl_error = packetHandler.read4ByteTxRx(portHandler, moving_dx_id, 140)
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error))
    print(f"Current Position {moving_dx_id} : {dxl_present_position}.")
    return dxl_present_position

def initiallize_poze(dx_id):
    move_to_front = VELOCITY_CW
    move_to_back = VELOCITY_CCW

    ccw_move_check_limit_start = 2738
    ccw_move_check_limit_end = 1358
    front_move_end_limit = 4000
    back_move_end_limit = 10

    if (dx_id == 13) :
        ccw_move_check_limit_start = 3766
        ccw_move_check_limit_end = 2030
        front_move_end_limit = 5000
        back_move_end_limit = 1013
    elif (dx_id == 14) :
        ccw_move_check_limit_start = 3200
        ccw_move_check_limit_end = 1716
        front_move_end_limit = 4500
        back_move_end_limit = 500

    current_motor_position = check_motor_position(dx_id)
    if abs(ccw_move_check_limit_start - current_motor_position) < abs(ccw_move_check_limit_end - current_motor_position) or (dx_id ==13 and 0 <= current_motor_position < 1000):
        print("move ccw")

        while True :
            dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, dx_id, ADDR_GOAL_VELOCITY, move_to_front)
            if dxl_comm_result != COMM_SUCCESS:
                print(f"Failed to set velocity: {packetHandler.getTxRxResult(dxl_comm_result)}")
            elif dxl_error != 0:
                print(f"Error while setting velocity: {packetHandler.getRxPacketError(dxl_error)}")
            else :
                print(f"Moving {dx_id} CCW...")

            if check_motor_position(dx_id) >= front_move_end_limit or (dx_id ==13 and 1000 <= check_motor_position(dx_id) <= 1013) :
                dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, dx_id, ADDR_GOAL_VELOCITY, 0)
                if dxl_comm_result != COMM_SUCCESS:
                    print(f"Failed to set velocity: {packetHandler.getTxRxResult(dxl_comm_result)}")
                elif dxl_error != 0:
                    print(f"Error while setting velocity: {packetHandler.getRxPacketError(dxl_error)}")
                else :
                    print(f"STOP {dx_id} CCW!!")
                break

    else :
        print("move cw")
        while True :
            dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, dx_id, ADDR_GOAL_VELOCITY, move_to_back)
            if dxl_comm_result != COMM_SUCCESS:
                print(f"Failed to set velocity: {packetHandler.getTxRxResult(dxl_comm_result)}")
            elif dxl_error != 0:
                print(f"Error while setting velocity: {packetHandler.getRxPacketError(dxl_error)}")
            else :
                print(f"Moving {dx_id} CW...")

            if check_motor_position(dx_id) <= back_move_end_limit or (dx_id ==13 and 1000 <= check_motor_position(dx_id) <= 1013) :
                dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, dx_id, ADDR_GOAL_VELOCITY, 0)
                if dxl_comm_result != COMM_SUCCESS:
                    print(f"Failed to set velocity: {packetHandler.getTxRxResult(dxl_comm_result)}")
                elif dxl_error != 0:
                    print(f"Error while setting velocity: {packetHandler.getRxPacketError(dxl_error)}")
                else :
                    print(f"STOP {dx_id} CW!!")
                break

    print(check_motor_position(dx_id))


# Initialize the positions of the motors
initiallize_poze(12) # 2738 ~ 1358  
initiallize_poze(13) # 3766 ~ 2030 
initiallize_poze(14) #  3200 ~ 1716 
# print(check_motor_position(12))
# print(check_motor_position(13))
# print(check_motor_position(14))

# Move motors via FastAPI routes
@app.post("/move_motor/{motor_id}/{direction}")
def move_motor(motor_id: int, direction: str):
    if direction == 'cw':
        velocity = VELOCITY_CW
    elif direction == 'ccw':
        velocity = VELOCITY_CCW
    elif direction == 'stop':
        velocity = VELOCITY_STOP
    else:
        return {"error": "Invalid direction"}

    dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, motor_id, ADDR_GOAL_VELOCITY, velocity)
    if dxl_comm_result != COMM_SUCCESS:
        return {"error": packetHandler.getTxRxResult(dxl_comm_result)}
    elif dxl_error != 0:
        return {"error": packetHandler.getRxPacketError(dxl_error)}

    return {"message": f"Motor {motor_id} set to {direction}"}

# Updated route for moving dual motors using path parameters
@app.post("/move_dual_motors/{direction_12}/{direction_13}")
def move_dual_motors(direction_12: str, direction_13: str):
    if direction_12 == 'cw':
        vel_12 = VELOCITY_CW
    elif direction_12 == 'ccw':
        vel_12 = VELOCITY_CCW
    elif direction_12 == 'stop':
        vel_12 = VELOCITY_STOP
    else:
        return {"error": "Invalid direction for motor 12"}

    if direction_13 == 'cw':
        vel_13 = VELOCITY_CW
    elif direction_13 == 'ccw':
        vel_13 = VELOCITY_CCW
    elif direction_13 == 'stop':
        vel_13 = VELOCITY_STOP
    else:
        return {"error": "Invalid direction for motor 13"}

    # Control motor 12
    dxl_comm_result_12, dxl_error_12 = packetHandler.write4ByteTxRx(portHandler, moving_dx_id_12, ADDR_GOAL_VELOCITY, vel_12)
    if dxl_comm_result_12 != COMM_SUCCESS or dxl_error_12 != 0:
        return {"error": f"Motor 13 failed to move: {packetHandler.getTxRxResult(dxl_comm_result_12)}"}

    # Control motor 13
    dxl_comm_result_13, dxl_error_13 = packetHandler.write4ByteTxRx(portHandler, moving_dx_id_13, ADDR_GOAL_VELOCITY, vel_13)
    if dxl_comm_result_13 != COMM_SUCCESS or dxl_error_13 != 0:
        return {"error": f"Motor 14 failed to move: {packetHandler.getTxRxResult(dxl_comm_result_13)}"}

    return {"message": f"Motors 12 and 13 moved. 12 to {direction_12}, 13 to {direction_13}"}

@app.post("/move_height_motors/{direction_13}/{direction_14}")
def move_height_motors(direction_13: str, direction_14: str):
    if direction_13 == 'cw':
        vel_13 = VELOCITY_CW
    elif direction_13 == 'ccw':
        vel_13 = VELOCITY_CCW
    elif direction_13 == 'stop':
        vel_13 = VELOCITY_STOP
    else:
        return {"error": "Invalid direction for motor 12"}

    if direction_14 == 'cw':
        vel_14 = VELOCITY_CW
    elif direction_14 == 'ccw':
        vel_14 = VELOCITY_CCW
    elif direction_14 == 'stop':
        vel_14 = VELOCITY_STOP
    else:
        return {"error": "Invalid direction for motor 13"}

    # Control motor 13
    dxl_comm_result_13, dxl_error_13 = packetHandler.write4ByteTxRx(portHandler, moving_dx_id_13, ADDR_GOAL_VELOCITY, vel_13)
    if dxl_comm_result_13 != COMM_SUCCESS or dxl_error_13 != 0:
        return {"error": f"Motor 13 failed to move: {packetHandler.getTxRxResult(dxl_comm_result_13)}"}

    # Control motor 14
    dxl_comm_result_14, dxl_error_14 = packetHandler.write4ByteTxRx(portHandler, moving_dx_id_14, ADDR_GOAL_VELOCITY, vel_14)
    if dxl_comm_result_14 != COMM_SUCCESS or dxl_error_14 != 0:
        return {"error": f"Motor 14 failed to move: {packetHandler.getTxRxResult(dxl_comm_result_14)}"}

    return {"message": f"Motors 13 and 14 moved. 12 to {direction_13}, 13 to {direction_14}"}

# Disable motor torque on exit
@app.on_event("shutdown")
def shutdown():
    for dxl_id in [moving_dx_id_11, moving_dx_id_12, moving_dx_id_13, 14, 15]:
        packetHandler.write1ByteTxRx(portHandler, dxl_id, ADDR_TORQUE_ENABLE, TORQUE_DISABLE)
    portHandler.closePort()
