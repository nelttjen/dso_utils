from pynput.keyboard import Key, KeyCode
import os


def get_key(char):
    keys = {
        'f1': Key.f1,
        'f2': Key.f2,
        'f3': Key.f3,
        'f4': Key.f4,
        'f5': Key.f5,
        'f6': Key.f6,
        'f7': Key.f7,
        'f8': Key.f8,
        'f9': Key.f9,
        'f10': Key.f10,
        'f11': Key.f11,
        'f12': Key.f12,
        'caps': Key.caps_lock,
        'TAB': Key.tab
    }
    if char in keys.keys():
        return keys[char]
    else:
        try:
            return KeyCode.from_char(char)
        except:
            try:
                os.remove('settings.txt')
                quit()
            except:
                quit()