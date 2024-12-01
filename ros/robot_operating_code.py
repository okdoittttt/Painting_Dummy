from fastapi import FastAPI
from dynamixel_sdk import *  # Dynamixel SDK 라이브러리 사용
from threading import Thread, Event
import re
import socket
import Jetson.GPIO as GPIO

app = FastAPI()

# 실행 상태를 제어하는 플래그
automove_running = False
automove_running_event = Event()
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

paint_pin = 7

# GPIO 채널 설정
GPIO.setmode(GPIO.BOARD) 
GPIO.setup(paint_pin, GPIO.OUT, initial=GPIO.LOW) 

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

stop_signal_received = False
stop_repaint_signal_received = True

center_x = center_y = 0
tl_x = tl_y = tr_x = tr_y =bl_x = bl_y =br_x =br_y = distance = 0
yel_tl_x = yel_tl_y = yel_tr_x = yel_tr_y = yel_bl_x = yel_bl_y = yel_br_x = yel_br_y = 0
repaint_coords = []

auto_move_left_right = 'right'
auto_move_up_down = 'down'
auto_destination = 3

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
    if br_x <= 320 and br_y <= 300 :
        return True
    return False


def check_if_end_corner_left() :
    global bl_x, bl_y
    if bl_x <= 320 and bl_y <= 300 :
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



def initialize_paint() :
    global paint_pin
    GPIO.output(paint_pin, GPIO.HIGH)
    time.sleep(3)
    GPIO.output(paint_pin, GPIO.LOW)


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


def find_area():
    global automove_running
    global stop_signal_received, distance
    # print('finding area...')
    while stop_signal_received == False:
        go_auto_back()
        if not automove_running :
            stop_motors()
            return 
        

def set_to_start_left_corner_center():
    global tl_x, tl_y
    global automove_running
    if tl_x > 320 :
        while tl_x > 320:
            go_left()
            if not automove_running :
                stop_motors()
                return 
        stop_motors()
    else :
        while tl_x < 320:
            go_right()
            if not automove_running :
                stop_motors()
                return 
        stop_motors()

    time.sleep(2)

    if tl_y > 240 :
        # print('going down...')
        while tl_y > 240:
            go_auto_down()
            look_auto_up()
            if not automove_running :
                stop_motors()
                return 
        stop_motors()
        go_auto_back()
        time.sleep(0.5)
        stop_motors()
    else :
        # print('going up...')
        while tl_y < 240:
            if not automove_running :
                stop_motors()
                return 
            go_auto_up()
            look_auto_down()
        stop_motors()
        go_auto_front()
        time.sleep(0.5)
        stop_motors()

def set_to_center():
    global center_x, center_y
    global automove_running
    if center_x > 320 :
        while center_x > 320:
            go_left()
            if not automove_running :
                stop_motors()
                return 
        stop_motors()
    else :
        while center_x < 320:
            go_right()
            if not automove_running :
                stop_motors()
                return 
        stop_motors()

    time.sleep(2)

    if center_y > 140 :
        # print('going down...')
        while center_y > 140:
            go_auto_down()
            look_auto_up()
            if not automove_running :
                stop_motors()
                return 
        stop_motors()
        go_auto_back()
        time.sleep(0.5)
        stop_motors()
    else :
        # print('going up...')
        while center_y < 140:
            go_auto_up()
            look_auto_down()
            if not automove_running :
                stop_motors()
                return 
        stop_motors()
        go_auto_front()
        time.sleep(0.5)
        stop_motors()

def go_to_left():
    global tr_x
    if tr_x > 320 :
        while tr_x > 320:
            go_auto_left()
            if not automove_running :
                stop_motors()
                return 
        stop_motors()
    else :
        while tr_x < 320:
            go_auto_right()
            if not automove_running :
                stop_motors()
                return 
        stop_motors()


def go_to_right():
    global tl_x
    if tl_x > 320 :
        while tl_x > 320:
            go_auto_left()
            if not automove_running :
                stop_motors()
                return 
        stop_motors()
    else :
        while tl_x < 320:
            go_auto_right()
            if not automove_running :
                stop_motors()
                return 
        stop_motors()


def auto_paint():
    global paint_pin
    while True :
        GPIO.output(paint_pin, GPIO.HIGH)
        go_to_left()

        if not automove_running :
            GPIO.output(paint_pin, GPIO.LOW)    
            stop_motors()
            return 
        
        GPIO.output(paint_pin, GPIO.LOW)
        stop_motors()
        
        # look_auto_down()
        # time.sleep(2)
        if not automove_running :
            GPIO.output(paint_pin, GPIO.LOW)    
            stop_motors()
            return 
        
        go_auto_down()
        time.sleep(1)
        stop_motors()
        
        if check_if_end_corner_left() :
            break
        

        GPIO.output(paint_pin, GPIO.HIGH)
        go_to_right()

        if not automove_running :
            GPIO.output(paint_pin, GPIO.LOW)    
            stop_motors()
            return 
    
        GPIO.output(paint_pin, GPIO.LOW)
        stop_motors()

        if not automove_running :
            GPIO.output(paint_pin, GPIO.LOW)    
            stop_motors()
            return 

        # look_auto_down()
        # time.sleep(2)
        go_auto_down()
        time.sleep(1)
        stop_motors()

        if check_if_end_corner_right() :
            break

