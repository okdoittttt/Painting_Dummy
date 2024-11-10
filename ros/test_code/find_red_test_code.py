import socket
import threading
from dynamixel_sdk import *  # Dynamixel SDK 라이브러리 사용


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
# Setup socket to receive signal
receiver_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
receiver_socket.bind(('localhost', 12345))

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


stop_signal_received = False

def listen_for_signal():
    global stop_signal_received
    while True:
        message, _ = receiver_socket.recvfrom(1024)
        message = message.decode()

        if "Red detected" in message:
            stop_signal_received = True
        else:
            stop_signal_received = False

def stop_motors():
    dxl_comm_result_13, dxl_error_13 = packetHandler.write4ByteTxRx(portHandler, moving_dx_id_11, ADDR_GOAL_VELOCITY, VELOCITY_STOP)
    if dxl_comm_result_13 != COMM_SUCCESS or dxl_error_13 != 0:
        print({"error": f"Motor 13 failed to move: {packetHandler.getTxRxResult(dxl_comm_result_13)}"})
    else:
        print("Motor 13 stopped successfully.")
        dxl_comm_result_13, dxl_error_13 = packetHandler.write4ByteTxRx(portHandler, moving_dx_id_12, ADDR_GOAL_VELOCITY, VELOCITY_STOP)
    if dxl_comm_result_13 != COMM_SUCCESS or dxl_error_13 != 0:
        print({"error": f"Motor 13 failed to move: {packetHandler.getTxRxResult(dxl_comm_result_13)}"})
    else:
        print("Motor 13 stopped successfully.")

        dxl_comm_result_13, dxl_error_13 = packetHandler.write4ByteTxRx(portHandler, moving_dx_id_13, ADDR_GOAL_VELOCITY, VELOCITY_STOP)
    if dxl_comm_result_13 != COMM_SUCCESS or dxl_error_13 != 0:
        print({"error": f"Motor 13 failed to move: {packetHandler.getTxRxResult(dxl_comm_result_13)}"})
    else:
        print("Motor 13 stopped successfully.")
    dxl_comm_result_13, dxl_error_13 = packetHandler.write4ByteTxRx(portHandler, moving_dx_id_14, ADDR_GOAL_VELOCITY, VELOCITY_STOP)
    if dxl_comm_result_13 != COMM_SUCCESS or dxl_error_13 != 0:
        print({"error": f"Motor 13 failed to move: {packetHandler.getTxRxResult(dxl_comm_result_13)}"})
    else:
        print("Motor 13 stopped successfully.")

def go_up():
    print("go up")
    # Control motor 13
    dxl_comm_result_13, dxl_error_13 = packetHandler.write4ByteTxRx(portHandler, moving_dx_id_13, ADDR_GOAL_VELOCITY, VELOCITY_CCW)
    if dxl_comm_result_13 != COMM_SUCCESS or dxl_error_13 != 0:
        return {"error": f"Motor 13 failed to move: {packetHandler.getTxRxResult(dxl_comm_result_13)}"}
            
    # Control motor 14
    dxl_comm_result_14, dxl_error_14 = packetHandler.write4ByteTxRx(portHandler, moving_dx_id_14, ADDR_GOAL_VELOCITY, VELOCITY_CW)
    if dxl_comm_result_14 != COMM_SUCCESS or dxl_error_14 != 0:
        return {"error": f"Motor 14 failed to move: {packetHandler.getTxRxResult(dxl_comm_result_14)}"}

    for _ in range (10):
        if stop_signal_received :
            stop_motors()
            print("stopped")
            return 
                
        time.sleep(0.1)

    # Control motor 13
    dxl_comm_result_13, dxl_error_13 = packetHandler.write4ByteTxRx(portHandler, moving_dx_id_13, ADDR_GOAL_VELOCITY, VELOCITY_STOP)
    if dxl_comm_result_13 != COMM_SUCCESS or dxl_error_13 != 0:
        return {"error": f"Motor 13 failed to move: {packetHandler.getTxRxResult(dxl_comm_result_13)}"}

    # Control motor 14
    dxl_comm_result_14, dxl_error_14 = packetHandler.write4ByteTxRx(portHandler, moving_dx_id_14, ADDR_GOAL_VELOCITY, VELOCITY_STOP)
    if dxl_comm_result_14 != COMM_SUCCESS or dxl_error_14 != 0:
        return {"error": f"Motor 14 failed to move: {packetHandler.getTxRxResult(dxl_comm_result_14)}"}

