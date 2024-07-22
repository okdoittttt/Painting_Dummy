#!/usr/bin/env python
# -*- coding: utf-8 -*-

#*******************************************************************************
# Copyright 2017 ROBOTIS CO., LTD.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#*******************************************************************************


#*******************************************************************************
#***********************     Read and Write Example      ***********************
#  Required Environment to run this example :
#    - Protocol 2.0 supported DYNAMIXEL(X, P, PRO/PRO(A), MX 2.0 series)
#    - DYNAMIXEL Starter Set (U2D2, U2D2 PHB, 12V SMPS)
#  How to use the example :
#    - Select the DYNAMIXEL in use at the MY_DXL in the example code. 
#    - Build and Run from proper architecture subdirectory.
#    - For ARM based SBCs such as Raspberry Pi, use linux_sbc subdirectory to build and run.
#    - https://emanual.robotis.com/docs/en/software/dynamixel/dynamixel_sdk/overview/
#  Author: Ryu Woon Jung (Leon)
#  Maintainer : Zerom, Will Son
# *******************************************************************************

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
    DXL_MAXIMUM_POSITION_VALUE = 4095
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

for dxl_id in range(11, 16):
    dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, dxl_id, ADDR_TORQUE_ENABLE, TORQUE_ENABLE)
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error))
    else:
        print(f"Dynamixel has been successfully connected DXL_ID : {dxl_id}")

# dxl_present_position, dxl_comm_result, dxl_error = packetHandler.read4ByteTxRx(portHandler, 14, ADDR_PRESENT_POSITION)
# if dxl_comm_result != COMM_SUCCESS:
#     print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
# elif dxl_error != 0:
#     print("%s" % packetHandler.getRxPacketError(dxl_error))

# move_step = dxl_present_position
moving = False
moving_dx_id = 11
direction = 1
lock = threading.Lock()

def move():
    global moving_dx_id
    dxl_present_position, dxl_comm_result, dxl_error = packetHandler.read4ByteTxRx(portHandler, moving_dx_id, ADDR_PRESENT_POSITION)
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error))

    move_step = dxl_present_position
    while True:
        with lock:
            if moving:
                move_step += 13 * direction
                dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, moving_dx_id, ADDR_GOAL_POSITION, move_step)
                if dxl_comm_result != COMM_SUCCESS:
                    print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
                elif dxl_error != 0:
                    print("%s" % packetHandler.getRxPacketError(dxl_error))
        time.sleep(0.01)

def main(stdscr):
    global moving, direction, moving_dx_id

    stdscr.nodelay(True)
    stdscr.clear()
    stdscr.addstr(0, 0, "Press and hold the 'q' key to increase and 'a' key to decrease. Release to stop.")
    stdscr.refresh()

    count_thread = threading.Thread(target=move)
    count_thread.daemon = True
    count_thread.start()

    while True:
        key = stdscr.getch()
        if key == ord('q'):
            with lock:
                moving = True
                moving_dx_id = 11
                direction = 1
        elif key == ord('a'):
            with lock:
                moving = True
                moving_dx_id = 11
                direction = -1
        elif key == ord('w'):
            with lock:
                moving = True
                moving_dx_id = 12
                direction = 1
        elif key == ord('s'):
            with lock:
                moving = True
                moving_dx_id = 12
                direction = -1
        elif key == ord('e'):
            with lock:
                moving = True
                moving_dx_id = 13
                direction = 1
        elif key == ord('d'):
            with lock:
                moving = True
                moving_dx_id = 13
                direction = -1
        elif key == ord('r'):
            with lock:
                moving = True
                moving_dx_id = 14
                direction = 1
        elif key == ord('f'):
            with lock:
                moving = True
                moving_dx_id = 14
                direction = -1
        elif key == ord('t'):
            with lock:
                moving = True
                moving_dx_id = 15
                direction = 1
        elif key == ord('g'):
            with lock:
                moving = True
                moving_dx_id = 15
                direction = -1
        else:
            with lock:
                moving = False

        if key == 27:  # ESC key
            break

        time.sleep(0.1)

curses.wrapper(main)

for dxl_id in range(11, 16):
    dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, dxl_id, ADDR_TORQUE_ENABLE, TORQUE_DISABLE)
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error))

portHandler.closePort()
