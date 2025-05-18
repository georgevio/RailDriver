import os
import ctypes
import time
import keyboard  # Import the keyboard library (install if needed: pip install keyboard)
from ctypes import c_int, c_char_p, c_float, POINTER, create_string_buffer

DLL_PATH = os.path.join(os.getcwd(), "C:\Program Files (x86)\Steam\steamapps\common\RailWorks\plugins\RailDriver64.dll")

# Load the DLL
try:
    rd_dll = ctypes.CDLL(DLL_PATH)
    print(f"Loaded DLL: {DLL_PATH}")
except OSError as e:
    print(f"Failed to load DLL: {e}")
    exit(1)

# Define argument and return types for the functions we will use
rd_dll.SetRailDriverConnected.argtypes = [c_int]
rd_dll.SetRailDriverConnected.restype = None
rd_dll.GetRailSimConnected.restype = c_int
rd_dll.GetLocoName.restype = c_char_p
rd_dll.GetControllerValue.argtypes = [c_char_p]
rd_dll.GetControllerValue.restype = c_float
rd_dll.SetControllerValue.argtypes = [c_char_p, c_float]  # Add SetControllerValue
rd_dll.SetControllerValue.restype = None

# Connect to RailDriver
try:
    rd_dll.SetRailDriverConnected(1)
    print("Connected to RailDriver.")
except Exception as e:
    print(f"Error connecting to RailDriver: {e}")

headlights_on = False
wipers_on = False

try:
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')

        is_connected = rd_dll.GetRailSimConnected()
        print(f"RailSim Connected: {bool(is_connected)}")

        loco_name_ptr = rd_dll.GetLocoName()
        loco_name = loco_name_ptr.decode('utf-8') if loco_name_ptr else "Unknown"
        print(f"Locomotive Name: {loco_name}")

        print("\nControlling Lights and Wipers:")
        print("  Press 'l' to toggle headlights.")
        print("  Press 'w' to toggle wipers.")

        if keyboard.is_pressed('l'):
            headlights_on = not headlights_on
            try:
                rd_dll.SetControllerValue(b"Headlights", 1.0 if headlights_on else 0.0)
                # To prevent rapid toggling on a single key press
                time.sleep(0.2)
            except Exception as e:
                print(f"  Error setting headlights: {e}")

        if keyboard.is_pressed('w'):
            wipers_on = not wipers_on
            try:
                rd_dll.SetControllerValue(b"Wipers", 1.0 if wipers_on else 0.0)
                # To prevent rapid toggling on a single key press
                time.sleep(0.2)
            except Exception as e:
                print(f"  Error setting wipers: {e}")

        # Get and print the current values
        try:
            headlights_value = rd_dll.GetControllerValue(b"Headlights")
            wipers_value = rd_dll.GetControllerValue(b"Wipers")
            print(f"  Headlights Value: {headlights_value} (Target: {'On' if headlights_on else 'Off'})")
            print(f"  Wipers Value: {wipers_value} (Target: {'On' if wipers_on else 'Off'})")
        except Exception as e:
            print(f"  Error getting light/wiper values: {e}")

        time.sleep(1)

except KeyboardInterrupt:
    print("\nExiting loop.")
except Exception as e:
    print(f"\nAn error occurred: {e}")
finally:
    pass