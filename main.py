import keyboard
import time
import threading
import random
import pyautogui
import os
import curses
# pip install windows-curses
# pip install pyautogui
# pip install keyboard

def randomi(i):
    return random.randint(-i, i)    

def press_key(key, interval):
    while True:
        if keys_active:
            keyboard.press_and_release(str(key))
        time.sleep(interval + random.uniform(-0.3, 0.3))

def countdown(row, interval):
    for i in range(interval):
        update_countdown(row, interval-i)
        time.sleep(1)
    time.sleep(random.uniform(0, 0.3))

def click_mouse_fast(key, interval):
    row = 2
    while True:
        if mouse_fast:           
            pyautogui.click(x + randomi(5), y + randomi(5))
            countdown(row, fast_countdown)          
        else:
            update_countdown(row, 0)
            time.sleep(pause_time)

def click_mouse_slow(key, interval):
    row = 3
    while True:
        if mouse_slow:            
            pyautogui.click(x + randomi(2), y + randomi(2))
            countdown(row, slow_countdown)
        else:
            update_countdown(row, 0)
            time.sleep(pause_time)


def click_mouse_plants(key, interval):
    global plants_action
    row = 4
    while True:
        if mouse_plants:            
            pyautogui.click(x + randomi(2), y + randomi(2))
            update_countdown(5,"growing")
            countdown(row, plan_growing_countdown)
            pyautogui.click(x + randomi(2), y + randomi(2))
            update_countdown(5,"harvesting")
            countdown(row, plan_harvesting_countdown)
        else:
            update_countdown(row, 0)
            update_countdown(5, "nothing")
            time.sleep(pause_time)


def setup_display():
    stdscr.addstr(0, 0, "=== Active Components ===")
    stdscr.addstr(1, 0, f"(K)eys:\t\t{'Yes' if keys_active else 'No '}")
    stdscr.addstr(2, 0, f"(F)ast mouse:\t{'Yes' if mouse_fast else 'No '}")
    stdscr.addstr(3, 0, f"(S)low mouse:\t{'Yes' if mouse_slow else 'No '}")
    stdscr.addstr(4, 0, f"(P)lant mouse:\t{'Yes' if mouse_plants else 'No '}")
    stdscr.addstr(5, 0, f"(P)lant:")
    stdscr.addstr(6, 0, f"Pos: \t\t{x},{y}       ")
    stdscr.addstr(8, 0, "Press 'ESC' to exit.")
    stdscr.refresh()


def update_countdown(row, i):
    if (isinstance(i, str) or i > 0):
        stdscr.addstr(row, 23, f"({i})           ")
    # elif (isinstance(i, str)):
    #     stdscr.addstr(row, 23, f"({i})  ")
    else:
        stdscr.addstr(row, 23, "                     ")
    stdscr.refresh()

def toggle_pause():
    global keys_active
    keys_active = not keys_active
    setup_display()

def toggle_mouse_slow():
    global mouse_plants, mouse_slow, mouse_fast, x, y
    x, y = pyautogui.position()
    mouse_slow = not mouse_slow
    if(mouse_slow):
        mouse_fast = False
        mouse_plants = False

    setup_display()

def toggle_mouse_fast():
    global mouse_plants, mouse_slow, mouse_fast, x, y
    x, y = pyautogui.position()
    mouse_fast = not mouse_fast
    if(mouse_fast):
        mouse_slow = False
        mouse_plants = False
    setup_display()

def toggle_mouse_plants():
    global mouse_plants, mouse_slow, mouse_fast, x, y
    x, y = pyautogui.position()
    mouse_plants = not mouse_plants
    if(mouse_plants):
        mouse_slow = False
        mouse_fast = False
    setup_display()


keys_active = False
mouse_slow = False
mouse_fast = False
mouse_plants = False

slow_countdown = 60
fast_countdown = 10
plan_growing_countdown = 30
plan_harvesting_countdown = 15
pause_time = 3
x=500
y=500
keyboard.add_hotkey('k', toggle_pause)
keyboard.add_hotkey('s', toggle_mouse_slow)
keyboard.add_hotkey('f', toggle_mouse_fast)
keyboard.add_hotkey('p', toggle_mouse_plants)
stdscr = None


def main(stdscrr):
    global stdscr
    # Initialize curses
    stdscr = stdscrr
    curses.curs_set(0)  # Hide cursor
    stdscr.clear()
    stdscr.nodelay(1)  # Non-blocking input
    setup_display()
    keys_intervals = {1: 4, 2: 15, 3: 190, 4: 14, 5: 28}

    threads = []

    for key, interval in keys_intervals.items():
        thread = threading.Thread(target=press_key, args=(key, interval), daemon=True)
        thread.start()
        threads.append(thread)

    thread = threading.Thread(target=click_mouse_fast, args=("",10), daemon=True)
    thread.start()
    threads.append(thread)

    thread2 = threading.Thread(target=click_mouse_slow, args=("",60), daemon=True)
    thread2.start()
    threads.append(thread2)

    thread3 = threading.Thread(target=click_mouse_plants, args=("",60), daemon=True)
    thread3.start()
    threads.append(thread3)

    
    # Check for exit
    keyboard.wait('esc')

if __name__ == "__main__":
    os.system('cls' if os.name == 'nt' else 'clear')
    curses.wrapper(main)


