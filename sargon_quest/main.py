import time

from pynput.keyboard import Key, Listener, Controller
import sys
import pyautogui
from ctypes import windll


def click1(dx, dy):
    pyautogui.click(470 * dx, 130 * dy)
    time.sleep(0.1)
    pyautogui.click(549 * dx, 280 * dy)
    time.sleep(0.1)


def on_press(key):
    global SCREEN_RES
    dx, dy = RESX / 1920, RESY / 1080
    if key == Key.f7:
        times_now = times
        while times_now > 0:
            times_now -= 1
            pyautogui.click(909 * dx, 417 * dy)
            pyautogui.click(909 * dx, 417 * dy)
            time.sleep(0.1)
            pyautogui.click(549 * dx, 280 * dy)
            time.sleep(0.1)
            for i in range(4):
                click1(dx, dy)
            time.sleep(0.1)
            pyautogui.click(549 * dx, 280 * dy)
            pyautogui.click(566 * dx, 281 * dy)
            pyautogui.click(566 * dx, 281 * dy)
        sys.exit()


if __name__ == '__main__':
    keyboard = Controller()
    USER32 = windll.user32
    SCREEN_RES = RESX, RESY = USER32.GetSystemMetrics(0), USER32.GetSystemMetrics(1)
    times = int(input('Кол-во повторов алгоритма: '))
    print('Для запуска нажмите F7')
    with Listener(on_press=on_press) as l:
        l.join()