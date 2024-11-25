import socket
import threading
import re
from dynamixel_sdk import *  # Dynamixel SDK 라이브러리 사용
import Jetson.GPIO as GPIO



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

AUTO_VELOCITY_CW = 5
AUTO_VELOCITY_CCW = -5

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
        # print("move ccw")

        while True :
            dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, dx_id, ADDR_GOAL_VELOCITY, move_to_front)
            if dxl_comm_result != COMM_SUCCESS:
                print(f"Failed to set velocity: {packetHandler.getTxRxResult(dxl_comm_result)}")
            elif dxl_error != 0:
                print(f"Error while setting velocity: {packetHandler.getRxPacketError(dxl_error)}")
            # else :
            #     print(f"Moving {dx_id} CCW...")

            if check_motor_position(dx_id) >= front_move_end_limit or (dx_id ==13 and 1000 <= check_motor_position(dx_id) <= 1013) :
                dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, dx_id, ADDR_GOAL_VELOCITY, 0)
                if dxl_comm_result != COMM_SUCCESS:
                    print(f"Failed to set velocity: {packetHandler.getTxRxResult(dxl_comm_result)}")
                elif dxl_error != 0:
                    print(f"Error while setting velocity: {packetHandler.getRxPacketError(dxl_error)}")
                # else :
                #     print(f"STOP {dx_id} CCW!!")
                break

    else :
        # print("move cw")
        while True :
            dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, dx_id, ADDR_GOAL_VELOCITY, move_to_back)
            if dxl_comm_result != COMM_SUCCESS:
                print(f"Failed to set velocity: {packetHandler.getTxRxResult(dxl_comm_result)}")
            elif dxl_error != 0:
                print(f"Error while setting velocity: {packetHandler.getRxPacketError(dxl_error)}")
            # else :
            #     # print(f"Moving {dx_id} CW...")

            if check_motor_position(dx_id) <= back_move_end_limit or (dx_id ==13 and 1000 <= check_motor_position(dx_id) <= 1013) :
                dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, dx_id, ADDR_GOAL_VELOCITY, 0)
                if dxl_comm_result != COMM_SUCCESS:
                    print(f"Failed to set velocity: {packetHandler.getTxRxResult(dxl_comm_result)}")
                elif dxl_error != 0:
                    print(f"Error while setting velocity: {packetHandler.getRxPacketError(dxl_error)}")
                # else :
                #     # print(f"STOP {dx_id} CW!!")
                break

    # print(check_motor_position(dx_id))


stop_signal_received = False
stop_repaint_signal_received = True

center_x = center_y = 0
tl_x = tl_y = tr_x = tr_y =bl_x = bl_y =br_x =br_y = distance = 0
yel_tl_x = yel_tl_y = yel_tr_x = yel_tr_y = yel_bl_x = yel_bl_y = yel_br_x = yel_br_y = 0
repaint_coords = []

auto_move_left_right = 'right'
auto_move_up_down = 'down'
auto_destination = 3

def listen_for_signal():
    global stop_signal_received, stop_repaint_signal_received
    global center_x, center_y
    global tl_x, tl_y, tr_x, tr_y, bl_x, bl_y, br_x, br_y, distance
    global yel_tl_x, yel_tl_y, yel_tr_x, yel_tr_y, yel_bl_x, yel_bl_y, yel_br_x, yel_br_y
    global repaint_coords

    while True:
        message, _ = receiver_socket.recvfrom(1024)
        message = message.decode()

        if "Black" in message :
            coordinates = re.findall(r'TL\((\d+), (\d+)\), TR\((\d+), (\d+)\), BL\((\d+), (\d+)\), BR\((\d+), (\d+)\), Distance: (\d+) cm', message)
            center_coord = re.findall(r'Black Center: \((\d+), (\d+)\)', message)
            # 결과를 정수로 변환하여 각각의 변수에 담기
            if coordinates:
                tl_x, tl_y, tr_x, tr_y, bl_x, bl_y, br_x, br_y, distance = map(int, coordinates[0])
                center_x, center_y = map(int, center_coord[0])
                # 결과 출력
                # print("TL x:", tl_x, "y:", tl_y)
                # print("TR x:", tr_x, "y:", tr_y)
                # print("BL x:", bl_x, "y:", bl_y)
                # print("BR x:", br_x, "y:", br_y)
            # else:
            #     # print("Coordinates not found in the message.")
            # print(f'Center : {center_x} / {center_y}')
            stop_signal_received = True
        elif "Yellow" in message :
            coordinates = re.findall(r'TL\((\d+), (\d+)\), TR\((\d+), (\d+)\), BL\((\d+), (\d+)\), BR\((\d+), (\d+)\)', message)
            if coordinates:
                yel_tl_x, yel_tl_y, yel_tr_x, yel_tr_y, yel_bl_x, yel_bl_y, yel_br_x, yel_br_y = map(int, coordinates[0])
            
            stop_signal_received = True
        else:
            stop_signal_received = False
            stop_repaint_signal_received = False

