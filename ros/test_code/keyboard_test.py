import curses
import time
import threading

# 초기 count 값을 설정합니다.
count = 0
running = False
lock = threading.Lock()

# count를 증가시키는 함수입니다.
def increment_count():
    global count
    while running:
        with lock:
            count += 1
        print(f"Current count: {count}")
        time.sleep(0.01)

# curses 초기화 및 키 이벤트 처리 함수
def main(stdscr):
    global running

    # nodelay를 설정하여 getch가 블록되지 않도록 합니다.
    stdscr.nodelay(True)
    stdscr.clear()
    stdscr.addstr(0, 0, "Press and hold the 'a' key to start counting. Release the key to stop and exit.")
    stdscr.refresh()

    while True:
        key = stdscr.getch()
        if key == ord('a'):
            if not running:
                running = True
                # count를 증가시키는 스레드를 시작합니다.
                count_thread = threading.Thread(target=increment_count)
                count_thread.daemon = True
                count_thread.start()
        else:
            if running:
                running = False
                break
        time.sleep(0.01)

try:
    curses.wrapper(main)
except KeyboardInterrupt:
    print("Program terminated.")
