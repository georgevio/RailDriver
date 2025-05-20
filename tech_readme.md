# Controlling Train Simulator Classic with Code

This document provides a guide to get you started with programmatically controlling Train Simulator Classic.

## 1. Understanding the Landscape

* **The Challenge**: Train Simulator Classic wasn't originally designed for easy, external programmatic control. We're primarily interacting with an interface intended for hardware controllers (like the RailDriver).
* **Key Components**:
    * `raildriver.dll`: This is the core library that enables interaction with the simulator. Your code will need to interface with this DLL.
    * **External Interface API**: The functions within `raildriver.dll` constitute the API we'll be using.
    * **RailSim Remote (Alternative)**: A separate project that wraps this API in a more web-friendly interface.

## 2. Choosing Your Approach

You have two main ways to proceed:

### 2.1 Direct DLL Interaction

* **Pros**: More direct control, potentially lower latency.
* **Cons**: More complex setup, requires language-specific knowledge of DLL handling (e.g., `LoadLibrary` in C/C++, `ctypes` in Python).

### 2.2 Using RailSim Remote

* **Pros**: Simpler communication (using HTTP), language-agnostic (any language that can send HTcommunitiesTP requests can be used).
* **Cons**: Adds a dependency (RailSim Remote needs to be running), potentially higher latency.

## 3. "Hello World" Equivalents

Here's how we can achieve basic interaction, the equivalent of a "hello world" program, for each approach.

### 3.1 Direct DLL Interaction ("Hello World" Equivalent)

This example outlines the steps conceptually. You'll need to adapt it to your chosen programming language. Below is a conceptual C++ example, often used for system-level interaction, but the principles apply to other languages.

#### 3.1.1 Conceptual C++ Example

```
cpp
#include <iostream>
//  Include appropriate headers for DLL loading (e.g., Windows.h for Windows)
#ifdef _WIN32
 #include <windows.h>
#else
 #include <dlfcn.h>
 #define HMODULE void*
 #define GetProcAddress dlsym
 #define LoadLibrary(lib) dlopen(lib, RTLD_LAZY)
 #define FreeLibrary(handle) dlclose(handle)
#endif
#include <cstring> // For strdup

int main() {
    //  1. Load the raildriver.dll
    HMODULE hModule = LoadLibrary("raildriver.dll"); // Windows-specific
    if (hModule == NULL) {
        std::cerr << "Failed to load raildriver.dll" << std::endl;
        return 1;
    }

    //  2. Get function pointers for the API functions we want to use
    typedef char* (*GetLocoNameFunc)();
    GetLocoNameFunc getLocoName = (GetLocoNameFunc)GetProcAddress(hModule, "GetLocoName");
    if (getLocoName == NULL) {
        std::cerr << "Failed to get GetLocoName function" << std::endl;
        FreeLibrary(hModule);
        return 1;
    }

    //  3. Call the function
    char* locoName = getLocoName();
    if (locoName != NULL)
    {
        std::cout << "Locomotive Name: " << locoName << std::endl;
        //IMPORTANT: You might need to free the memory allocated by the DLL
        // In C++, if the DLL allocates memory, you MUST use the DLL to free it.
        //There might be a function in the raildriver.dll like FreeMemory()
        // strdup() is used to make a copy.  You must free locoNameCopy.
        char* locoNameCopy = strdup(locoName);
        std::cout << "Locomotive Name (copy): " << locoNameCopy << std::endl;
        free(locoNameCopy);

    }
    else
        std::cout << "Locomotive Name: NULL" << std::endl;


    //  4. Free the DLL
    FreeLibrary(hModule); // Windows-specific
    return 0;
}
```

Explanation:

Load the DLL: The code loads raildriver.dll into the process's memory. The exact method is OS-specific (using platform directives for Windows and other systems).
Get Function Pointers: It retrieves the memory addresses of the API functions (like GetLocoName) that you want to call.
Call the Function: The code calls the GetLocoName function to get the name of the currently driven locomotive.
Handle the Result: The code then prints the locomotive name to the console. It also demonstrates how to handle memory that might be allocated by the DLL.
Free the DLL: The code unloads the DLL.
3.2 Using RailSim Remote ("Hello World" Equivalent)
This approach is generally simpler.

### 3.2.1 Python Example (One of the many in the folder)

```
import requests

#  1. Ensure RailSim Remote is running
#  (You'll need to download and start it separately)

#  2. Send an HTTP GET request to get the locomotive name
try:
    response = requests.get("http://localhost:8080/api/railworks/loco")  #  Default port is 8080
    response.raise_for_status()  #  Raise an exception for bad status codes (4xx or 5xx)
    data = response.json()
    print(f"Locomotive Name: {data['provider']} : {data['product']} : {data['name']}")
except requests.exceptions.RequestException as e:
    print(f"Error: {e}")
```

