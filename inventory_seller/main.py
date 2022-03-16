import time

from pynput.keyboard import Key, Listener
from PIL import ImageGrab

import pyautogui
import argparse

BIND = None

INV = 828, 27
BAG1 = 1346, 574

TEST = 1332, (603, 603 + 81, 603 + 161, 603 + 242)
SLOTSIZE = 76


def open_smelt():
    pyautogui.click(826, 25)
    time.sleep(0.1)
    pyautogui.rightClick(1447, 647)

def script(key):
    global BIND
    if key == Key.end:
        quit()
    if not BIND:
        BIND = key
        print(f'Binded key: {key.__str__()}')
        print('Script ready, press END to quit')
    elif key == BIND:
        _start = time.perf_counter()
        print('Launched')
        main_script()
        et = time.perf_counter() - _start
        print(f'Done in {et:0.4f} seconds\n')


def get_offset(val):
    if val == 0:
        return 0
    elif val == 1:
        return 5
    elif val == 2:
        return 9
    elif val == 3:
        return 14
    elif val == 4:
        return 18
    else:
        return 18 + (val - 4) * 5


blue = ((63, 68), (121, 127), (184, 191))
purple = ((169, 180), (49, 55), (85, 102))
gold = ((248, 256), (188, 201), (86, 92))
unique = ((249, 256), (248, 255), (97, 107))
set_item = ((91, 124), (205, 219), (232, 242))


color_item = ((120, 131), (96, 107), (66, 77))


def main_script():
    _start = time.perf_counter()
    mx, my = pyautogui.position()
    if args.use_dog:
        pyautogui.click(887, 29)
        time.sleep(0.05)
        pyautogui.rightClick(607 + (100 * (DOG[1] - 1)), 639 + (100 * (DOG[0] - 1)))
        time.sleep(0.05)
    smelt = 0
    if not args.smelt:
        open_sell()
    else:
        open_smelt()
    for bag in BAGS:
        pyautogui.click(BAG1[0] + 50 * (bag - 1), BAG1[1])
        time.sleep(0.05)
        pyautogui.moveTo(BAG1[0] + 50 * 9, BAG1[1])
        print(f'Processing bag {bag}')
        slots = []
        for j in range(4):
            for i in range(7):
                pixels = ImageGrab.grab((TEST[0] + SLOTSIZE * i + get_offset(i) + 37,
                                         TEST[1][j] + 16,
                                         TEST[0] + SLOTSIZE * i + get_offset(i) + 38,
                                         TEST[1][j] + + 17)).load()

                if any([check_pixels(m, pixels, 0, 0) for m in (blue, purple, gold, unique, set_item, color_item)]):
                    slots.append((TEST[0] + SLOTSIZE * i + get_offset(i) + 37, TEST[1][j] + 16))
        for i in slots:
            if not args.smelt:
                pyautogui.rightClick(i[0], i[1], _pause=False)
                time.sleep(0.075)
            else:
                if smelt == 9:
                    smelt = 0
                    pyautogui.click(501, 782)
                    time.sleep(0.075)
                pyautogui.rightClick(i[0], i[1], _pause=False)
                time.sleep(0.075)
                smelt += 1
    if args.smelt:
        pyautogui.click(501, 782)
        time.sleep(0.075)
    if not args.use_dog:
        pyautogui.click(1899, 92) if args.inv_close else None
        time.sleep(0.05)
        pyautogui.moveTo(mx, my)
    else:
        pyautogui.click(1899, 92)
        time.sleep(0.05)
        pyautogui.click(887, 29)
        _done = time.perf_counter()
        if _done - _start < 6:
            print(_done - _start)
            time.sleep(int(6 - (_done - _start)) + 1)
        pyautogui.rightClick(607 + (100 * (PET[1] - 1)), 639 + (100 * (PET[0] - 1)))
        time.sleep(0.05)
        pyautogui.click(887, 29)
        time.sleep(0.2)
        open_sell() if not args.inv_close else None


def open_sell():
    pyautogui.click(771, 24)
    time.sleep(0.05)
    pyautogui.click(686, 182)
    time.sleep(0.05)
    pyautogui.click(1018, 846)


def colors(slotx, sloty):
    ppixels = ImageGrab.grab((TEST[0] + SLOTSIZE * (slotx - 1) + get_offset(slotx - 1), TEST[1][sloty - 1],
                              TEST[0] + SLOTSIZE * (slotx - 1) + get_offset(slotx - 1) + SLOTSIZE,
                              TEST[1][sloty - 1] + SLOTSIZE)).load()
    stack = set()
    for xi in range(36, 38):
        stack.add(ppixels[xi, 16])
    return stack


def check_pixels(stack, arr_pixels, x, y):
    r, g, b = arr_pixels[x, y]
    r1, g1, b1 = stack
    if r1[0] <= r <= r1[1] and g1[0] <= g <= g1[1] and b1[0] <= b <= b1[1]:
        return True
    return False


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--inv-close', action='store_false', default=True)
    parser.add_argument('--use-dog', action='store_true', default=False)
    parser.add_argument('--smelt', action='store_true', default=False)
    args = parser.parse_args()
    # {(112, 87, 60), (114, 92, 69)}
    # {(112, 87, 60)}
    # {(112, 87, 60), (112, 87, 61)}
    # {(139, 113, 79), (129, 105, 71)}
    # print(colors(2, 1))
    # quit()

    BAGS = tuple(map(int, input('Введите сумки через пробел (1-9): ').split()))

    DOG = tuple(map(int, input('Введите координаты собаки в альбоме '
                               '(строка, ячейка, 2 цифры через пробел): ').split())) if args.use_dog else (0, 0)

    PET = tuple(map(int, input('Введите координаты основного пета в альбоме '
                               '(строка, ячейка, 2 цифры через пробел):').split())) if args.use_dog else (0, 0)

    print('Press any key to bind...')
    if BAGS:
        with Listener(on_press=script) as l:
            l.join()
