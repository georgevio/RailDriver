# VERSION: 2.0 with SetRailDriverConnected(). As said online,it keeps the connection alive.
import ctypes
import os
import time
import keyboard  # Requires `pip install keyboard`
import sys  # Import the sys module for explicit exiting

# RailDriver DLL path
DLL_NAME = r"C:\Program Files (x86)\Steam\steamapps\common\RailWorks\plugins\RailDriver64.dll"

# Load RailDriver DLL
def load_raildriver_dll(dll_name=DLL_NAME):
    try:
        raildriver = ctypes.CDLL(dll_name)
        print(f"[INFO] loaded RailDriver(64).dll")
        time.sleep(1)  # Small delay after loading
        return raildriver
    except OSError as e:
        raise RuntimeError(f"Error loading {dll_name}: {e}. Ending...")

# Set controller values
def set_controller_value(raildriver, control_id, value):
    if raildriver:
        try:
            raildriver.SetControllerValue(control_id, ctypes.c_float(value))
        except Exception as e:
            print(f"Error setting controller {control_id}: {e}")

def get_controller_list(raildriver):
    """Retrieves the controller list."""
    if not raildriver:
        raise RuntimeError("No RailDriver DLL.")
    try:
        GetControllerList = raildriver.GetControllerList
        GetControllerList.restype = ctypes.c_char_p
        controller_list_bytes = GetControllerList()
        if not controller_list_bytes:
            raise RuntimeError("Failed to turn controller to bytes.")
        controller_list_str = controller_list_bytes.decode('utf-8')
        controllers = controller_list_str.split("::")
        print("Successfully retrieved controller list.")
        return controllers
    except Exception as e:
        raise RuntimeError(f"Failed controller list: {e}")

def get_controller_id_by_name(raildriver, target_names):
    """
    Retrieves controller IDs based on target names.

    Args:
        raildriver: The loaded RailDriver from DLL.
        target_names: Dict with control names to search for.

    Returns:
        A dict with keys as target_names, values as controller IDs (None if not found).
    """
    if not raildriver:
        return {name: None for name in target_names}
    try:
        controllers = get_controller_list(raildriver)
        found_controls = {name: None for name in target_names}
        for i, controller_name in enumerate(controllers):
            for target_name in target_names:
                if target_name in controller_name:
                    found_controls[target_name] = i
                    print(f"Found {target_name} at ID: {i}, Name: {controller_name}")
                    break
        return found_controls
    except RuntimeError as e:
        raise  # Propagate the critical error
    except Exception as e:
        print(f"Error in get_controller_id_by_name: {e}")
        return {name: None for name in target_names}

# Define controls to find.
controls_to_find = {
    "Wipers": None,
    "EmergencyBrake": None,
    "Horn": None,
}

# Initialize controller states
controller_states = {control: 0.0 for control in controls_to_find}

raildriver_lib = load_raildriver_dll()

if raildriver_lib:
    try:
        SetRailDriverConnected = raildriver_lib.SetRailDriverConnected
        SetRailDriverConnected.argtypes = [ctypes.c_bool]
        SetRailDriverConnected.restype = None
    except AttributeError as e:
        print(f"[ERROR] Could not find SetRailDriverConnected function in RailDriver64.dll: {e}")
        sys.exit(1)

try:
    if not raildriver_lib:
        raise RuntimeError("RailDriver DLL not loaded. Aborting...")

    # Initially try to establish the connection
    if raildriver_lib:
        try:
            SetRailDriverConnected(True)
        except Exception as e:
            print(f"[WARNING] Error calling SetRailDriverConnected initially: {e}")

    # Get the controller IDs
    controls = get_controller_id_by_name(raildriver_lib, controls_to_find)

    # Check if all required controls were found
    if not all(value is not None for value in controls.values()):
        print("[ERROR]: Not all required controls found:")
        for control_name, control_id in controls.items():
            print(f"    {control_name}: {control_id}")
        raise RuntimeError("Not all required controls found :(")

    print("\nControls Found:")
    for control_name, control_id in controls.items():
        print(f"{control_name}: {control_id}")

    print("\nPress '2' to toggle Wipers, '3' for EmergencyBrake, '4' for Horn.")
    print("Press '0' to exit.")

    while True:
        if raildriver_lib:
            try:
                SetRailDriverConnected(True)
            except Exception as e:
                print(f"[WARNING] Error calling SetRailDriverConnected in loop: {e}")

        if keyboard.is_pressed("2"):
            if controls.get("Wipers") is not None:
                controller_states["Wipers"] = 1.0 if controller_states["Wipers"] == 0.0 else 0.0
                set_controller_value(raildriver_lib, controls["Wipers"], controller_states["Wipers"])
                print(f"Wipers: {controller_states['Wipers']}")
            time.sleep(0.3)

        if keyboard.is_pressed("3"):
            if controls.get("EmergencyBrake") is not None:
                controller_states["EmergencyBrake"] = 1.0 if controller_states["EmergencyBrake"] == 0.0 else 0.0
                set_controller_value(raildriver_lib, controls["EmergencyBrake"], controller_states["EmergencyBrake"])
                print(f"EmergencyBrake: {controller_states['EmergencyBrake']}")
            time.sleep(0.3)

        if keyboard.is_pressed("4"):
            if controls.get("Horn") is not None:
                controller_states["Horn"] = 1.0 if controller_states["Horn"] == 0.0 else 0.0
                set_controller_value(raildriver_lib, controls["Horn"], controller_states["Horn"])
                print(f"Horn: {controller_states['Horn']}")
            time.sleep(0.3)

        if keyboard.is_pressed("0"):  # Exit condition
            print("\"0\" pressed, exit program...")
            break

        time.sleep(0.05) # Small delay to avoid busy-waiting

except RuntimeError as e:
    print(f"[ERROR]: {e}")
    sys.exit(1)
except Exception as e:
    print(f"[ERROR]: {e}")
    sys.exit(1)