def reboot():
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

def stop_motors():
    dxl_comm_result_13, dxl_error_13 = packetHandler.write4ByteTxRx(portHandler, moving_dx_id_11, ADDR_GOAL_VELOCITY, VELOCITY_STOP)
    if dxl_comm_result_13 != COMM_SUCCESS or dxl_error_13 != 0:
        print({"error": f"Motor 13 failed to move: {packetHandler.getTxRxResult(dxl_comm_result_13)}"})
    else:
        # print("Motor 13 stopped successfully.")
        dxl_comm_result_13, dxl_error_13 = packetHandler.write4ByteTxRx(portHandler, moving_dx_id_12, ADDR_GOAL_VELOCITY, VELOCITY_STOP)
    if dxl_comm_result_13 != COMM_SUCCESS or dxl_error_13 != 0:
        print({"error": f"Motor 13 failed to move: {packetHandler.getTxRxResult(dxl_comm_result_13)}"})
    else:
        # print("Motor 13 stopped successfully.")

        dxl_comm_result_13, dxl_error_13 = packetHandler.write4ByteTxRx(portHandler, moving_dx_id_13, ADDR_GOAL_VELOCITY, VELOCITY_STOP)
    if dxl_comm_result_13 != COMM_SUCCESS or dxl_error_13 != 0:
        print({"error": f"Motor 13 failed to move: {packetHandler.getTxRxResult(dxl_comm_result_13)}"})
    else:
        # print("Motor 13 stopped successfully.")
        dxl_comm_result_14, dxl_error_14 = packetHandler.write4ByteTxRx(portHandler, moving_dx_id_14, ADDR_GOAL_VELOCITY, VELOCITY_STOP)
    if dxl_comm_result_14 != COMM_SUCCESS or dxl_error_14 != 0:
        print({"error": f"Motor 13 failed to move: {packetHandler.getTxRxResult(dxl_comm_result_13)}"})
    # else:
    #     # print("Motor 13 stopped successfully.")

def go_up():
    # print("go up")
    # Control motor 13
    dxl_comm_result_13, dxl_error_13 = packetHandler.write4ByteTxRx(portHandler, moving_dx_id_13, ADDR_GOAL_VELOCITY, VELOCITY_CCW)
    if dxl_comm_result_13 != COMM_SUCCESS or dxl_error_13 != 0:
        # reboot()
        return {"error": f"Motor 13 failed to move: {packetHandler.getTxRxResult(dxl_comm_result_13)}"}
            
    # Control motor 14
    dxl_comm_result_14, dxl_error_14 = packetHandler.write4ByteTxRx(portHandler, moving_dx_id_14, ADDR_GOAL_VELOCITY, VELOCITY_CW)
    if dxl_comm_result_14 != COMM_SUCCESS or dxl_error_14 != 0:
        # reboot()
        return {"error": f"Motor 14 failed to move: {packetHandler.getTxRxResult(dxl_comm_result_14)}"}

    for _ in range (10):
        if stop_signal_received :
            stop_motors()
            # print("stopped")
            return 
                
        time.sleep(0.1)

    # Control motor 13
    dxl_comm_result_13, dxl_error_13 = packetHandler.write4ByteTxRx(portHandler, moving_dx_id_13, ADDR_GOAL_VELOCITY, VELOCITY_STOP)
    if dxl_comm_result_13 != COMM_SUCCESS or dxl_error_13 != 0:
        # reboot()
        return {"error": f"Motor 13 failed to move: {packetHandler.getTxRxResult(dxl_comm_result_13)}"}

    # Control motor 14
    dxl_comm_result_14, dxl_error_14 = packetHandler.write4ByteTxRx(portHandler, moving_dx_id_14, ADDR_GOAL_VELOCITY, VELOCITY_STOP)
    if dxl_comm_result_14 != COMM_SUCCESS or dxl_error_14 != 0:
        # reboot()
        return {"error": f"Motor 14 failed to move: {packetHandler.getTxRxResult(dxl_comm_result_14)}"}

