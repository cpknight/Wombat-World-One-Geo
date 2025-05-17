#!/usr/bin/env python3

import pyautogui
import time
from Xlib import display

# -----------------------------------------------------------------------------------------------------------------
# VERY SHORT DELAY FUNCTION
# -----------------------------------------------------------------------------------------------------------------

def micro_delay(duration):
    start = time.perf_counter()
    while time.perf_counter() - start < duration:
        pass


# -----------------------------------------------------------------------------------------------------------------
# CHECK FOR MINECRAFT FOCUS FUNCTION
# -----------------------------------------------------------------------------------------------------------------

# Function to check if Minecraft (or any window with specific title) is in focus
def is_minecraft_focused():
    d = display.Display()
    root = d.screen().root
    window_name = root.get_full_property(d.intern_atom('_NET_ACTIVE_WINDOW'), 0).value[0]
    window = d.create_resource_object('window', window_name)
    title = window.get_full_property(d.intern_atom('_NET_WM_NAME'), 0).value

    if isinstance(title, bytes):
        title = title.decode('utf-8')

    # Check if the window title contains "Minecraft"
    return "Minecraft" in title if title else False


# -----------------------------------------------------------------------------------------------------------------
# SEND COMMAND TO MINECRAFT FUNCTION
# -----------------------------------------------------------------------------------------------------------------

# Function to type and send a command to Minecraft chat
def send_command(command):
    pyautogui.press('/')
    for increment in range(10):
        pyautogui.press('backspace')
    for char in command:
        pyautogui.press(char)
    pyautogui.press('enter')  # Send command
    micro_delay(0.05)  # Short delay for command execution

# -----------------------------------------------------------------------------------------------------------------
# GET DISTANCE FUNCTION
# -----------------------------------------------------------------------------------------------------------------

def get_distance():
    try:
        distance = float(input("Enter distance forward (in blocks): "))
        return int(distance)
    except ValueError:
        print("Please enter valid number")
        return None


# -----------------------------------------------------------------------------------------------------------------
# BUILD FUNCTION
# -----------------------------------------------------------------------------------------------------------------

# Function to build the standard northbound tunnel 
def build_tunnel_northeast(distance):
    for x in range(1,distance,1):
        send_command(f"/fill ~-1 ~-2 ~-1 ~4 ~3 ~-2 stone")
        send_command(f"/fill ~ ~ ~-1 ~3 ~1 ~-1 air")
        send_command(f"/tp ~1 ~ ~-1")

        if (x % 5 == 0):
            send_command(f"/setblock ~-1 ~-1 ~ sea_lantern")
            send_command(f"/setblock ~1 ~-1 ~1 sea_lantern")

# -----------------------------------------------------------------------------------------------------------------
# MAIN...
# -----------------------------------------------------------------------------------------------------------------

# Example usage
def main():
    distance = get_distance()
    if distance:

        # Wait for Minecraft to be in focus
        while not is_minecraft_focused():
            print("Waiting for Minecraft to be in focus...")
            time.sleep(1)  # Check every second

        print("Minecraft is now in focus. Pressing escape to get into playing mode.")
        pyautogui.press('escape')  # Press the escape key
        time.sleep(0.5)  # Give a small delay to allow for menu closing or state change

        print("Starting script.")

        # Run the function once Minecraft is focused
        build_tunnel_northeast(distance)
    else:
        print("Failed to get valid distance")


# -----------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    main()

# -----------------------------------------------------------------------------------------------------------------
