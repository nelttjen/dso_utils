from PIL import ImageGrab
from pynput.keyboard import Key, Listener

import pyautogui
import time
import ctypes


KEY = None

BAG1 = 1346, 574
MAPCOORDS = 1369, 636
ARROWBACK = 301, 175
KINGSHILL = 680, 444
KINGSHILL2 = 603, 306

ATLANTIDA = 1314, 644
XRAMS = 975, 545

GROTS = 933, 536
SKLEP = 913, 307
CAVES = 922, 374

MERCY = 1128, 557
ENTER = 1350, 830
SKILL = 778, 1046
SCROLL = 'D'
OPENED = (145, 180, 200)


def check_inv_opened():
    #     825 46
    return ImageGrab.grab((825 * sc_x, 46 * sc_y, 826 * sc_x, 47 * sc_y)).load()[0, 0] == OPENED


def normalize_map():
    pyautogui.click(828 * sc_x, 27 * sc_y)
    time.sleep(0.03)
    pyautogui.click(BAG1[0] * sc_x, BAG1[1] * sc_y)
    time.sleep(0.03)
    pyautogui.click(MAPCOORDS[0] * sc_x, MAPCOORDS[1] * sc_y, button='right')
    time.sleep(0.03)
    pyautogui.click(ARROWBACK[0] * sc_x, ARROWBACK[1] * sc_y)
    time.sleep(0.03)


def select_tegan_region():
    pyautogui.click(784 * sc_x, 199 * sc_y)


def select_parallel_region():
    pyautogui.click(922 * sc_x, 484 * sc_y)


def enter_brigavik():
    pyautogui.click(1280 * sc_x, 671 * sc_y)
    time.sleep(0.03)
    pyautogui.click(ENTER[0] * sc_x, ENTER[1] * sc_y)
    time.sleep(0.03)
    pyautogui.click(949 * sc_x, 571 * sc_y)


def enter_stonekeep():
    pyautogui.click(1321 * sc_x, 642 * sc_y)
    time.sleep(0.03)
    pyautogui.click(ENTER[0] * sc_x, ENTER[1] * sc_y)
    time.sleep(0.03)
    pyautogui.click(949 * sc_x, 571 * sc_y)


def on_press(key):
    global KEY
    if key == Key.end:
        quit()
    if not KEY:
        KEY = key
        print(f'binded key: {key.__str__()}')
    elif key == KEY:
        normalize_map()
        if mode == 1:
            select_tegan_region()
            enter_stonekeep()
        if mode == 2:
            select_parallel_region()
            enter_brigavik()


if __name__ == '__main__':
    user32 = ctypes.windll.user32
    sc_x, sc_y = user32.GetSystemMetrics(0) / 1920, user32.GetSystemMetrics(1) / 1080
    mode = int(input('Режим (1 - стоункиип, 2 - бригавик): '))
    print('press key to bind')
    with Listener(on_press=on_press) as l:
        l.join()