def go_down():
    # Control motor 13
    dxl_comm_result_13, dxl_error_13 = packetHandler.write4ByteTxRx(portHandler, moving_dx_id_13, ADDR_GOAL_VELOCITY, VELOCITY_CW)
    if dxl_comm_result_13 != COMM_SUCCESS or dxl_error_13 != 0:
        # reboot()
        return {"error": f"Motor 13 failed to move: {packetHandler.getTxRxResult(dxl_comm_result_13)}"}

    # Control motor 14
    dxl_comm_result_14, dxl_error_14 = packetHandler.write4ByteTxRx(portHandler, moving_dx_id_14, ADDR_GOAL_VELOCITY, VELOCITY_CCW)
    if dxl_comm_result_14 != COMM_SUCCESS or dxl_error_14 != 0:
        # reboot()
        return {"error": f"Motor 14 failed to move: {packetHandler.getTxRxResult(dxl_comm_result_14)}"}

    for _ in range (10):
        if stop_signal_received :
            stop_motors()
            # print("stopped")
            return 
                
        time.sleep(0.1)

    # Control motor 13
    dxl_comm_result_13, dxl_error_13 = packetHandler.write4ByteTxRx(portHandler, moving_dx_id_13, ADDR_GOAL_VELOCITY, VELOCITY_STOP)
    if dxl_comm_result_13 != COMM_SUCCESS or dxl_error_13 != 0:
        # reboot()
        return {"error": f"Motor 13 failed to move: {packetHandler.getTxRxResult(dxl_comm_result_13)}"}

    # Control motor 14
    dxl_comm_result_14, dxl_error_14 = packetHandler.write4ByteTxRx(portHandler, moving_dx_id_14, ADDR_GOAL_VELOCITY, VELOCITY_STOP)
    if dxl_comm_result_14 != COMM_SUCCESS or dxl_error_14 != 0:
        # reboot()
        return {"error": f"Motor 14 failed to move: {packetHandler.getTxRxResult(dxl_comm_result_14)}"}

def go_left():
    # Control motor 13
    dxl_comm_result_13, dxl_error_13 = packetHandler.write4ByteTxRx(portHandler, moving_dx_id_11, ADDR_GOAL_VELOCITY, VELOCITY_CCW)
    if dxl_comm_result_13 != COMM_SUCCESS or dxl_error_13 != 0:
        # reboot()
        return {"error": f"Motor 13 failed to move: {packetHandler.getTxRxResult(dxl_comm_result_13)}"}

    for _ in range (5):
        if stop_signal_received :
            stop_motors()
            # print("stopped")
            return 
                
        time.sleep(0.1)

    # Control motor 13
    dxl_comm_result_13, dxl_error_13 = packetHandler.write4ByteTxRx(portHandler, moving_dx_id_11, ADDR_GOAL_VELOCITY, VELOCITY_STOP)
    if dxl_comm_result_13 != COMM_SUCCESS or dxl_error_13 != 0:
        # reboot()
        return {"error": f"Motor 13 failed to move: {packetHandler.getTxRxResult(dxl_comm_result_13)}"}

def go_right():
    # Control motor 13
    dxl_comm_result_13, dxl_error_13 = packetHandler.write4ByteTxRx(portHandler, moving_dx_id_11, ADDR_GOAL_VELOCITY, VELOCITY_CW)
    if dxl_comm_result_13 != COMM_SUCCESS or dxl_error_13 != 0:
        # reboot()
        return {"error": f"Motor 13 failed to move: {packetHandler.getTxRxResult(dxl_comm_result_13)}"}

    for _ in range (5):
        if stop_signal_received :
            stop_motors()
            # print("stopped")
            return 
                
        time.sleep(0.1)

    # Control motor 13
    dxl_comm_result_13, dxl_error_13 = packetHandler.write4ByteTxRx(portHandler, moving_dx_id_11, ADDR_GOAL_VELOCITY, VELOCITY_STOP)
    if dxl_comm_result_13 != COMM_SUCCESS or dxl_error_13 != 0:
        # reboot()
        return {"error": f"Motor 13 failed to move: {packetHandler.getTxRxResult(dxl_comm_result_13)}"}
    

