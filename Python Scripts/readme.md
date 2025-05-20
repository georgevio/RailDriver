# RailDriver-Python-Interfaces

Those are multiple Python scripts for itneracting with the RailDriver controller and Train Simulator. They interact with the `RailDriver64.dll` (or `RailDriver.dll`) to get/set locomotive data and commands.

## Features

* **DLL Loading**: loading of the RailDriver DLL, with architecture detection for Windows (x64/x86).
* **Locomotive Data Retrieval**: Get the name of the currently driven locomotive.
* **Controller Information**:
    * Retrieve a list of available controllers.
    * Get current, minimum, and maximum values for individual controllers.
    * Dynamically determine controller IDs by their names.
* **Controller Control**: Set values for various controllers, enabling in-game actions like toggling wipers, emergency brake, horn, and setting simple direction.
* **Connection Management**: Keep the RailDriver connection alive.
* **Logging**: Centralized logging with different debug levels (ERROR, INFO, DEBUG).
* **Error Handling**: Includes mechanisms for handling DLL loading errors and failed controller retrieval attempts.

## Requirements

* **The scripts are written in Python 3.x**: 
* **Train Simulator (RailWorks)**: The game must be running and a scenario loaded for functions to work correctly.
* **`keyboard` library (import keyboard)**: Used in `set_variables_2.py`, `set_variables_basic_example.py`, and `wipers_lights.py` for keyboard input detection. Install it using pip:
    ```bash
    pip install keyboard
    ```

## Project Structure

* `all_data_printout.py`: Connects to RailDriver, retrieves the locomotive name, and lists all detected controllers with their current, min, and max values. It also attempts multiple times to get the controller list if an error occurs and saves the data to a text file.
* `full_debug.py`: Similar to `all_data_printout.py` but primarily focused on displaying controller information to the console for debugging purposes.
* `minimal.py`: A basic example demonstrating how to load the DLL, check RailSim connection, get the locomotive name, and read a specific controller value (SpeedometerMPH).
* `RailDriverData.py`: A comprehensive library containing functions to interact with the RailDriver DLL. It includes functions for getting controller lists, locomotive names, controller values, and setting controller values. It also defines additional "virtual" controllers (e.g., Latitude, Longitude, Fuel level). This script also serves as an example of logging all available data to a file, including the "virtual" controllers.
* `set_variables_2.py`: Demonstrates how to set controller values based on keyboard input. It uses `get_controller_value` to implement a state-aware toggle for Wipers, EmergencyBrake, and Horn, and allows setting values for "SimpleChangeDirection". It attempts to find controllers by name.
* `set_variables_basic_example.py`: A simpler example of setting controller values with keyboard input. It toggles Wipers, EmergencyBrake, and Horn states. It also attempts to find controllers by name.
* `wipers_lights.py`: Focuses specifically on toggling Headlights and Wipers using keyboard presses, and displays their current values. This script uses controller names directly (e.g., "Headlights", "Wipers") instead of IDs, which works for standard controllers.

## Setup and Usage

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/your-username/RailDriver-Python-Interface.git](https://github.com/your-username/RailDriver-Python-Interface.git)
    cd RailDriver-Python-Interface
    ```
2.  **Install dependencies:**
    ```bash
    pip install keyboard
    ```
3.  **Verify DLL Path:** Ensure the `DLL_NAME` (or `DLL_PATH`) variable in each script points to the correct location of your `RailDriver64.dll` (or `RailDriver.dll`). The default path is:
    `C:\Program Files (x86)\Steam\steamapps\common\RailWorks\plugins\RailDriver64.dll`.
    *Note: `RailDriverData.py` attempts to automatically select the correct DLL based on system architecture.*

4.  **Run the scripts:**
    * To get all controller data:
        ```bash
        python all_data_printout.py
        ```
    * For a detailed debug output of controllers:
        ```bash
        python full_debug.py
        ```
    * For basic locomotive and speed information:
        ```bash
        python minimal.py
        ```
    * To control wipers, emergency brake, horn, and direction using keyboard:
        ```bash
        python set_variables_2.py
        ```
        (Follow on-screen instructions for key presses: '2' for Wipers, '3' for EmergencyBrake, '4' for Horn, '5'/'6'/'7' for SimpleChangeDirection, '0' to exit).
    * For a basic example of setting variables:
        ```bash
        python set_variables_basic_example.py
        ```
        (Follow on-screen instructions for key presses: '2' for Wipers, '3' for EmergencyBrake, '4' for Horn, '0' to exit).
    * To toggle headlights and wipers:
        ```bash
        python wipers_lights.py
        ```
        (Press 'l' for headlights, 'w' for wipers).

**Important Notes:**

* Train Simulator must be running a scenario for the DLL to return data and for controls to function.
* Some functions, particularly `GetControllerList`, might require multiple attempts to retrieve data if Train Simulator is still loading or initializing. The `attempt_get_controller_list` is supposed to do this by retrying.
* The `SetRailDriverConnected(True)` call is crucial for maintaining the connection with the RailDriver DLL and ensuring continuous data flow.
* Error messages will be printed to the console if the DLL fails to load or if controllers cannot be found.

## Contributing

Feel free to open issues or pull requests if you have suggestions, improvements, or bug fixes.

---

**Disclaimer**: This project is not officially affiliated with RailDriver or Dovetail Games. It is a community-driven effort to provide a Python interface for the RailDriver DLL. It is provided as-is.