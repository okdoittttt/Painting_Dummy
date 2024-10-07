from fastapi import FastAPI
import time
from dynamixel_sdk import *  # Dynamixel SDK 라이브러리 사용

app = FastAPI()

# ********* DYNAMIXEL 모델 정의 *********
MY_DXL = 'X_SERIES'

ADDR_OPERATING_MODE = 11
ADDR_TORQUE_ENABLE = 64
ADDR_GOAL_VELOCITY = 104
ADDR_PRESENT_POSITION = 132  # 현재 위치 주소
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

for dxl_id in range(11,16):
    dxl_comm_result, dxl_error = packetHandler.reboot(portHandler, dxl_id)
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error))

    print("[ID:%03d] reboot Succeeded\n" % dxl_id)



# Set wheel mode and torque for each Dynamixel motor
for dxl_id in [10, 11, 12, 13, 14,15]:
    packetHandler.write1ByteTxRx(portHandler, dxl_id, ADDR_OPERATING_MODE, 1)
    packetHandler.write1ByteTxRx(portHandler, dxl_id, ADDR_TORQUE_ENABLE, TORQUE_ENABLE)

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
            
    
initiallize_poze(12)
initiallize_poze(11)
initiallize_poze(13)

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

@app.post("/move_dual_motors?direction_12={direction_12}&direction_13={direction_13}")
def move_dual_motors(direction_12: str, direction_13: str):
    if direction_12 == 'cw':
        vel_12 = VELOCITY_CW
    elif direction_12 == 'ccw':
        vel_12 = VELOCITY_CCW
    elif direction_12 == 'stop':
        vel_12 = VELOCITY_STOP
    else :
        return {"error": "Invalid direction"}

    if direction_13 == 'cw':
        vel_13 = VELOCITY_CW
    elif direction_13 == 'ccw':
        vel_13 = VELOCITY_CCW
    elif direction_13 == 'stop':
        vel_13 = VELOCITY_STOP
    else :
        return {"error": "Invalid direction"}

    # Control motor 12
    packetHandler.write4ByteTxRx(portHandler, moving_dx_id_12, ADDR_GOAL_VELOCITY, vel_12)
    # Control motor 13
    packetHandler.write4ByteTxRx(portHandler, moving_dx_id_13, ADDR_GOAL_VELOCITY, vel_13)

    return {"message": f"Motors 12 and 13 moved. 12 to {direction_12}, 13 to {direction_13}"}

# Disable motor torque on exit
@app.on_event("shutdown")
def shutdown():
    for dxl_id in [moving_dx_id_11, moving_dx_id_12, moving_dx_id_13, 14, 15]:
        packetHandler.write1ByteTxRx(portHandler, dxl_id, ADDR_TORQUE_ENABLE, TORQUE_DISABLE)
    portHandler.closePort()