def go_auto_up():
    # Control motor 13
    dxl_comm_result_13, dxl_error_13 = packetHandler.write4ByteTxRx(portHandler, moving_dx_id_12, ADDR_GOAL_VELOCITY, AUTO_VELOCITY_CCW)
    if dxl_comm_result_13 != COMM_SUCCESS or dxl_error_13 != 0:
        # reboot()
        return {"error": f"Motor 13 failed to move: {packetHandler.getTxRxResult(dxl_comm_result_13)}"}
            
    # Control motor 14
    dxl_comm_result_14, dxl_error_14 = packetHandler.write4ByteTxRx(portHandler, moving_dx_id_14, ADDR_GOAL_VELOCITY, AUTO_VELOCITY_CW)
    if dxl_comm_result_14 != COMM_SUCCESS or dxl_error_14 != 0:
        # reboot()
        return {"error": f"Motor 14 failed to move: {packetHandler.getTxRxResult(dxl_comm_result_14)}"}

def go_auto_down():
    # Control motor 13
    dxl_comm_result_13, dxl_error_13 = packetHandler.write4ByteTxRx(portHandler, moving_dx_id_12, ADDR_GOAL_VELOCITY, AUTO_VELOCITY_CW)
    if dxl_comm_result_13 != COMM_SUCCESS or dxl_error_13 != 0:
        # reboot()
        return {"error": f"Motor 13 failed to move: {packetHandler.getTxRxResult(dxl_comm_result_13)}"}

    # Control motor 14
    dxl_comm_result_14, dxl_error_14 = packetHandler.write4ByteTxRx(portHandler, moving_dx_id_14, ADDR_GOAL_VELOCITY, AUTO_VELOCITY_CCW)
    if dxl_comm_result_14 != COMM_SUCCESS or dxl_error_14 != 0:
        # reboot()
        return {"error": f"Motor 14 failed to move: {packetHandler.getTxRxResult(dxl_comm_result_14)}"}

    
def go_auto_front():
    # Control motor 13
    dxl_comm_result_13, dxl_error_13 = packetHandler.write4ByteTxRx(portHandler, moving_dx_id_12, ADDR_GOAL_VELOCITY, AUTO_VELOCITY_CW)
    if dxl_comm_result_13 != COMM_SUCCESS or dxl_error_13 != 0:
        # reboot()
        return {"error": f"Motor 13 failed to move: {packetHandler.getTxRxResult(dxl_comm_result_13)}"}

    # Control motor 14
    dxl_comm_result_14, dxl_error_14 = packetHandler.write4ByteTxRx(portHandler, moving_dx_id_13, ADDR_GOAL_VELOCITY, AUTO_VELOCITY_CCW)
    if dxl_comm_result_14 != COMM_SUCCESS or dxl_error_14 != 0:
        # reboot()
        return {"error": f"Motor 14 failed to move: {packetHandler.getTxRxResult(dxl_comm_result_14)}"}


def go_auto_back():
    # Control motor 13
    dxl_comm_result_13, dxl_error_13 = packetHandler.write4ByteTxRx(portHandler, moving_dx_id_12, ADDR_GOAL_VELOCITY, AUTO_VELOCITY_CCW)
    if dxl_comm_result_13 != COMM_SUCCESS or dxl_error_13 != 0:
        # reboot()
        return {"error": f"Motor 13 failed to move: {packetHandler.getTxRxResult(dxl_comm_result_13)}"}

    # Control motor 14
    dxl_comm_result_14, dxl_error_14 = packetHandler.write4ByteTxRx(portHandler, moving_dx_id_13, ADDR_GOAL_VELOCITY, AUTO_VELOCITY_CW)
    if dxl_comm_result_14 != COMM_SUCCESS or dxl_error_14 != 0:
        # reboot()
        return {"error": f"Motor 14 failed to move: {packetHandler.getTxRxResult(dxl_comm_result_14)}"}

