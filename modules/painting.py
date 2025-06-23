import time
import ctypes
from tqdm import tqdm

import modules.output as output
import modules.virtualkeystroke as vkey
import modules.utilities as utilities
from modules.window_management import setup_window
from modules.utilities import verify_color
from PIL import ImageGrab

# === Win32 mouse input setup ===
ctypes.windll.user32.SetProcessDPIAware()
user32 = ctypes.windll.user32

MOUSEEVENTF_MOVE = 0x0001
MOUSEEVENTF_ABSOLUTE = 0x8000
MOUSEEVENTF_LEFTDOWN = 0x0002
MOUSEEVENTF_LEFTUP = 0x0004

screen_width = user32.GetSystemMetrics(0)
screen_height = user32.GetSystemMetrics(1)

def to_absolute_coords(x, y):
    abs_x = int(x * 65535 / screen_width)
    abs_y = int(y * 65535 / screen_height)
    return abs_x, abs_y

def click(x, y):
    print(f"[DEBUG] Moving to ({x}, {y})")
    abs_x, abs_y = to_absolute_coords(x, y)
    user32.mouse_event(MOUSEEVENTF_MOVE | MOUSEEVENTF_ABSOLUTE, abs_x, abs_y, 0, 0)
    time.sleep(0.1)
    user32.mouse_event(MOUSEEVENTF_LEFTDOWN, abs_x, abs_y, 0, 0)
    time.sleep(0.08)
    user32.mouse_event(MOUSEEVENTF_LEFTUP, abs_x, abs_y, 0, 0)
    time.sleep(0.05)
    
    print("🖱️ Clicked")

def click_pixel(coords, pixel_x, pixel_y, grid_size=32):
    canvas_width = coords["lastX"] - coords["firstX"]
    canvas_height = coords["lastY"] - coords["firstY"]

    pixel_width = canvas_width / grid_size
    pixel_height = canvas_height / grid_size

    click_x = int(coords["firstX"] + pixel_x * pixel_width + pixel_width / 2)
    click_y = int(coords["firstY"] + pixel_y * pixel_height + pixel_height / 2)

    print(f"[DEBUG] Clicking pixel ({pixel_x}, {pixel_y}) → screen coords ({click_x}, {click_y})")
    

def select_color(coords, color):
    hexColor = utilities.rgb2hex(color)
    click(coords["openButtonX"], coords["openButtonY"])
    time.sleep(.1)
    click(coords["inputX"], coords["inputY"])
    vkey.typer(string=hexColor)
    time.sleep(.08)
    click(coords["openButtonX"], coords["openButtonY"])
    time.sleep(.1)

def verify_painted_pixels(image_pixels, coords):
    failed_pixels = []
    canvas_width = coords["lastX"] - coords["firstX"]
    canvas_height = coords["lastY"] - coords["firstY"]
    pixel_width = canvas_width / 32
    pixel_height = canvas_height / 32

    screenshot = ImageGrab.grab((coords["firstX"], coords["firstY"], coords["lastX"], coords["lastY"]))

    for x in range(32):
        for y in range(32):
            target = image_pixels[x, y]
            if target == (255, 255, 255):
                continue
            screen_x = int(x * pixel_width + pixel_width / 2)
            screen_y = int(y * pixel_height + pixel_height / 2)
            pixel_color = screenshot.getpixel((screen_x, screen_y))
            if pixel_color != target:
                failed_pixels.append((target, x, y))

    return failed_pixels

def start_painting(image_pixels, image_name):
    output.printAscii()
    print("   Image selected:", image_name)
    startInput = input("   Begin painting? (y/n) ")
    if startInput.lower() != 'y':
        output.clear()
        quit()

    output.printAscii()
    print("Painting progress:")
    coords = setup_window()
    if coords is None:
        output.printError("Something went wrong. Try again.")
        return

    print("Canvas coords:", coords["firstX"], coords["firstY"], coords["lastX"], coords["lastY"])
    click(1290, 781)

    image_pixels = image_pixels.load()

    pixels = {}
    for x in range(32):
        for y in range(32):
            color = image_pixels[x, y]
            if color != (255, 255, 255):
                pixels.setdefault(color, []).append((x, y))

    time.sleep(1)
    for _ in range(2):
        click(coords["closeButtonX"], coords["closeButtonY"])
    time.sleep(0.5)

    for color in tqdm(pixels):
        print(f"\n[DEBUG] Painting color {color} at {len(pixels[color])} positions")
        select_color(coords, color)
        for pixel in pixels[color]:
            print(f"[DEBUG] -> Pixel {pixel}")
            click_pixel(coords, *pixel)
            


    print("\n🎨 Painting completed, enjoy!")

def test_clicks_and_colors(coords):
    print("\n🧪 Testing clicks on canvas corners and center...\n")

    test_pixels = {
        "top-left": (0, 0),
        "top-right": (31, 0),
        "bottom-left": (0, 31),
        "bottom-right": (31, 31),
        "center": (16, 16)
    }

    canvas_width = coords["lastX"] - coords["firstX"]
    canvas_height = coords["lastY"] - coords["firstY"]

    pixel_width = canvas_width / 32
    pixel_height = canvas_height / 32

    for name, (px, py) in test_pixels.items():
        click_x = int(coords["firstX"] + px * pixel_width + pixel_width / 2)
        click_y = int(coords["firstY"] + py * pixel_height + pixel_height / 2)
        print(f"[DEBUG] Clicking {name} pixel at ({click_x}, {click_y})")
        click(click_x, click_y)
