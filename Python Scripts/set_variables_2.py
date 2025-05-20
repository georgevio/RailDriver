# VERSION: 2.1 with state-aware toggle with get_controller_value()

import ctypes
import os
import time
import keyboard  # Requires `pip install keyboard`
import sys  # sys module for explicit exiting

# RailDriver DLL path
DLL_NAME = r"C:\Program Files (x86)\Steam\steamapps\common\RailWorks\plugins\RailDriver64.dlcl"

# Load RailDriver DLL
def load_raildriver_dll(dll_name=DLL_NAME):
    try:
        raildriver = ctypes.CDLL(dll_name)
        print(f"[INFO] loaded RailDriver(64).dll")
        time.sleep(1)  # Testing if it stops the loading error
        return raildriver
    except OSError as e:
        raise RuntimeError(f"Error loading {dll_name}: {e}. Ending...")


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

def get_controller_value(raildriver, control_id):
    """Retrieves the current value of a controller (mode 0)."""
    if not raildriver:
        print(f"[ERROR] get_controller_value.")
        #return None
        raise RuntimeError("[ERROR] get_controller_value.")
    try:
        GetControllerValue = raildriver.GetControllerValue
        GetControllerValue.restype = ctypes.c_float
        value = GetControllerValue(control_id, 0)
        return value
    except Exception as e:
        print(f"[ERROR] Error in get_controller_value, ID {control_id}: {e}")
        return None

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
    "SimpleChangeDirection": None,
}

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

    print("\nPress:")
    print("'2' to toggle Wipers, '3' for EmergencyBrake, '4' for Horn.")
    print("'5' or '6' or '7' to play with SimpleChangeDirection")
    print("'0' to exit.")

    while True:
        if raildriver_lib:
            try:
                SetRailDriverConnected(True)
            except Exception as e:
                print(f"[ERROR] SetRailDriverConnected: {e}")

        # check the status of the controls and toggle accordingly
        def toggle_control(control_name, control_id, on_value=1.0, off_value=0.0, threshold=0.5):
            if control_id is not None:
                current_value = get_controller_value(raildriver_lib, control_id)
                if current_value is not None:
                    new_value = off_value if current_value > threshold else on_value
                    set_controller_value(raildriver_lib, control_id, new_value)
                    print(f"{control_name}: {'ON' if new_value > threshold else 'OFF'} ({new_value:.2f})")

        if keyboard.is_pressed("2"):
            if controls.get("Wipers") is not None:
                current_value = get_controller_value(raildriver_lib, controls["Wipers"])
                if current_value is not None:
                    new_value = 1.0 if current_value < 0.5 else 0.0
                    set_controller_value(raildriver_lib, controls["Wipers"], new_value)
                    print(f"Wipers: {'ON' if new_value > 0.5 else 'OFF'} ({new_value:.2f}), Current Value: {get_controller_value(raildriver_lib, controls['Wipers']):.2f}")
                else:
                    print("[WARNING] Could not read current Wipers value.")
            time.sleep(0.3)

        if keyboard.is_pressed("3"):
            if controls.get("EmergencyBrake") is not None:
                current_value = get_controller_value(raildriver_lib, controls["EmergencyBrake"])
                if current_value is not None:
                    new_value = 1.0 if current_value < 0.5 else 0.0
                    set_controller_value(raildriver_lib, controls["EmergencyBrake"], new_value)
                    print(f"EmergencyBrake: {'ON' if new_value > 0.5 else 'OFF'} ({new_value:.2f}), Current Value: {get_controller_value(raildriver_lib, controls['EmergencyBrake']):.2f}")
                else:
                    print("[WARNING] Could not read current EmergencyBrake value.")
            time.sleep(0.3)

        if keyboard.is_pressed("4"):
            if controls.get("Horn") is not None:
                current_value = get_controller_value(raildriver_lib, controls["Horn"])
                if current_value is not None:
                    new_value = 1.0 if current_value < 0.1 else 0.0 
                    set_controller_value(raildriver_lib, controls["Horn"], new_value)
                    print(f"Horn: {'ON' if new_value > 0.1 else 'OFF'} ({new_value:.2f}), Current Value: {get_controller_value(raildriver_lib, controls['Horn']):.2f}")
                else:
                    print("[WARNING] Could not read current Horn value.")
            time.sleep(0.3)

        if keyboard.is_pressed("5"): # # value = (-1)
            if controls.get("SimpleChangeDirection") is not None:
                target_value = -1.0
                set_controller_value(raildriver_lib, controls["SimpleChangeDirection"], target_value)
                current_value = get_controller_value(raildriver_lib, controls["SimpleChangeDirection"])
                if current_value is not None:
                    print(f"SimpleChangeDirection: Set to {target_value:.1f}, Active Value: {current_value:.1f}")
                else:
                    print(f"[WARNING] SimpleChangeDirection: Set to {target_value:.1f}, cannot read value.")
            time.sleep(0.3)

        if keyboard.is_pressed("6"): # value = (0)
            if controls.get("SimpleChangeDirection") is not None:
                target_value = 0.0
                set_controller_value(raildriver_lib, controls["SimpleChangeDirection"], target_value)
                current_value = get_controller_value(raildriver_lib, controls["SimpleChangeDirection"])
                if current_value is not None:
                    print(f"SimpleChangeDirection: Set to {target_value:.1f}, Active Value: {current_value:.1f}")
                else:
                    print(f"[WARNING] SimpleChangeDirection: Set to {target_value:.1f}, cannot read value.")
            time.sleep(0.3)

        if keyboard.is_pressed("7"): # value = (1)
            if controls.get("SimpleChangeDirection") is not None:
                target_value = 1.0
                set_controller_value(raildriver_lib, controls["SimpleChangeDirection"], target_value)
                current_value = get_controller_value(raildriver_lib, controls["SimpleChangeDirection"])
                if current_value is not None:
                    print(f"SimpleChangeDirection: Set to {target_value:.1f}, Active Value: {current_value:.1f}")
                else:
                    print(f"[WARNING] SimpleChangeDirection: Set to {target_value:.1f}, cannot read value..")
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