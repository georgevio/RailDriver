# VERSION: 3.0
#   SetRailDriverConnected(). As said online,it keeps the connection alive.
#   Get the controller ID by name
#   Get standard controller values, 400 - 408 are virtual controllers

import ctypes
import os
import time

# ===============================
# Global Configuration
# ===============================
# RailDriver DLL path
DLL_NAME_X64 = r"C:\Program Files (x86)\Steam\steamapps\common\RailWorks\plugins\RailDriver64.dll"
DLL_NAME_X86 = r"C:\Program Files (x86)\Steam\steamapps\common\RailWorks\plugins\RailDriver.dll"
# Set the DLL name based on the system architecture
if os.name == 'nt':  # Windows
    if os.environ['PROCESSOR_ARCHITECTURE'].endswith('64'):
        DLL_NAME = DLL_NAME_X64
    else:
        DLL_NAME = DLL_NAME_X86
else:
    print("Operating system not Windows. Please adjust DLL_NAME manually.")
    DLL_NAME = DLL_NAME_X64 # Default to x64 for non-Windows

# Load RailDriver DLL
def load_raildriver_dll(dll_name=DLL_NAME):
    """Loads the specified RailDriver DLL."""
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        dll_path = os.path.join(script_dir, dll_name)
        raildriver = ctypes.CDLL(dll_path)
        log(2, f"Successfully loaded: {dll_path}")
        time.sleep(1)  # Small delay after loading. Does it make any difference?
        return raildriver
    except OSError as e:
        log(1, f"Error loading {dll_name}: {e}")
        return None

DEBUG_LEVEL = 1  # 0: NONE, 1: ERROR, 2: INFO, 3: DEBUG
LOG_LEVELS = {
    0: "NONE",
    1: "ERROR",
    2: "INFO",
    3: "DEBUG"
}

def log(level, message):
    """Centralized logging function with level control."""
    if level <= DEBUG_LEVEL:
        log_level_name = LOG_LEVELS.get(level, "UNKNOWN")
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] [{log_level_name}] {message}")

# ===============================
# API Wrappers
# ===============================
def get_controller_list(raildriver):
    """Retrieves the controller list."""
    if not raildriver:
        log(1, f"{DLL_NAME} not loaded.")
        raise RuntimeError("DLL not loaded!")
        #return None
    try:
        GetControllerListFunc = raildriver.GetControllerList
        GetControllerListFunc.restype = ctypes.c_char_p
        GetControllerListFunc.argtypes = [] 
        controller_list_bytes = GetControllerListFunc()
        if controller_list_bytes:
            controller_list_str = controller_list_bytes.decode('utf-8')
            controllers = controller_list_str.split("::")
            log(3, f"Retrieved controller list: {controllers}")
            return controllers
        else:
            log(1, "Failed to retrieve controller list.")
            #return None
            raise RuntimeError("Failed to retrieve controller list.")
    except Exception as e:
        log(1, f"Exception in get_controller_list: {e}")
        return None

def get_loco_name(raildriver):
    """Retrieves the current locomotive name."""
    if not raildriver:
        log(1, f"{DLL_NAME} not loaded.")
        return None
    try:
        GetLocoNameFunc = raildriver.GetLocoName
        GetLocoNameFunc.restype = ctypes.c_char_p
        GetLocoNameFunc.argtypes = [] 
        loco_name_bytes = GetLocoNameFunc()
        if loco_name_bytes:
            loco_name_str = loco_name_bytes.decode('utf-8')
            log(3, f"Retrieved locomotive name: {loco_name_str}")
            return loco_name_str
        else:
            log(1, "Failed to retrieve locomotive name.")
            return None
    except Exception as e:
        log(1, f"Exception in get_loco_name: {e}")
        return None

def get_controller_value(raildriver, control_id, mode=0):
    """Retrieves the current, min, or max value of a controller."""
    if not raildriver:
        log(1, f"{DLL_NAME} not loaded")
        return None
    try:
        GetControllerValueFunc = raildriver.GetControllerValue
        GetControllerValueFunc.restype = ctypes.c_float
        GetControllerValueFunc.argtypes = [ctypes.c_int, ctypes.c_int] # controlID, Mode
        value = GetControllerValueFunc(control_id, mode)
        log(3, f"GetControllerValue(control_id={control_id}, mode={mode}) returned: {value}")
        return value
    except Exception as e:
        log(1, f"Error in get_controller_value: {e}")
        return None

def set_controller_value(raildriver, control_id, value):
    """Sets the value of a specific controller."""
    if not raildriver:
        log(1, f"{DLL_NAME} not loaded")
        return None
    try:
        SetControllerValueFunc = raildriver.SetControllerValue
        SetControllerValueFunc.restype = None # void return
        SetControllerValueFunc.argtypes = [ctypes.c_int, ctypes.c_float] # Control, Value
        SetControllerValueFunc(control_id, ctypes.c_float(value))
        log(3, f"SetControllerValue(control_id={control_id}, value={value}) called.")
    except Exception as e:
        log(1, f"Error in set_controller_value: {e}")
        return None

