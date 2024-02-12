import ctypes
import win32clipboard
import threading
import keyboard


def screenshot_ctrl(event):
    if event.name == 'print screen':
        print("PrtSc key pressed!")
        threading.Event().wait(1)
        win32clipboard.OpenClipboard(None)
        
        try:
            data_format = win32clipboard.EnumClipboardFormats(0)
            if data_format == win32clipboard.CF_BITMAP:
                data_handle = win32clipboard.GetClipboardData(data_format)

                print("Clipboard Screenshot Data:", data_handle)
                win32clipboard.EmptyClipboard()
                print("Clipboard data deleted")
                ctypes.windll.user32.MessageBoxW(None, f"Don't pressed PrtSc key.", '경고', 0x30)

            else:
                print("No screenshot data on the clipboard.")
        finally:
            win32clipboard.CloseClipboard()

keyboard.on_press(screenshot_ctrl)