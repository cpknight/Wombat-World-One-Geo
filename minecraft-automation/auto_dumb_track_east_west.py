#!/usr/bin/env python3

import pyautogui
import time
import sys
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

# Function to build the standard westbound rail string 
def build_rail_string_west():                               # makes 20 block + landing spot...
    # print("Building next section of westbound track...")
    send_command("/fill ~ ~-1 ~ ~-19 ~-1 ~ stone")         # clear the pathway ahead
    send_command("/setblock ~ ~-1 ~ redstone_block")       # add the redstone block
    send_command("/setblock ~ ~ ~ detector_rail[shape=east_west]")           # add the detector rail
    send_command(f"/fill ~-1 ~ ~ ~-3 ~ ~ powered_rail[shape=east_west]")     # add 3 powered rails
    send_command("/fill ~-4 ~ ~ ~-19 ~ ~ rail[shape=east_west]")             # add 15 rails
    send_command("/fill ~-20 ~ ~ ~-20 ~1 ~ air")            # clear new spot
    send_command("/setblock ~-20 ~-1 ~ stone")              # make a new landing spot
    send_command("/tp ~-20 ~ ~")                            # move to new spot


# Function to build the standard eastbound rail string 
def build_rail_string_east():                               # makes 20 block + landing spot...
    # print("Building next section of eastbound track...")
    send_command(f"/fill ~ ~-1 ~ ~19 ~-1 ~ stone")          # clear the pathway ahead
    send_command(f"/setblock ~ ~-1 ~ redstone_block")       # add the redstone block
    send_command(f"/setblock ~ ~ ~ detector_rail[shape=east_west]")          # add the detector rail
    send_command(f"/fill ~1 ~ ~ ~3 ~ ~ powered_rail[shape=east_west]")       # add 3 powered rails
    send_command(f"/fill ~4 ~ ~ ~19 ~ ~ rail[shape=east_west]")              # add 15 rails
    send_command("/fill ~20 ~ ~ ~20 ~1 ~ air")              # clear new spot
    send_command("/setblock ~20 ~-1 ~ stone")               # make a new landing spot
    send_command("/tp ~20 ~ ~")                             # move to new spot


def main_effort():
    # Prompt for direction
    direction = input("Enter 'e' for east or 'w' for west: ").lower()
    while direction not in ['e', 'w']:
        direction = input("Please enter 'e' or 'w': ").lower()

    # Prompt for distance
    try:
        distance = int(input("Enter the distance: "))
        if distance < 0:
            raise ValueError("Distance must be non-negative.")
    except ValueError:
        print("Invalid input for distance. Please enter a positive integer.")
        return

    get_focus()

    # Determine function based on direction
    if direction == 'e':
        build_func = build_rail_string_east
    else:
        build_func = build_rail_string_west

    # Total distance in units of 20 for progress calculation
    total_distance = distance
    iterations = distance // 20
    remainder = distance % 20

    # Progress bar
    bar_length = 50
    for i in range(iterations):
        progress = i / iterations
        bar = '#' * int(bar_length * progress) + '-' * (bar_length - int(bar_length * progress))
        sys.stdout.write(f'\rProgress: [{bar}] {int(100 * progress)}%')
        sys.stdout.flush()
        build_func() 

    if remainder > 0:
        # One more progress update for the remainder
        progress = 1.0  # Since we've completed all full iterations, we're at 100%
        bar = '#' * bar_length
        sys.stdout.write(f'\rProgress: [{bar}] {int(100 * progress)}%')
        sys.stdout.flush()
        # print(f"\nBuilding rail string to the {direction} for {remainder} units.")

    # Final newline for clean output
    print()


def get_focus():    # Wait for Minecraft to be in focus
    while not is_minecraft_focused():
        print("Waiting for Minecraft to be in focus...")
        time.sleep(1)  # Check every second

    print("Minecraft is now in focus. Pressing escape to get into playing mode.")
    pyautogui.press('escape')  # Press the escape key
    time.sleep(0.5)  # Give a small delay to allow for menu closing or state change


main_effort()

