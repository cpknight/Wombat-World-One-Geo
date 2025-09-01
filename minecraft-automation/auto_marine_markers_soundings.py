#!/usr/bin/env python3

import pyautogui
import time
from Xlib import display
from qgis.core import QgsVectorLayer
import os

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

def is_minecraft_focused():
    d = display.Display()
    root = d.screen().root
    window_name = root.get_full_property(d.intern_atom('_NET_ACTIVE_WINDOW'), 0).value[0]
    window = d.create_resource_object('window', window_name)
    title = window.get_full_property(d.intern_atom('_NET_WM_NAME'), 0).value
    
    if isinstance(title, bytes):
        title = title.decode('utf-8')
    
    return "Minecraft" in title if title else False

# -----------------------------------------------------------------------------------------------------------------
# SEND COMMAND TO MINECRAFT FUNCTION
# -----------------------------------------------------------------------------------------------------------------

def send_command(command):
    pyautogui.press('/')
    for increment in range(10):
        pyautogui.press('backspace')
    for char in command:
        pyautogui.press(char)
    pyautogui.press('enter')
    micro_delay(0.1)

# -----------------------------------------------------------------------------------------------------------------
# READ SHAPEFILE FUNCTION
# -----------------------------------------------------------------------------------------------------------------

def read_shapefile(file_path):
    if not os.path.exists(file_path):
        print(f"Error: Shapefile {file_path} not found")
        return None
    layer = QgsVectorLayer(file_path, "waterway_markers", "ogr")
    if not layer.isValid():
        print(f"Error: Invalid shapefile {file_path}")
        return None
    # Check if 'Y' field exists, add if not
    if layer.fields().indexFromName("Y") == -1:
        from qgis.core import QgsField
        from PyQt5.QtCore import QVariant
        layer.startEditing()
        layer.addAttribute(QgsField("Y", QVariant.Double))
        layer.commitChanges()
    coordinates = []
    for feature in layer.getFeatures():
        geom = feature.geometry()
        if geom and geom.isMultipart():
            point = geom.asMultiPoint()[0]
        else:
            point = geom.asPoint()
        x = float(point.x())
        z = -float(point.y())  # Reverse Y to match Minecraft Z due to CRS
        coordinates.append((x, z, feature.id()))
    return layer, coordinates

# -----------------------------------------------------------------------------------------------------------------
# MAIN FOR SOUNDING
# -----------------------------------------------------------------------------------------------------------------

def main():
    # Path to shapefile, relative to <Project>/minecraft-automation/
    shapefile_path = os.path.join("..", "qgis", "waterway-markers-proposed.shp")
    layer, coords_list = read_shapefile(shapefile_path)
    
    if not coords_list:
        print("Failed to load coordinates from shapefile")
        return

    # Wait for Minecraft to be in focus
    while not is_minecraft_focused():
        print("Waiting for Minecraft to be in focus...")
        time.sleep(1)

    print("Minecraft is now in focus. Pressing escape to get into playing mode.")
    pyautogui.press('escape')
    time.sleep(0.5)

    print("Starting sounding process. Visit each location, find sea floor, and input Y coordinate.")

    for i, (x, z, fid) in enumerate(coords_list, 1):
        print(f"Teleporting to marker {i}/{len(coords_list)} at X={x}, Z={z}")
        send_command(f"/tp {x} 75 {z}")
        time.sleep(2.0)  # Give time to teleport and for you to find sea floor
        try:
            y = float(input(f"Enter sea floor Y coordinate for X={x}, Z={z}: "))
            # Update shapefile with Y coordinate
            layer.startEditing()
            layer.changeAttributeValue(fid, layer.fields().indexFromName("Y"), y)
            layer.commitChanges()
            print(f"Saved Y={y} for marker at X={x}, Z={z}")
        except ValueError:
            print(f"Invalid Y input, skipping marker at X={x}, Z={z}")
        time.sleep(1.0)  # Delay between teleports

if __name__ == "__main__":
    main()
