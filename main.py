"""
Simple Screenshot Application
Press F9 to take a screenshot of your entire screen.
Press ESC to exit the application.
"""

import os
from datetime import datetime
from pathlib import Path
from mss import mss
from pynput import keyboard

# Global Variables
SCREENSHOT_KEY = keyboard.Key.f9
EXIT_KEY = keyboard.Key.f10

SCREENSHOT_DIR = Path.home() / "screenshots"
SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)


def screenshot_taker() -> bool:
    try:
        currentTime = datetime.now()
        string_time = currentTime.strftime("%Y%m%d%H%M%S")
        filePath = SCREENSHOT_DIR / f"{string_time}.png"

        with mss() as sct:
            monitor = sct.monitors[0]
            data = sct.grab(monitor)

            final_data = mss.tools.to_png(data.rgb, data.size, output=filePath)

        print("Screenshot Saved to " + filePath)
        return True

    except Exception as e:
        print(f"Error taking screenshot: {e}")
        return False


def main():
    "Main function"
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

    print("Application Finished")

if __name__ == "__main__":
    main()