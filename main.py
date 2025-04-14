
# import keyboard
# import time
# import threading
# import random
# import pyautogui
# import os

# def press_key(key, interval):
#     while True:
#         if not paused:
#             keyboard.press_and_release(str(key))
#         time.sleep(interval + random.uniform(0, 2.2))

# def click_mouse(interval, key):
#     active_clicks[key] = True
#     while active_clicks[key]:
#         if not paused:
#             x, y = pyautogui.position()
#             offset_x = random.randint(-5, 5)
#             offset_y = random.randint(-5, 5)
#             pyautogui.click(x + offset_x, y + offset_y)
#         time.sleep(interval + random.uniform(0, 2.2))
#     active_clicks[key] = False

# def toggle_pause():
#     global paused
#     paused = not paused
#     print("Paused" if paused else "Resumed")
#     update_display()

# def toggle_clicking(key, interval):
#     if key in active_clicks and active_clicks[key]:
#         active_clicks[key] = False
#     else:
#         threading.Thread(target=click_mouse, args=(interval, key), daemon=True).start()
#     update_display()

# def update_display():
#     os.system('cls' if os.name == 'nt' else 'clear')
#     print("=== Script Status ===")
#     print(f"Paused: {'Yes' if paused else 'No'}")
#     print("Active Clicks:")
#     for key, active in active_clicks.items():
#         print(f" - {key.upper()}: {'Active' if active else 'Inactive'}")
#     print("\nPress 'P' to pause/resume. Press 'ESC' to exit.")

# time.sleep(3)

# paused = False
# active_clicks = {"s": False, "f": False}
# keyboard.add_hotkey('p', toggle_pause)

# # Start/stop mouse click threads on 's' and 'f' key press
# keyboard.add_hotkey('s', lambda: toggle_clicking("s", 60))
# keyboard.add_hotkey('f', lambda: toggle_clicking("f", 5))

# keys_intervals = {1: 4, 2: 15, 3: 20, 4: 15, 5: 30}
# threads = []

# for key, interval in keys_intervals.items():
#     thread = threading.Thread(target=press_key, args=(key, interval), daemon=True)
#     thread.start()
#     threads.append(thread)



# update_display()
# keyboard.wait('esc')





import keyboard
import time
import threading
import random
import pyautogui
import os
import curses
# pip install windows-curses

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
            offset_x = random.randint(-5, 5)
            offset_y = random.randint(-5, 5)
            pyautogui.click(x + offset_x, y + offset_y)
            countdown(row, fast_countdown)          
        else:
            update_countdown(row, 0)
            time.sleep(pause_time)

def click_mouse_slow(key, interval):
    row = 3
    while True:
        if mouse_slow:            
            offset_x = random.randint(-2, 2)
            offset_y = random.randint(-2, 2)
            pyautogui.click(x + offset_x, y + offset_y)
            countdown(row, slow_countdown)
        else:
            update_countdown(row, 0)
            time.sleep(pause_time)


def click_mouse_plants(key, interval):
    global plants_action
    row = 4
    while True:
        if mouse_plants:            
            offset_x = random.randint(-2, 2)
            offset_y = random.randint(-2, 2)
            pyautogui.click(x + offset_x, y + offset_y)
            plants_action = "growing"
            countdown(row, plan_growing_countdown)
            offset_x = random.randint(-2, 2)
            offset_y = random.randint(-2, 2)
            pyautogui.click(x + offset_x, y + offset_y)
            plants_action = "harvesting "
            countdown(row, plan_harvesting_countdown)
        else:
            update_countdown(row, 0)
            plants_action = "nothing"
            time.sleep(pause_time)

# def update_display():
#     os.system('cls' if os.name == 'nt' else 'clear')
#     print("=== Active Components ===")
#     print(f"(K)eys:\t\t{'Yes' if keys_active else 'No'}")
#     print(f"(F)ast mouse:\t{'Yes' if mouse_fast else 'No'}")
#     print(f"(S)low mouse:\t{'Yes' if mouse_slow else 'No'}")
#     print(f"(P)lant mouse:\t{'Yes' if mouse_plants else 'No'}")
#     print(f"(P)lant:\t{plants_action}")
#     print(f"Pos: \t\t{x},{y}")

#     print("\nPress 'ESC' to exit.")


def update_display():
    stdscr.addstr(0, 0, "=== Active Components ===")
    stdscr.addstr(1, 0, f"(K)eys:\t\t{'Yes' if keys_active else 'No '}")
    stdscr.addstr(2, 0, f"(F)ast mouse:\t{'Yes' if mouse_fast else 'No '}")
    stdscr.addstr(3, 0, f"(S)low mouse:\t{'Yes' if mouse_slow else 'No '}")
    stdscr.addstr(4, 0, f"(P)lant mouse:\t{'Yes' if mouse_plants else 'No '}")
    stdscr.addstr(5, 0, f"(P)lant:\t{plants_action}")
    stdscr.addstr(6, 0, f"Pos: \t\t{x},{y}       ")
    stdscr.addstr(8, 0, "Press 'ESC' to exit.")
    stdscr.refresh()


def update_countdown(row, i):
    stdscr.addstr(row, 30, f"({i})  ")
    stdscr.refresh()

def toggle_pause():
    global keys_active
    keys_active = not keys_active
    update_display()

def toggle_mouse_slow():
    global mouse_fast, mouse_slow,x,y
    x, y = pyautogui.position()
    mouse_slow = not mouse_slow
    if(mouse_slow):
        mouse_fast = False
    update_display()

def toggle_mouse_fast():
    global mouse_fast, mouse_slow,x,y
    x, y = pyautogui.position()
    mouse_fast = not mouse_fast
    if(mouse_fast):
        mouse_slow = False
    update_display()

def toggle_mouse_plants():
    global mouse_plants,x,y
    x, y = pyautogui.position()
    mouse_plants = not mouse_plants
    update_display()


keys_active = False
mouse_slow = False
mouse_fast = False
mouse_plants = False
plants_action = "nothing     "
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
    update_display()
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


