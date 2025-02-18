#!/usr/bin/env python3

import pyautogui
import time
from Xlib import display

# Define keys
block_place = 'shift'
move_forward = 'w'
escape_key = 'esc'


def micro_delay(duration):
    start = time.perf_counter()
    while time.perf_counter() - start < duration:
       pass


# Function to lay rail or dig tunnel
def lay_rail_or_dig(length):
    for loop in range(length):
        print(f"Cycle: {loop}")
        pyautogui.click(button='left')
        pyautogui.keyDown(move_forward)
        time.sleep(0.25)
        pyautogui.keyUp(move_forward)
        time.sleep(0.5)  # Adjust for speed
    # Ensure keys are released at the end of the script
    pyautogui.keyUp(move_forward)

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

# Function to type and send a command to Minecraft chat
def send_command(command):
    pyautogui.press('/')
    # micro_delay(0.01)
    for increment in range (10):
        pyautogui.press('backspace')
        # micro_delay(0.01)
    #pyautogui.press('enter')
    #micro_delay(0.01)
    #pyautogui.press('/')
    #micro_delay(0.01)
    #for increment in range (3):
    #    pyautogui.press('backspace')
    #    # micro_delay(0.01)
    for char in command:
        pyautogui.press(char)
        # micro_delay(0.01)        
    # micro_delay(0.1)
    pyautogui.press('enter')  # Send command
    micro_delay(0.01)  # Short delay for command execution

# Function to build the path and grass borders
def build_path_and_grass(length):
    for i in range(length):
        # Place path blocks 
        for y in range(2):
            send_command(f"/setblock ~{y} ~ ~-{i} path\t")
        
        # Place grass blocks on either side of the path
        for y in range(2):
            send_command(f"/setblock ~-1 ~ ~-{i} grass\t")
            send_command(f"/setblock ~2 ~ ~-{i} grass\t")


# Wait for Minecraft to be in focus
while not is_minecraft_focused():
    print("Waiting for Minecraft to be in focus...")
    time.sleep(1)  # Check every second

print("Minecraft is now in focus. Pressing escape to get into playing mode.")
pyautogui.press(escape_key)  # Press the escape key
time.sleep(0.5)  # Give a small delay to allow for menu closing or state change

print("Starting script.")
   
# Run the function once Minecraft is focused
# lay_rail_or_dig(100)  # Example for 100 blocks
build_path_and_grass(10)



