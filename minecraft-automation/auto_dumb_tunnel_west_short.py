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

# Function to build the standard eastbound rail string 
def build_tunnel_west():
    send_command(f"/fill ~-1 ~-1 ~1 ~-30 ~3 ~-2 stone")
    send_command(f"/fill ~-1 ~ ~ ~-30 ~1 ~-1 air")
    send_command(f"/tp ~-6 ~ ~")
    for x in range(1,4,1):
        send_command(f"/fill ~-1 ~-1 ~ ~-1 ~-1 ~-1 sea_lantern")
        send_command(f"/tp ~-10 ~ ~")
    send_command(f"/tp ~6 ~ ~")

# Wait for Minecraft to be in focus
while not is_minecraft_focused():
    print("Waiting for Minecraft to be in focus...")
    time.sleep(1)  # Check every second

print("Minecraft is now in focus. Pressing escape to get into playing mode.")
pyautogui.press('escape')  # Press the escape key
time.sleep(0.5)  # Give a small delay to allow for menu closing or state change

print("Starting script.")
   
# Run the function once Minecraft is focused
build_tunnel_west()



