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
    for increment in range (10):
        pyautogui.press('backspace')
    for char in command:
        pyautogui.press(char)
    pyautogui.press('enter')  # Send command
    micro_delay(0.1)  # Short delay for command execution

# -----------------------------------------------------------------------------------------------------------------
# GET COORDINATES FUNCTION
# -----------------------------------------------------------------------------------------------------------------

def get_coordinates():
    try:
        x = float(input("Enter X coordinate: "))
        y = float(input("Enter Y coordinate: "))
        z = float(input("Enter Z coordinate: "))
        return x, y, z
    except ValueError:
        print("Please enter valid numbers for coordinates")
        return None

# -----------------------------------------------------------------------------------------------------------------
# BUILD FUNCTION
# -----------------------------------------------------------------------------------------------------------------

# Function to build the standard underground room (westbound)
# Assumes starting point is in tunnel, at left edge of room

def build_maritime_marker(x, y, z):
    # Convert coordinates to integers for the commands
    x, y, z = int(x), int(y), int(z)
    base = int(y)
    transition_point = int(63 - 25);    # static

    if (base > transition_point):
        transition_point = int(base);

    send_command(f"/tp {x} {y} {z}")
    send_command(f"/fill {x - 1} {base - 5} {z - 1} {x + 1} {transition_point} {z + 1} stone")
    send_command(f"/fill {x - 1} {transition_point + 1} {z} {x + 1} {transition_point + 1} {z} stone")
    send_command(f"/fill {x} {transition_point + 1} {z - 1} {x} {transition_point + 1} {z + 1} stone")
    send_command(f"/fill {x} {transition_point + 1} {z} {x} 63 {z} stone")
    send_command(f"/fill {x} 64 {z} {x} 66 {z} red_concrete")
    send_command(f"/setblock {x} 65 {z} pearlescent_froglight")
    send_command(f"/tp {x} 75 {z}")

# -----------------------------------------------------------------------------------------------------------------
# MAIN...
# -----------------------------------------------------------------------------------------------------------------

# Example usage
def main():
    coords = get_coordinates()
    if coords:
        x, y, z = coords

        # Wait for Minecraft to be in focus
        while not is_minecraft_focused():
            print("Waiting for Minecraft to be in focus...")
            time.sleep(1)  # Check every second

        print("Minecraft is now in focus. Pressing escape to get into playing mode.")
        pyautogui.press('escape')  # Press the escape key
        time.sleep(0.5)  # Give a small delay to allow for menu closing or state change

        print("Starting script.")

        # Run the function once Minecraft is focused
        build_maritime_marker(x, y, z)
    else:
        print("Failed to get valid coordinates")


# -----------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    main()

# -----------------------------------------------------------------------------------------------------------------
