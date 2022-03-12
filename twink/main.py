import ctypes

from pynput.keyboard import Key, Listener, Controller

import time
import pyautogui
import schedule
from PIL import Image, ImageGrab

now_running = True
load_pixel = None

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


# 1 1763 634

# 5 1440x900 1311 753
# 5 1763 903


def normalize_map():
    pyautogui.click(828 * sc_x, 27 * sc_y)
    time.sleep(0.05)
    pyautogui.click(BAG1[0] * sc_x, BAG1[1] * sc_y)
    time.sleep(0.05)
    pyautogui.click(MAPCOORDS[0] * sc_x, MAPCOORDS[1] * sc_y, button='right')
    time.sleep(0.05)
    pyautogui.click(ARROWBACK[0] * sc_x, ARROWBACK[1] * sc_y)
    time.sleep(0.05)


def enter_grots():
    pyautogui.click(GROTS[0] * sc_x, GROTS[1] * sc_y)
    time.sleep(0.2)
    pyautogui.click(ENTER[0] * sc_x, ENTER[1] * sc_y)


def enter_caves():
    pyautogui.click(CAVES[0] * sc_x, CAVES[1] * sc_y)
    time.sleep(0.2)
    pyautogui.click(ENTER[0] * sc_x, ENTER[1] * sc_y)


def enter_sklep():
    pyautogui.click(SKLEP[0] * sc_x, SKLEP[1] * sc_y)
    time.sleep(0.2)
    pyautogui.click(ENTER[0] * sc_x, ENTER[1] * sc_y)


def enter_king():
    pyautogui.click(KINGSHILL[0] * sc_x, KINGSHILL[1] * sc_y)


def select_king_region():
    pyautogui.click(KINGSHILL2[0] * sc_x, KINGSHILL2[1] * sc_y)
    time.sleep(0.05)


def select_atlantida_region():
    pyautogui.click(ATLANTIDA[0] * sc_x, ATLANTIDA[1] * sc_y)


def enter_xrams():
    pyautogui.click(XRAMS[0] * sc_x, XRAMS[1] * sc_y)
    time.sleep(0.2)
    pyautogui.click(ENTER[0] * sc_x, ENTER[1] * sc_y)


def press_skill():
    pyautogui.click(SKILL[0] * sc_x, SKILL[1] * sc_y)


def reload_location():
    global dungeon
    normalize_map()
    select_king_region()
    enter_king()
    check_load()
    time.sleep(13)
    if dungeon == 1:
        normalize_map()
        select_king_region()
        enter_grots()
        check_load()
    if dungeon == 2:
        normalize_map()
        select_king_region()
        enter_sklep()
        check_load()
    if dungeon == 3:
        normalize_map()
        select_king_region()
        enter_caves()
        check_load()
    if dungeon == 4:
        normalize_map()
        select_atlantida_region()
        enter_xrams()
        check_load()


def check_load():
    global load_pixel
    count = 0
    time.sleep(2)
    if not load_pixel:
        load_pixel = ImageGrab.grab((x, y, x + 1, y + 1))
    while True:
        print(f'load screen {count}')
        if count == 15:
            count = 0
            print('new attempt')
            pyautogui.click(951, 1018)
        time.sleep(1)
        temp = ImageGrab.grab((x, y, x + 1, y + 1))
        if temp == load_pixel:
            count += 1
        else:
            return


def check_run():
    global x, y, now_running, pixel
    newpixel = ImageGrab.grab((x, y, x + 1, y + 1))
    newpixel = newpixel.load()[0, 0]
    if newpixel != pixel:
        time.sleep(0.5)
        pixel2 = ImageGrab.grab((x, y, x + 1, y + 1))
        pixel2 = pixel2.load()[0, 0]
        if pixel2 != pixel:
            now_running = False
    elif not now_running and newpixel == pixel:
        now_running = True
    if not now_running:
        reload_location()
        time.sleep(3)
        pixel = ImageGrab.grab((x, y, x + 1, y + 1)).load()[0, 0]


if __name__ == '__main__':
    x, y = map(int, input('Координаты звезды (FHD игра на 1 мониторе, x,y через пробел): ').split())
    dungeon = int(input('Режим (1 - гроты, 2 - склеп, 3 - пещеры, 4 - храмы): '))
    # time.sleep(10)
    user32 = ctypes.windll.user32
    sc_x, sc_y = user32.GetSystemMetrics(0) / 1920, user32.GetSystemMetrics(1) / 1080
    print('Запущено')
    pixel = ImageGrab.grab((x, y, x + 1, y + 1))
    pixel = pixel.load()[0, 0]
    print(pixel)
    schedule.every().second.do(check_run)
    schedule.every().minute.do(press_skill)
    running = True
    while running:
        schedule.run_pending()
