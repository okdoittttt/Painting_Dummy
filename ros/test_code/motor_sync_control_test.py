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
    ADDR_TORQUE_ENABLE = 64
    ADDR_GOAL_POSITION = 116
    ADDR_PRESENT_POSITION = 132
    DXL_MINIMUM_POSITION_VALUE = 0
    DXL_MAXIMUM_POSITION_VALUE = 4067
    BAUDRATE = 57600

PROTOCOL_VERSION = 2.0
DXL_ID = 15
DEVICENAME = '/dev/ttyUSB0'
TORQUE_ENABLE = 1
TORQUE_DISABLE = 0

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

for dxl_id in range(11, 13):
    dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, dxl_id, ADDR_TORQUE_ENABLE, TORQUE_ENABLE)
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error))
    else:
        print(f"Dynamixel has been successfully connected DXL_ID : {dxl_id}")


moving_11 = False
moving_dx_id_11 = 11
direction_11 = 1

moving_12 = False
moving_dx_id_12 = 12
direction_12 = 1

lock_11 = threading.Lock()
lock_12 = threading.Lock()

def move11():
    global moving_dx_id_11, direction_11, moving_dx_id_12, direction_12
    dxl_present_position_11, dxl_comm_result_11, dxl_error_11 = packetHandler.read4ByteTxRx(portHandler, moving_dx_id_11, ADDR_PRESENT_POSITION)
    if dxl_comm_result_11 != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result_11))
    elif dxl_error != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error_11))

    
    move_step_11 = dxl_present_position_11

    dxl_present_position_12, dxl_comm_result_12, dxl_error_12 = packetHandler.read4ByteTxRx(portHandler, moving_dx_id_12, ADDR_PRESENT_POSITION)
    if dxl_comm_result_12 != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result_12))
    elif dxl_error != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error_12))

    
    move_step_12 = dxl_present_position_12  

    # current_dxl_id = moving_dx_id_11
    while True:
        with lock_11:
            if moving_11:
                # if current_dxl_id != moving_dx_id_11 :
                #     dxl_present_position_11, dxl_comm_result_11, dxl_error_11 = packetHandler.read4ByteTxRx(portHandler, moving_dx_id_11, ADDR_PRESENT_POSITION)
                #     if dxl_comm_result_11 != COMM_SUCCESS:
                #         print("%s" % packetHandler.getTxRxResult(dxl_comm_result_11))
                #     elif dxl_error != 0:
                #         print("%s" % packetHandler.getRxPacketError(dxl_error_11))
                    
                # move_step = dxl_present_position_11
                    # current_dxl_id=moving_dx_id_11

                move_step_11 += 13 * direction_11
                move_step_12 += 13 * direction_12

                if move_step_11 >= 4067:
                    move_step_11 = 4067
                elif move_step_11 < 0 :
                    move_step_11 = 0

                if move_step_12 >= 4067:
                    move_step_12 = 4067
                elif move_step_12 < 0 :
                    move_step_12 = 0

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

                print(f"${move_step_11} / ${move_step_12}")

        time.sleep(0.01)

def move12():
    global moving_dx_id_12, direction_12
    dxl_present_position_12, dxl_comm_result_12, dxl_error_12 = packetHandler.read4ByteTxRx(portHandler, moving_dx_id_12, ADDR_PRESENT_POSITION)
    if dxl_comm_result_12 != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result_12))
    elif dxl_error != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error_12))

    
    move_step = dxl_present_position_12
    # current_dxl_id = moving_dx_id_12
    while True:
        with lock_12:
            if moving_12:
                # if current_dxl_id != moving_dx_id_12 :
                #     dxl_present_position, dxl_comm_result, dxl_error = packetHandler.read4ByteTxRx(portHandler, moving_dx_id_12, ADDR_PRESENT_POSITION)
                #     if dxl_comm_result != COMM_SUCCESS:
                #         print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
                #     elif dxl_error != 0:
                #         print("%s" % packetHandler.getRxPacketError(dxl_error))
                    
                # move_step = dxl_present_position
                    # current_dxl_id=moving_dx_id_12

                move_step += 13 * direction_12

                if move_step >= 4067:
                    move_step = 4067
                elif move_step < 0 :
                    move_step = 0

                dxl_comm_result_12, dxl_error_12 = packetHandler.write4ByteTxRx(portHandler, moving_dx_id_12, ADDR_GOAL_POSITION, move_step)
                print(move_step)
                if dxl_comm_result_12 != COMM_SUCCESS:
                    print("%s" % packetHandler.getTxRxResult(dxl_comm_result_12))
                elif dxl_error != 0:
                    print("%s" % packetHandler.getRxPacketError(dxl_error_12))
        time.sleep(0.01)

def main(stdscr):
    global moving_11, moving_12, direction_11, direction_12, moving_dx_id_11, moving_dx_id_12

    stdscr.nodelay(True)
    stdscr.clear()
    stdscr.addstr(0, 0, "Press and hold the 'q' key to increase and 'a' key to decrease. Release to stop.")
    stdscr.addstr(1, 0, "Press and hold the 'w' key to increase and 's' key to decrease. Release to stop.")

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

    count_thread_11 = threading.Thread(target=move11)
    count_thread_11.daemon = True
    count_thread_11.start()

    count_thread_12 = threading.Thread(target=move12)
    count_thread_12.daemon = True
    count_thread_12.start()
    
    while True:
        
        key = stdscr.getch()

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

        if key == 27:  # ESC key
            break

        time.sleep(0.1)

curses.wrapper(main)

for dxl_id in range(11, 13):
    dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, dxl_id, ADDR_TORQUE_ENABLE, TORQUE_DISABLE)
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error))

portHandler.closePort()
