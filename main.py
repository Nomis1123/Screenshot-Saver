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



def main():
    "Main function"
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

    print("Application Finished")

if __name__ == "__main__":
    main()