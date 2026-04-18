"""
Simple Screenshot Application
Press F9 to take a screenshot of your entire screen.
Press ESC to exit the application.
"""

import os
from datetime import datetime
from pathlib import Path
from mss import mss
from mss import tools
from PIL import Image, ImageTk
from pynput import keyboard
import tkinter as tk

# Global Variables
SCREENSHOT_KEY = keyboard.Key.f9
EXIT_KEY = keyboard.Key.f10

start_x = None
start_y = None
end_x = None
end_y = None

SCREENSHOT_DIR = Path.home() / "screenshots"
SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)


def screenshot_taker(region) -> bool:
    try:
        currentTime = datetime.now()
        string_time = currentTime.strftime("%Y%m%d%H%M%S")
        filePath = SCREENSHOT_DIR / f"{string_time}.png"

        with mss() as sct:
            # monitor = sct.monitors[1]
            data = sct.grab(region)

            final_data = tools.to_png(data.rgb, data.size, output=str(filePath))

        print(f"Screenshot Saved to {filePath}")
        return True

    except Exception as e:
        print(f"Error taking screenshot: {e}")
        return False

def on_press(key):
    try:
        if key == SCREENSHOT_KEY:
            start_snipping()

        elif key == EXIT_KEY:
            print("Exiting application")
            return False

    except AttributeError as e:
        pass


def start_snipping():
    global canvas, root, bg_photo
    root = tk.Tk()

    with mss() as sct:
        monitor = sct.monitors[1]
        sct_img = sct.grab(monitor)
        img = Image.frombytes("RGB", sct_img.size, sct_img.rgb)
        bg_photo = ImageTk.PhotoImage(img)

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.geometry(f"{screen_width}x{screen_height}+0+0")
    root.overrideredirect(True)
    root.attributes('-topmost', True)
    root.lift()
    root.configure(background='lightblue')

    canvas = tk.Canvas(root, width=1920, height=1080)
    canvas.pack(fill="both", expand=True)

    canvas.bind("<ButtonPress-1>", on_mouse_press)
    canvas.bind("<B1-Motion>", on_mouse_drag)
    canvas.bind("<ButtonRelease-1>", on_mouse_release)

    canvas.create_image(0, 0, image=bg_photo, anchor=tk.NW)

    root.mainloop()

def on_mouse_press(event):
    global start_x, start_y
    start_x = event.x
    start_y = event.y

def on_mouse_drag(event):
    canvas.delete("snippet_rect")
    canvas.create_rectangle(
        start_x, start_y, event.x, event.y,
        outline="red", width=1, tags="snippet_rect")

def on_mouse_release(event):
    global end_x, end_y
    end_x = event.x
    end_y = event.y

    left = min(start_x, end_x)
    top = min(start_y, end_y)
    width = abs(start_x - end_x)
    height = abs(start_y - end_y)

    monitor_region = {'top': top, 'left': left, 'width': width, 'height': height}
    screenshot_taker(monitor_region)
    root.destroy()

def main():
    "Main function"
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

    print("Application Finished")

if __name__ == "__main__":
    main()