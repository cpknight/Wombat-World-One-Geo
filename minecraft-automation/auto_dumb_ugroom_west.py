#!/usr/bin/env python3

import pyautogui
import time
from Xlib import display

def micro_delay(duration):
    start = time.perf_counter()
    while time.perf_counter() - start < duration:
       pass


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
    for increment in range (10):
        pyautogui.press('backspace')
    for char in command:
        pyautogui.press(char)
    pyautogui.press('enter')  # Send command
    micro_delay(0.1)  # Short delay for command execution

# Function to build the standard underground room (westbound)
# Assumes starting point is in tunnel, at left edge of room

def build_underground_room_west():
    send_command(f"/fill ~-1 ~-9 ~1 ~-9 ~4 ~-9 stone")   # external shell
    send_command(f"/fill ~-2 ~-8 ~ ~-8 ~2 ~-8 air")      # empty internal space
    send_command(f"/fill ~-1 ~-1 ~1 ~-9 ~-1 ~-9 stone")  # floor -0
    send_command(f"/fill ~-1 ~-5 ~1 ~-9 ~-5 ~-9 stone")  # floor -1
    send_command(f"/setblock ~-1 ~ ~-5 iron_door[facing=west,half=lower]")    # door
    send_command(f"/setblock ~-1 ~1 ~-5 iron_door[facing=west,half=upper]")   # door
    # send_command(f"/setblock ~ ~1 ~-4 stone_button[face=wall,facing=west]")
    # send_command(f"/setblock ~ ~1 ~-6 pale_oak_wall_sign[facing=west]")

   #for x in range(1,4,1):
    #    send_command(f"/fill ~-1 ~-1 ~ ~-1 ~-1 ~-1 sea_lantern")
    #    send_command(f"/tp ~-10 ~ ~")
    #send_command(f"/tp ~6 ~ ~")

# Wait for Minecraft to be in focus
while not is_minecraft_focused():
    print("Waiting for Minecraft to be in focus...")
    time.sleep(1)  # Check every second

print("Minecraft is now in focus. Pressing escape to get into playing mode.")
pyautogui.press('escape')  # Press the escape key
time.sleep(0.5)  # Give a small delay to allow for menu closing or state change

print("Starting script.")
   
# Run the function once Minecraft is focused
build_underground_room_west()