def go_down():
    # Control motor 13
    dxl_comm_result_13, dxl_error_13 = packetHandler.write4ByteTxRx(portHandler, moving_dx_id_13, ADDR_GOAL_VELOCITY, VELOCITY_CW)
    if dxl_comm_result_13 != COMM_SUCCESS or dxl_error_13 != 0:
        return {"error": f"Motor 13 failed to move: {packetHandler.getTxRxResult(dxl_comm_result_13)}"}

    # Control motor 14
    dxl_comm_result_14, dxl_error_14 = packetHandler.write4ByteTxRx(portHandler, moving_dx_id_14, ADDR_GOAL_VELOCITY, VELOCITY_CCW)
    if dxl_comm_result_14 != COMM_SUCCESS or dxl_error_14 != 0:
        return {"error": f"Motor 14 failed to move: {packetHandler.getTxRxResult(dxl_comm_result_14)}"}

    for _ in range (10):
        if stop_signal_received :
            stop_motors()
            print("stopped")
            return 
                
        time.sleep(0.1)

    # Control motor 13
    dxl_comm_result_13, dxl_error_13 = packetHandler.write4ByteTxRx(portHandler, moving_dx_id_13, ADDR_GOAL_VELOCITY, VELOCITY_STOP)
    if dxl_comm_result_13 != COMM_SUCCESS or dxl_error_13 != 0:
        return {"error": f"Motor 13 failed to move: {packetHandler.getTxRxResult(dxl_comm_result_13)}"}

    # Control motor 14
    dxl_comm_result_14, dxl_error_14 = packetHandler.write4ByteTxRx(portHandler, moving_dx_id_14, ADDR_GOAL_VELOCITY, VELOCITY_STOP)
    if dxl_comm_result_14 != COMM_SUCCESS or dxl_error_14 != 0:
        return {"error": f"Motor 14 failed to move: {packetHandler.getTxRxResult(dxl_comm_result_14)}"}

def go_left():
    # Control motor 13
    dxl_comm_result_13, dxl_error_13 = packetHandler.write4ByteTxRx(portHandler, moving_dx_id_11, ADDR_GOAL_VELOCITY, VELOCITY_CCW)
    if dxl_comm_result_13 != COMM_SUCCESS or dxl_error_13 != 0:
        return {"error": f"Motor 13 failed to move: {packetHandler.getTxRxResult(dxl_comm_result_13)}"}

    for _ in range (10):
        if stop_signal_received :
            stop_motors()
            print("stopped")
            return 
                
        time.sleep(0.1)

    # Control motor 13
    dxl_comm_result_13, dxl_error_13 = packetHandler.write4ByteTxRx(portHandler, moving_dx_id_11, ADDR_GOAL_VELOCITY, VELOCITY_STOP)
    if dxl_comm_result_13 != COMM_SUCCESS or dxl_error_13 != 0:
        return {"error": f"Motor 13 failed to move: {packetHandler.getTxRxResult(dxl_comm_result_13)}"}

def go_right():
    # Control motor 13
    dxl_comm_result_13, dxl_error_13 = packetHandler.write4ByteTxRx(portHandler, moving_dx_id_11, ADDR_GOAL_VELOCITY, VELOCITY_CW)
    if dxl_comm_result_13 != COMM_SUCCESS or dxl_error_13 != 0:
        return {"error": f"Motor 13 failed to move: {packetHandler.getTxRxResult(dxl_comm_result_13)}"}

    for _ in range (10):
        if stop_signal_received :
            stop_motors()
            print("stopped")
            return 
                
        time.sleep(0.1)

    # Control motor 13
    dxl_comm_result_13, dxl_error_13 = packetHandler.write4ByteTxRx(portHandler, moving_dx_id_11, ADDR_GOAL_VELOCITY, VELOCITY_STOP)
    if dxl_comm_result_13 != COMM_SUCCESS or dxl_error_13 != 0:
        return {"error": f"Motor 13 failed to move: {packetHandler.getTxRxResult(dxl_comm_result_13)}"}
    


def find_red():
    global stop_signal_received

    while True:
        go_up()
        if stop_signal_received :
            break
        go_left()
        if stop_signal_received :
            break
        go_down()
        if stop_signal_received :
            break
        go_right()
        if stop_signal_received :
            break

        time.sleep(1)
    

# Initialize the positions of the motors
initiallize_poze(12) # 2738 ~ 1358  
initiallize_poze(13) # 3766 ~ 2030 
initiallize_poze(14) #  3200 ~ 1716 
print(check_motor_position(12))
print(check_motor_position(13))
print(check_motor_position(14))

time.sleep(2)

signal_thread = threading.Thread(target=listen_for_signal, daemon=True)
signal_thread.start()

find_red()