def look_auto_up():
    # Control motor 14
    dxl_comm_result_14, dxl_error_14 = packetHandler.write4ByteTxRx(portHandler, moving_dx_id_14, ADDR_GOAL_VELOCITY, AUTO_VELOCITY_CCW)
    if dxl_comm_result_14 != COMM_SUCCESS or dxl_error_14 != 0:
        # reboot()
        return {"error": f"Motor 14 failed to move: {packetHandler.getTxRxResult(dxl_comm_result_14)}"}
    
def look_auto_down():
    # Control motor 14
    dxl_comm_result_14, dxl_error_14 = packetHandler.write4ByteTxRx(portHandler, moving_dx_id_14, ADDR_GOAL_VELOCITY, AUTO_VELOCITY_CW)
    if dxl_comm_result_14 != COMM_SUCCESS or dxl_error_14 != 0:
        # reboot()
        return {"error": f"Motor 14 failed to move: {packetHandler.getTxRxResult(dxl_comm_result_14)}"}

def go_auto_left():
    # Control motor 13
    dxl_comm_result_13, dxl_error_13 = packetHandler.write4ByteTxRx(portHandler, moving_dx_id_11, ADDR_GOAL_VELOCITY, AUTO_VELOCITY_CCW)
    if dxl_comm_result_13 != COMM_SUCCESS or dxl_error_13 != 0:
        # reboot()
        return {"error": f"Motor 13 failed to move: {packetHandler.getTxRxResult(dxl_comm_result_13)}"}

def go_auto_right():
    # Control motor 13
    dxl_comm_result_13, dxl_error_13 = packetHandler.write4ByteTxRx(portHandler, moving_dx_id_11, ADDR_GOAL_VELOCITY, AUTO_VELOCITY_CW)
    if dxl_comm_result_13 != COMM_SUCCESS or dxl_error_13 != 0:
        # reboot()
        return {"error": f"Motor 13 failed to move: {packetHandler.getTxRxResult(dxl_comm_result_13)}"}

    
def check_if_end_corner_right() :
    global br_x, br_y
    if br_x <= 320 and br_y <= 250 :
        return True
    return False


def check_if_end_corner_left() :
    global bl_x, bl_y
    if bl_x <= 320 and bl_y <= 250 :
        return True
    return False

def check_if_end_corner_left_repaint() :
    global yel_bl_x, yel_bl_y
    if yel_bl_x <= 320 and yel_bl_y <= 250:
        return True
    return False

def check_if_end_corner_right_repaint() :
    global yel_br_x, yel_br_y
    if yel_br_x <= 320 and yel_br_y <= 250:
        return True
    return False


def find_area():
    global stop_signal_received, distance
    # print('finding area...')
    while stop_signal_received == False:
        go_auto_back()
        # print(stop_signal_received, distance)
        

def set_to_start_left_corner_center():
    global tl_x, tl_y
    if tl_x > 320 :
        while tl_x > 320:
            go_left()
        stop_motors()
    else :
        while tl_x < 320:
            go_right()
        stop_motors()

    time.sleep(2)

    if tl_y > 140 :
        # print('going down...')
        while tl_y > 140:
            go_auto_down()
            look_auto_up()
        stop_motors()
        go_auto_back()
        time.sleep(0.5)
        stop_motors()
    else :
        # print('going up...')
        while tl_y < 140:
            go_auto_up()
            look_auto_down()
        stop_motors()
        go_auto_front()
        time.sleep(0.5)
        stop_motors()

def set_to_center():
    global center_x, center_y
    if center_x > 320 :
        while center_x > 320:
            go_left()
        stop_motors()
    else :
        while center_x < 320:
            go_right()
        stop_motors()

    time.sleep(2)

    if center_y > 140 :
        # print('going down...')
        while center_y > 140:
            go_auto_down()
            look_auto_up()
        stop_motors()
        go_auto_back()
        time.sleep(0.5)
        stop_motors()
    else :
        # print('going up...')
        while center_y < 140:
            go_auto_up()
            look_auto_down()
        stop_motors()
        go_auto_front()
        time.sleep(0.5)
        stop_motors()