def get_rail_sim_loco_changed(raildriver):
    """Checks if the currently driven locomotive has changed."""
    if not raildriver:
        log(1, f"{DLL_NAME} not loaded")
        return None
    try:
        GetRailSimLocoChangedFunc = raildriver.GetRailSimLocoChanged
        GetRailSimLocoChangedFunc.restype = ctypes.c_bool
        GetRailSimLocoChangedFunc.argtypes = [] 
        changed = GetRailSimLocoChangedFunc()
        log(3, f"GetRailSimLocoChanged() returned: {changed}")
        return changed
    except Exception as e:
        log(1, f"Error in get_rail_sim_loco_changed: {e}")
        return None

def set_rail_driver_connected(raildriver, value):
    """Keeps the RailDriver connection open."""
    if not raildriver:
        log(1, f"{DLL_NAME} not loaded")
        return None
    try:
        SetRailDriverConnectedFunc = raildriver.SetRailDriverConnected
        SetRailDriverConnectedFunc.restype = None # void return 
        SetRailDriverConnectedFunc.argtypes = [ctypes.c_bool] 
        SetRailDriverConnectedFunc(ctypes.c_bool(value))
        log(3, f"SetRailDriverConnected({value}) called.")
    except Exception as e:
        log(1, f"Error in set_rail_driver_connected: {e}")
        return None

# trying to debug the controller retrieval errors! Not sure if it makes any difference
def attempt_get_controller_list(raildriver, max_attempts=3, delay=2):
    for attempt in range(max_attempts):
        try:
            controllers = get_controller_list(raildriver)
            return controllers
        except RuntimeError as e:
            print(f"[WARNING] Attempt {attempt + 1} to get controller list failed: {e}")
            if attempt < max_attempts - 1:
                time.sleep(delay)
            else:
                raise  

# =============
# Main Script
# =============
if __name__ == "__main__":
    raildriver_lib = load_raildriver_dll()  # central DLL_NAME

    if raildriver_lib:
        loco_name = get_loco_name(raildriver_lib)
        if loco_name:
            detailed_time = time.strftime("%Y-%m-%d %H:%M:%S")
            compact_date = time.strftime("%Y%m%d")
            # Replace invalid characters in the locomotive name with underscores
            safe_loco_name = loco_name.replace(':', '_').replace('.', '')
            filename = f"{compact_date}_{safe_loco_name}.txt"

            with open(filename, "w") as outfile:
                outfile.write(f"{detailed_time}\n")
                outfile.write(f"Locomotive Name: {loco_name}\n")
                outfile.write("-" * 40 + "\n")

                log(2, f"Currently driven locomotive: {loco_name}")

                controllers = attempt_get_controller_list(raildriver_lib)
                if controllers:
                    log(2, "\nDetected Controllers and Values:")
                    log(2, "-" * 40)
                    outfile.write("Detected Controllers and Values:\n")
                    outfile.write("-" * 40 + "\n")
                    for index, controller_name in enumerate(controllers):
                        current_value = get_controller_value(raildriver_lib, index, 0)
                        min_value = get_controller_value(raildriver_lib, index, 1)
                        max_value = get_controller_value(raildriver_lib, index, 2)

                        output = f"[{index:02d}] {controller_name}: "
                        if min_value == 0.0 and max_value == 1.0 and current_value is not None:
                            status = "ON" if current_value > 0.5 else "OFF"
                            output += f"(BOOLEAN): {status} "
                        elif current_value is not None and min_value is not None and max_value is not None:
                            output += f": {current_value:.2f}, Min/Max: [{min_value:.2f}, {max_value:.2f}]"
                        else:
                            output += "Could not retrieve all values."
                        print(output)  # console output
                        outfile.write(output + "\n")
                    outfile.write("-" * 40 + "\n")

                    # Added the extra "virtual" controllers to the printout
                    outfile.write("\nAdditional RailDriver Controllers:\n")
                    outfile.write("-" * 40 + "\n")
                    virtual_controllers = {
                        400: "Latitude",
                        401: "Longitude",
                        402: "Fuel level",
                        403: "Is in tunnel?",
                        404: "Gradient",
                        405: "Heading",
                        406: "Time: hours",
                        407: "Time: minutes",
                        408: "Time: seconds",
                    }
                    for control_id, description in virtual_controllers.items():
                        current_value = get_controller_value(raildriver_lib, control_id, 0)
                        output = f"[{control_id:03d}] {description}: "
                        if current_value is not None:
                            output += f"{current_value:.2f}"
                        else:
                            output += "Could not retrieve value."
                        print(output)
                        outfile.write(output + "\n")
                    outfile.write("-" * 40 + "\n")

                else:
                    log(1, f"No controller list. Is Train Simulator running a scenario?")
                    outfile.write("No controller list found.\n")

            print(f"\nData written to: {filename}")

        else:
            print("No Locomotive Name retrieved")
            log(1, f"No locomotive name. Is Train Simulator running a scenario?")
    else:
        log(1, f"Failed to load {DLL_NAME}. Exiting.")