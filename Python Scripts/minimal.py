import os
import ctypes
from ctypes import c_int, c_char_p, c_float, POINTER

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

# Connect to RailDriver
try:
    rd_dll.SetRailDriverConnected(1)
    print("Connected to RailDriver.")
except Exception as e:
    print(f"Error connecting to RailDriver: {e}")

# Check RailSim connection status
try:
    is_connected = rd_dll.GetRailSimConnected()
    print(f"RailSim Connected: {bool(is_connected)}")
except Exception as e:
    print(f"Error checking RailSim connection: {e}")

# Get Locomotive Name
try:
    loco_name_ptr = rd_dll.GetLocoName()
    loco_name = loco_name_ptr.decode('utf-8') if loco_name_ptr else "Unknown"
    print(f"Locomotive Name: {loco_name}")
except Exception as e:
    print(f"Error getting locomotive name: {e}")

# Get Speed
try:
    speed = rd_dll.GetControllerValue(b"SpeedometerMPH")
    print(f"Speed: {speed} MPH")
except Exception as e:
    print(f"Error getting speed: {e}")
