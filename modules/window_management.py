import pygetwindow as gw
import win32gui
import modules.output as output
from screeninfo import get_monitors

def setup_window(window_title="Roblox", width=2560, height=1600):
    # Get screen center
    for m in get_monitors():
        screen_width, screen_height = m.width, m.height
    center_x, center_y = screen_width // 2, screen_height // 2

    # Look for the Roblox window
    roblox_window = None
    for win in gw.getAllWindows():
        if window_title in win.title:
            class_name = win32gui.GetClassName(win._hWnd)
            if "Chrome_WidgetWin_1" not in class_name:
                roblox_window = win
                break

    if not roblox_window:
        output.printError("Roblox window not found. Open Roblox and try again!")
        return None

    if roblox_window.isMinimized:
        roblox_window.restore()

    roblox_window.resizeTo(width, height)
    roblox_window.moveTo(center_x - width // 2, center_y - height // 2)
    hwnd = roblox_window._hWnd
    win32gui.SetForegroundWindow(hwnd)

    if roblox_window.size != (width, height):
        output.printError("Failed to resize the Roblox window.")

    coords = {
        "hwnd": hwnd,
        "firstX": 815,
        "firstY": 269,
        "lastX":  1747,
        "lastY":  1200,
        "openButtonX": 1472,
        "openButtonY": 1282,
        "inputX": 1470,
        "inputY": 1143,
        "closeButtonX": 1831,
        "closeButtonY": 716 
    }

    return coords