def go_to_left():
    global tr_x
    if tr_x > 320 :
        while tr_x > 320:
            go_auto_left()
        stop_motors()
    else :
        while tr_x < 320:
            go_auto_right()
        stop_motors()


def go_to_right():
    global tl_x
    if tl_x > 320 :
        while tl_x > 320:
            go_auto_left()
        stop_motors()
    else :
        while tl_x < 320:
            go_auto_right()
        stop_motors()



# LED 사용할 핀 정의
led_pin = 7
 
# GPIO 채널 설정
GPIO.setmode(GPIO.BOARD) 
GPIO.setup(led_pin, GPIO.OUT, initial=GPIO.LOW) 

def auto_paint():
    while True :
        GPIO.output(led_pin, GPIO.HIGH)
        go_to_left()
        GPIO.output(led_pin, GPIO.LOW)
        stop_motors()
        
        # look_auto_down()
        # time.sleep(2)
        go_auto_down()
        time.sleep(1)
        stop_motors()
        
        if check_if_end_corner_left() :
            break

        GPIO.output(led_pin, GPIO.HIGH)
        go_to_right()
        GPIO.output(led_pin, GPIO.LOW)
        stop_motors()

        # look_auto_down()
        # time.sleep(2)
        go_auto_down()
        time.sleep(1)
        stop_motors()

        if check_if_end_corner_right() :
            break

def auto_repaint():
    while True :
        GPIO.output(led_pin, GPIO.HIGH)
        go_to_left()
        GPIO.output(led_pin, GPIO.LOW)
        stop_motors()
        
        # look_auto_down()
        # time.sleep(2)
        go_auto_down()
        time.sleep(1)
        stop_motors()
        
        if check_if_end_corner_left_repaint() :
            break

        GPIO.output(led_pin, GPIO.HIGH)
        go_to_right()
        GPIO.output(led_pin, GPIO.LOW)
        stop_motors()

        # look_auto_down()
        # time.sleep(2)
        go_auto_down()
        time.sleep(1)
        stop_motors()

        if check_if_end_corner_right_repaint() :
            break

def check_and_repaint() :
    global yel_tl_x, yel_tl_y
    if yel_tl_x > 320 :
        while yel_tl_x > 320:
            go_left()
        stop_motors()
    else :
        while yel_tl_x < 320:
            go_right()
        stop_motors()

    time.sleep(2)

    if yel_tl_y > 140 :
        # print('going down...')
        while yel_tl_y > 140:
            go_auto_down()
            look_auto_up()
        stop_motors()
        go_auto_back()
        time.sleep(0.5)
        stop_motors()
    else :
        # print('going up...')
        while yel_tl_y < 140:
            go_auto_up()
            look_auto_down()
        stop_motors()
        go_auto_front()
        time.sleep(0.5)
        stop_motors()
    
    auto_repaint()

def go_to_left():
    global tr_x
    if tr_x > 320 :
        while tr_x > 320:
            go_auto_left()
        stop_motors()
    else :
        while tr_x < 320:
            go_auto_right()
        stop_motors()


def go_to_right():
    global tl_x
    if tl_x > 320 :
        while tl_x > 320:
            go_auto_left()
        stop_motors()
    else :
        while tl_x < 320:
            go_auto_right()
        stop_motors()

def initialize_paint() :
    GPIO.output(led_pin, GPIO.HIGH)
    time.sleep(5)
    GPIO.output(led_pin, GPIO.LOW)

# Initialize the positions of the motors
initiallize_poze(12) # 2738 ~ 1358a
initiallize_poze(13) # 3766 ~ 2030 
initiallize_poze(14) #  3200 ~ 1716 
# print(check_motor_position(12))
# print(check_motor_position(13))
# print(check_motor_position(14))

initialize_paint()

time.sleep(2)

signal_thread = threading.Thread(target=listen_for_signal, daemon=True)
signal_thread.start()

print("finding area")
find_area()
time.sleep(2)
print("setting corner center")
set_to_start_left_corner_center()
time.sleep(2)
auto_paint()
print("check and repainting")
while stop_repaint_signal_received :
    print('repaint')
    set_to_center()
    check_and_repaint()

if signal_thread.is_alive :
    signal_thread.join()