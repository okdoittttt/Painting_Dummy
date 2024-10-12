import requests
import curses
import time

API_URL = "http://localhost:8000"  # FastAPI 서버 주소

def move_motor(motor_id, direction):
    try:
        response = requests.post(f"{API_URL}/move_motor/{motor_id}/{direction}")
        if response.status_code == 200:
            print(response.json())
        else:
            print(f"Error: {response.status_code}")
    except Exception as e:
        print(f"Failed to move motor {motor_id}: {str(e)}")

def move_dual_motors(direction_12: str, direction_13: str):

    try:
        response = requests.post(f"{API_URL}/move_dual_motors/{direction_12}/{direction_13}")
        if response.status_code == 200:
            print(response.json())
        else:
            print(f"Error: {response.status_code}")
    except Exception as e:
        print(f"Failed to move dual motors: {str(e)}")

def move_height_motors(direction_13: str, direction_14: str):

    try:
        response = requests.post(f"{API_URL}/move_height_motors/{direction_13}/{direction_14}")
        if response.status_code == 200:
            print(response.json())
        else:
            print(f"Error: {response.status_code}")
    except Exception as e:
        print(f"Failed to move dual motors: {str(e)}")

def main(stdscr):
    curses.curs_set(0)  # Hide the cursor
    stdscr.nodelay(True)
    stdscr.timeout(100)

    while True:
        key = stdscr.getch()

        if key == ord('d'):
            move_motor(11, 'ccw')
        elif key == ord('a'):
            move_motor(11, 'cw')
        elif key == ord('w'):
            move_dual_motors('cw', 'ccw')
        elif key == ord('s'):
            move_dual_motors('ccw','cw')
        # elif key == ord('i'):
        #     move_motor(13, 'ccw')
        # elif key == ord('k'):
        #     move_motor(13, 'cw')
        elif key == ord('o'):
            move_height_motors('ccw', 'cw')
        elif key == ord('l'):
            move_height_motors('cw', 'ccw')

        # Stop all motors if no key is pressed
        if key == curses.ERR:
            move_motor(11, 'stop')
            move_motor(13, 'stop')
            move_motor(14, 'stop')
            move_dual_motors('stop','stop')
            move_height_motors('stop','stop')

        if key == 27:  # ESC key to exit
            break

        time.sleep(0.1)

if __name__ == "__main__":
    curses.wrapper(main)