def auto_repaint():
    global paint_pin
    while True :
        GPIO.output(paint_pin, GPIO.HIGH)
        go_to_left()

        if not automove_running :
            GPIO.output(paint_pin, GPIO.LOW)    
            stop_motors()
            return 

        GPIO.output(paint_pin, GPIO.LOW)
        stop_motors()
        

        if not automove_running :
            GPIO.output(paint_pin, GPIO.LOW)    
            stop_motors()
            return 


        # look_auto_down()
        # time.sleep(2)
        go_auto_down()
        time.sleep(1)
        stop_motors()
        
        if check_if_end_corner_left_repaint() :
            break

        GPIO.output(paint_pin, GPIO.HIGH)
        go_to_right()

        if not automove_running :
            GPIO.output(paint_pin, GPIO.LOW)    
            stop_motors()
            return 
        
        GPIO.output(paint_pin, GPIO.LOW)
        stop_motors()

        # look_auto_down()
        # time.sleep(2)
        go_auto_down()

        if not automove_running :
            GPIO.output(paint_pin, GPIO.LOW)    
            stop_motors()
            return 
    
        time.sleep(1)
        stop_motors()

        if check_if_end_corner_right_repaint() :
            break

def check_and_repaint() :
    global yel_tl_x, yel_tl_y
    if yel_tl_x > 320 :
        while yel_tl_x > 320:
            go_left()
            if not automove_running :
                stop_motors()
                return 
        stop_motors()
    else :
        while yel_tl_x < 320:
            go_right()
            if not automove_running :
                stop_motors()
                return 
        stop_motors()

    time.sleep(2)

    if yel_tl_y > 140 :
        # print('going down...')
        while yel_tl_y > 140:
            go_auto_down()
            look_auto_up()
            if not automove_running :
                stop_motors()
                return 
        stop_motors()
        go_auto_back()
        time.sleep(0.5)
        stop_motors()
    else :
        # print('going up...')
        while yel_tl_y < 140:
            go_auto_up()
            look_auto_down()
            if not automove_running :
                stop_motors()
                return 
        stop_motors()
        go_auto_front()
        time.sleep(0.5)
        stop_motors()
    
    auto_repaint()

################## API 영역 ####################3


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

@app.post("/paint/{switchStatus}")
def paintOnOff(switchStatus: str):
    global paint_pin
    if switchStatus == 'on' :
       GPIO.output(paint_pin, GPIO.HIGH)
    elif switchStatus == 'off' :
       GPIO.output(paint_pin, GPIO.LOW)
    else :
       return {"error": "Invalid operation"}

@app.post("/initialize")
def initialize_automove():
    global automove_running
    global automove_running_event

    # 이미 실행 중이면 실행 중단
    if automove_running_event.is_set():
        automove_running = False
        automove_running_event.clear()  # 실행 중단 플래그 비활성화
        return {"message": "Automove stopped"}
    
    automove_running_event.set()  # 실행 플래그 활성화
    automove_thread = Thread(target=automove, daemon=True)
    automove_thread.start()
    return {"message": "Automove started"}
    
def automove():
    global automove_running
    global automove_running_event
    automove_running = True
    # 작업 시작
    initialize_paint()
    time.sleep(2)

    if not automove_running:
        return {"message": "Auto Stopped"}

    # 신호 수신 스레드 시작
    signal_thread = Thread(target=listen_for_signal, daemon=True)
    signal_thread.start()

    # 영역 찾기
    if automove_running:
        print('find_area')
        find_area()
    time.sleep(1)

    if not automove_running:
        return {"message": "Auto Stopped"}
    time.sleep(2)
    
    print(automove_running)

    # 시작 코너로 이동
    if automove_running:
        print('set to start left corner center')
        set_to_start_left_corner_center()

    print(automove_running)

    if not automove_running:
        return {"message": "Auto Stopped"}
    time.sleep(2)

    print(automove_running)


    # 페인팅 시작
    if automove_running:
        print('auto paint')
        auto_paint()

    print(automove_running)

    if not automove_running:
        return {"message": "Auto Stopped"}

    print(automove_running)

    time.sleep(2)

    # 리페인팅 처리
    if automove_running:
        print('check and repaint')
        set_to_center()
        check_and_repaint()

    print(automove_running)
    
    if not automove_running:
        return {"message": "Auto Stopped"}

    print(automove_running)
    # 작업 종료 시 플래그 해제
    automove_running = False

    return {"message": "Auto Finished"}

# Disable motor torque on exit
@app.on_event("shutdown")
def shutdown():
    for dxl_id in [moving_dx_id_11, moving_dx_id_12, moving_dx_id_13, 14, 15]:
        packetHandler.write1ByteTxRx(portHandler, dxl_id, ADDR_TORQUE_ENABLE, TORQUE_DISABLE)
    portHandler.closePort()
