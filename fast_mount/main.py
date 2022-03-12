import os.path
import sys
import pyautogui
import argparse
import keyboard

from ctypes import windll
from pynput.keyboard import Key, Listener, Controller
from keys import get_key
from time import sleep
from PIL import ImageGrab

PAGE = 1343, 572
SLOT = 1368, 645
DX, DY = 75, 75

OPENED = (145, 180, 200)


def check_inv_opened():
    #     825 46
    return ImageGrab.grab((825, 46, 826, 47)).load()[0, 0] == OPENED


def on_press(key):
    global key_now, k_row
    keys = {
        Key.f1: 'f1',
        Key.f2: 'f2',
        Key.f3: 'f3',
        Key.f4: 'f4',
        Key.f5: 'f5',
        Key.f6: 'f6',
        Key.f7: 'f7',
        Key.f8: 'f8',
        Key.f9: 'f9',
        Key.f10: 'f10',
        Key.f11: 'f11',
        Key.f12: 'f12',
        Key.caps_lock: 'caps',
        Key.tab: 'TAB'
    }

    if (key in keys.keys() or not key.__str__().startswith('Key')) and not key.__str__().startswith('<'):
        k_row = key
        key = keys[key] if key in keys.keys() else key.__str__()
        key_now = key
        return False
    else:
        key_now = 'err'
        print('Клавиша не поддерживается')


def main_script(sc_x, sc_y, x0, y0):
    global control, x, y, k_row, active
    temp = k_row
    k_row = None
    control.press(temp)
    control.release(temp)
    pyautogui.click(826 * sc_x, 26 * sc_y) if not check_inv_opened() else None
    pyautogui.click(PAGE[0] * sc_x, PAGE[1] * sc_y)
    pyautogui.doubleClick(SLOT[0] * sc_x + DX * sc_x * (x - 1) + 8 * (x - 1) * sc_x, SLOT[1] * sc_y + DY * sc_y * (y - 1) + 7 * (y - 1) * sc_y)
    sleep(0.3)
    control.press(temp)
    control.release(temp)
    sleep(0.1)
    print(SLOT[0] * sc_x + DX * sc_x * (x - 1) + 8 * (x - 1), SLOT[1] * sc_y + DY * sc_y * (y - 1) + 8 * (y - 1)) if DEBUG else None
    pyautogui.doubleClick(SLOT[0] * sc_x + DX * sc_x * (x - 1) + 8 * (x - 1) * sc_x, SLOT[1] * sc_y + DY * sc_y * (y - 1) + 7 * (y - 1) * sc_y)
    pyautogui.click(826 * sc_x, 26 * sc_y)
    pyautogui.moveTo(x0, y0)
    k_row = temp


def on_press_script(key):
    global k_row, control, active, DEBUG
    if key == Key.end:
        sys.exit()
    if DEBUG:
        if key == Key.f11:
            print(pyautogui.position())
    if k_row == key:
        if not active:
            active = 2
            mouse_x, mouse_y = pyautogui.position()
            user32 = windll.user32
            screen_res = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
            scaled_x, scaled_y = screen_res[0] / 1920, screen_res[1] / 1080
            print(mouse_x, mouse_y) if DEBUG else None
            main_script(scaled_x, scaled_y, mouse_x, mouse_y)
        else:
            active -= 1


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    check_inv_opened()
    active = 0
    prs = argparse.ArgumentParser()
    prs.add_argument('-n', action='store_true')
    prs.add_argument('--debug', action='store_true')
    args = prs.parse_args()
    DEBUG = args.debug
    if args.n:
        try:
            os.remove('settings.txt')
        except:
            pass
    key_now = ''
    k_row = None
    if not os.path.exists('./settings.txt'):
        print('Нажмите любую клавишу чтобы назначить')
        with Listener(on_press=on_press) as l:
            l.join()
        print('Назначенная клавиша: {}'.format(key_now).replace("'", ''))
        print('Введите строку и слот плаща в инвентаре (Плащ должен находиться на первой странице)')
        x, y = -1, -1
        while y == -1:
            try:
                y2 = int(input('Строка (от 1 до 4): '))
                if 1 <= y2 <= 4:
                    y = y2
                else:
                    y = -1
            except ValueError as e:
                y = -1
        while x == -1:
            try:
                x2 = int(input('Слот (от 1 до 7): '))
                if 1 <= x2 <= 7:
                    x = x2
                else:
                    x = -1
            except ValueError as e:
                x = -1
        with open('settings.txt', 'w') as f:
            f.write(f'''{x} {y} {key_now.replace("'", "")}''')
        print('Настройки созданы')
    else:
        fdata = open('settings.txt', 'r').read().split()
        x, y = map(int, [fdata[0], fdata[1]])
        k_row = get_key(fdata[2])
        key_now = fdata[2]
        print('Настройки загруженны')
    control = Controller()
    print()
    print('Для остановки нажмите End')
    print(f'''Назначенная клавиша: {key_now.replace("'", '')}''')
    print('Для переназначения клавиши удалите файл settings.txt, либо запустите скрипт с аргументом "-n"')
    with Listener(on_press=on_press_script) as l:
        l.join()