** Explanation: **

Ensure RailSim Remote is Running: This assumes you have downloaded and started the RailSim Remote server.
Send HTTP Request: The code uses the requests library (in Python) to send an HTTP GET request to the RailSim Remote server's endpoint for getting the locomotive name.
Handle the Response: The code parses the JSON response from the server and prints the locomotive name.
4. Next Steps
Choose Your Path: Decide whether you want to interact with raildriver.dll directly or use RailSim Remote.
Set Up Your Environment:
Direct DLL: Configure your development environment to load and use DLLs (this varies by language and OS).
RailSim Remote: Download RailSim Remote from GitHub and follow its instructions to run the server. Install a library like requests (Python), or the equivalent in your language, to make HTTP requests.
Implement "Hello World": Get the basic example working in your chosen language.
Explore the API: Once you have basic communication working, explore the available functions (in raildriver.dll) or endpoints (in RailSim Remote) to get and set train parameters.
Alright, let's outline the steps to connect to Train Simulator Classic 2024 programmatically using a C routine and stop a moving train. Keep in mind that direct interaction with the game's DLL requires understanding its API, which isn't officially and comprehensively documented by the developers. The most reliable approach currently involves using the RailDriver.dll and potentially the insights from community efforts like the RailSim Remote project.

** Prerequisites:**

Train Simulator Classic 2024 Installed: Ensure the game is fully installed on your Windows ThinkPad i7.
Development Environment: You'll need a C development environment set up (e.g., Visual Studio, GCC with MinGW).
Understanding of DLL Interaction in C: You should be familiar with concepts like loading DLLs, getting function pointers, and calling functions from a DLL.
Steps:

** Step 1: Locate raildriver.dll **
The primary interface for external control appears to be the raildriver.dll file. This is typically located within your Train Simulator Classic installation directory, usually under a plugins subfolder (e.g., C:\Program Files (x86)\Steam\steamapps\common\RailWorks\plugins\raildriver.dll).

** Step 2: Load the DLL in your C Routine **
You'll need to use Windows API functions to load the raildriver.dll into your C program. The key functions are LoadLibrary() and FreeLibrary().

```
#include <windows.h>
#include <stdio.h>

HMODULE hRailDriver = NULL;

// Function pointer types (will be defined in Step 3)
typedef char* (*GETLOCOMOTIVENAME)();
typedef int (*GETCONTROLLERID)(const char* szControllerName);
typedef float (*GETCONTROLLERVALUE)(int nControllerID, int nType);
typedef void (*SETCONTROLLERVALUE)(int nControllerID, float fValue);
typedef bool (*GETRAILSIMCONNECTED)();

GETLOCOMOTIVENAME GetLocomotiveName = NULL;
GETCONTROLLERID GetControllerID = NULL;
GETCONTROLLERVALUE GetControllerValue = NULL;
SETCONTROLLERVALUE SetControllerValue = NULL;
GETRAILSIMCONNECTED GetRailSimConnected = NULL;

int main() {
    hRailDriver = LoadLibrary("raildriver.dll");
    if (hRailDriver == NULL) {
        fprintf(stderr, "Error loading raildriver.dll: %d\n", GetLastError());
        return 1;
    }
    printf("raildriver.dll loaded successfully.\n");

    // Get function pointers (Step 3)
    // ...

    FreeLibrary(hRailDriver);
    return 0;
}
```

** Step 3: Get Function Pointers **
Once the DLL is loaded, you need to get the memory addresses (function pointers) of the functions you want to call. You'll use the GetProcAddress() function for this. Based on community findings, some relevant functions for controlling the train include:

```
GetLocomotiveName = (GETLOCOMOTIVENAME)GetProcAddress(hRailDriver, "GetLocoName");
    GetControllerID = (GETCONTROLLERID)GetProcAddress(hRailDriver, "GetControllerID");
    GetControllerValue = (GETCONTROLLERVALUE)GetProcAddress(hRailDriver, "GetControllerValue");
    SetControllerValue = (SETCONTROLLERVALUE)GetProcAddress(hRailDriver, "SetControllerValue");
    GetRailSimConnected = (GETRAILSIMCONNECTED)GetProcAddress(hRailDriver, "GetRailSimConnected");

    if (!GetLocomotiveName || !GetControllerID || !GetControllerValue || !SetControllerValue || !GetRailSimConnected) {
        fprintf(stderr, "Error getting function addresses.\n");
        FreeLibrary(hRailDriver);
        return 1;
    }
    printf("Function pointers obtained.\n");
```

