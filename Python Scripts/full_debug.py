import ctypes
import os
import time

# ===============================
# Global Configuration
# ===============================
DLL_NAME = r"C:\Program Files (x86)\Steam\steamapps\common\RailWorks\plugins\RailDriver64.dll"  # Corrected path using raw string
# Load RailDriver DLL
def load_raildriver_dll(dll_name=DLL_NAME):
    try:
        raildriver = ctypes.CDLL(dll_name)
        time.sleep(1)  # Small delay after loading
        return raildriver
    except OSError as e:
        print(f"Error loading {dll_name}: {e}")
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
# DLL Loading
# ===============================
def load_raildriver_dll(dll_name=DLL_NAME):
    """Loads the specified RailDriver DLL."""
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        dll_path = os.path.join(script_dir, dll_name)
        raildriver = ctypes.CDLL(dll_path)
        log(2, f"Successfully loaded: {dll_path}")
        time.sleep(1)  # Small delay after loading
        return raildriver
    except OSError as e:
        log(1, f"Error loading {dll_name}: {e}")
        return None

# ===============================
# API Function Wrappers
# ===============================
def get_controller_list(raildriver):
    """Retrieves the controller list."""
    if not raildriver:
        log(1, f"{DLL_NAME} not loaded.")
        return None
    try:
        GetControllerList = raildriver.GetControllerList
        GetControllerList.restype = ctypes.c_char_p
        controller_list_bytes = GetControllerList()
        if controller_list_bytes:
            controller_list_str = controller_list_bytes.decode('utf-8')
            controllers = controller_list_str.split("::")
            log(3, f"Retrieved controller list: {controllers}")
            return controllers
        else:
            log(1, "Failed to retrieve controller list.")
            return None
    except Exception as e:
        log(1, f"Exception in get_controller_list: {e}")
        return None

def get_loco_name(raildriver):
    """Retrieves the current locomotive name."""
    if not raildriver:
        log(1, f"{DLL_NAME} not loaded.")
        return None
    try:
        GetLocoName = raildriver.GetLocoName
        GetLocoName.restype = ctypes.c_char_p
        loco_name_bytes = GetLocoName()
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
        GetControllerValue = raildriver.GetControllerValue
        GetControllerValue.restype = ctypes.c_float
        value = GetControllerValue(control_id, mode)
        log(3, f"GetControllerValue(control_id={control_id}, mode={mode}) returned: {value}")
        return value
    except Exception as e:
        log(1, f"Error in get_controller_value: {e}")
        return None

# ===============================
# Main Script Logic
# ===============================
if __name__ == "__main__":
    raildriver_lib = load_raildriver_dll()  # Uses the global DLL_NAME

    if raildriver_lib:
        loco_name = get_loco_name(raildriver_lib)
        if loco_name:
            log(2, f"Currently driven locomotive: {loco_name}")
        else:
            log(1, f"Could not retrieve locomotive name. Is Train Simulator running AND are you in a driving session?")

        controllers = get_controller_list(raildriver_lib)
        if controllers:
            log(2, "\nDetected Controllers and Values:")
            log(2, "-" * 60)
            for index, controller_name in enumerate(controllers):
                current_value = get_controller_value(raildriver_lib, index, 0)
                min_value = get_controller_value(raildriver_lib, index, 1)
                max_value = get_controller_value(raildriver_lib, index, 2)

                print(f"[{index:02d}] {controller_name}:")
                print(f"      Current Value: {current_value}")
                if min_value is not None and max_value is not None:
                    print(f"      Min Value:     {min_value}")
                    print(f"      Max Value:     {max_value}")
                print("-" * 60)
        else:
            log(1, f"Could not retrieve controller list. Is Train Simulator running AND are you in a driving session?")
    else:
        log(1, f"Failed to load {DLL_NAME}. Exiting.")