** Step 4: Verify Connection to Train Simulator **
Before attempting to control anything, check if your program can detect if Train Simulator is running and the RailDriver interface is active.

```
if (GetRailSimConnected()) {
        printf("Train Simulator is connected.\n");
    } else {
        printf("Train Simulator is not connected.\n");
        FreeLibrary(hRailDriver);
        return 1;
    }
```

** Step 5: Get the Controller ID for the "Train Brake" **
To stop the train, you'll need to control the "Train Brake" (or a similar master brake control). You'll use GetControllerID() to find the numerical ID associated with this control for the currently active locomotive. The exact string for the train brake controller might vary between locomotives. You might need to experiment or consult community resources to find the correct string for the locomotives you intend to control. Common possibilities include:

* "TrainBrake"
* "BrakeTrain"
* "MasterBrake"

```
const char* trainBrakeName = "TrainBrake"; // You might need to try other names
    int trainBrakeId = GetControllerID(trainBrakeName);

    if (trainBrakeId == -1) {
        fprintf(stderr, "Could not find controller ID for '%s'.\n", trainBrakeName);
        FreeLibrary(hRailDriver);
        return 1;
    }
    printf("Controller ID for '%s': %d\n", trainBrakeName, trainBrakeId);
```

** Step 6: Continuously Monitor Speed ** 
To stop the train while it's moving, you'll likely want to monitor its speed. There might be a controller for "Speed" or you might need to infer it from the rate of change of position (which might be more complex to access through this interface). For simplicity, let's assume there's a "Speed" controller you can read (you'd get its ID similarly to the brake).

```
const char* speedControllerName = "Speed"; // This might not exist directly; you might need to find a relevant control
    int speedControllerId = GetControllerID(speedControllerName);
    if (speedControllerId != -1) {
        float currentSpeed = GetControllerValue(speedControllerId, 0); // 0 usually means current value
        printf("Current Speed: %f\n", currentSpeed);
    } else {
        printf("Could not find controller ID for '%s'.\n", speedControllerName);
    }
```

** Step 7: Set the "Train Brake" Value to Apply Brakes ** 
The value range for the train brake controller typically goes from 0.0 (fully released) to 1.0 (fully applied). To stop the train, you'll want to set this value towards 1.0.

```
float brakeValueToApply = 1.0f;
    SetControllerValue(trainBrakeId, brakeValueToApply);
    printf("Train brake set to %f.\n", brakeValueToApply);

    // You might want to add a loop here to continuously check the speed
    // and potentially reduce the brake application as the train slows down
    // for a smoother stop, but for a simple stop, setting it to 1.0 might suffice.

    // Example of a simple loop to wait for the train to (theoretically) stop
    // This is a very basic example and might need adjustments based on the sim's behavior.
    if (speedControllerId != -1) {
        float currentSpeed;
        do {
            Sleep(1000); // Wait for 1 second
            currentSpeed = GetControllerValue(speedControllerId, 0);
            printf("Current Speed: %f\n", currentSpeed);
        } while (currentSpeed > 0.1f); // Wait until speed is close to zero
        printf("Train has likely stopped.\n");
    }
```

** Step 8: Clean Up ** 
When your program is finished, remember to release the loaded DLL.

```
FreeLibrary(hRailDriver);
    printf("raildriver.dll unloaded.\n");
    return 0;
```

# Important Considerations and Challenges:

**  Controller Names Vary:** The string names for controllers like "TrainBrake" are not standardized across all locomotives in Train Simulator Classic. You will likely need to identify the correct names for the specific locomotives you want to control. Tools or community-provided lists might be helpful here.
Controller Value Ranges: The exact meaning and range of values for different controllers can vary. Experimentation and observation within the game might be necessary.
** No Official Comprehensive Documentation:** The lack of official, detailed documentation for this external interface makes development challenging. You'll rely heavily on community findings and experimentation.
** Error Handling:** Implement error handling everywhere to catch issues like the DLL not loading, functions not being found, or invalid controller IDs.

## Next Steps:

Run the game and identify a locomotive you want to control.
Search online forums (especially Rail-Sim.de and the Steam Community) for information on controller names for that specific locomotive.
Start with a simple C or Python program to load raildriver.dll and check the connection status.
Try to get the locomotive name using GetLocomotiveName().
Experiment with GetControllerID() using potential names for the train brake.
Once you have the ID, try reading its value using GetControllerValue() while manually applying the brakes in the game to observe the value range.
Attempt to set the brake value using SetControllerValue() to stop a moving train in a controlled scenario.
